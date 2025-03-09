import 'dart:async';
import 'dart:convert';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:http/http.dart' as http;
import 'package:flutter_dotenv/flutter_dotenv.dart';

class AuthService {
  final FirebaseAuth _auth = FirebaseAuth.instance;
  final String _baseUrl = dotenv.env['DJANGO_API_URL'] ?? 'http://localhost:8000/api';

  // Stream of auth state changes
  Stream<User?> get authStateChanges => _auth.authStateChanges();

  // Get current user's ID token
  Future<String> get userIdToken async {
    return await _auth.currentUser?.getIdToken() ?? '';
  }

  // Sign in with email and password
  Future<UserCredential> signInWithEmail(String email, String password) async {
    try {
      final credential = await _auth.signInWithEmailAndPassword(
        email: email,
        password: password,
      );
      
      // After Firebase auth, sync with Django backend
      await _syncUserWithBackend();
      
      return credential;
    } on FirebaseAuthException catch (e) {
      throw _handleAuthException(e);
    } catch (e) {
      throw 'Ocurrió un error de conexión. Por favor, verifica tu conexión a internet.';
    }
  }

  // Sign up with email and password
  Future<UserCredential> signUpWithEmail(String email, String password) async {
    try {
      // Validate Firebase initialization
      if (_auth == null) {
        throw Exception('Firebase Authentication is not initialized properly');
      }
      
      print('Attempting to create user with email: $email');
      final credential = await _auth.createUserWithEmailAndPassword(
        email: email,
        password: password,
      );
      
      print('User created successfully. User ID: ${credential.user?.uid}');
      
      // After Firebase auth, sync with Django backend
      try {
        await _syncUserWithBackend();
      } catch (syncError) {
        print('Error syncing with backend, but user was created: $syncError');
        // We'll continue since the Firebase user was created successfully
      }
      
      return credential;
    } on FirebaseAuthException catch (e) {
      print('Firebase Auth Error: ${e.code} - ${e.message}');
      throw _handleAuthException(e);
    } on Exception catch (e) {
      print('Firebase Configuration Error: $e');
      if (e.toString().contains('initialization')) {
        throw 'Error de inicialización de Firebase. Por favor, verifica la configuración.';
      }
      throw 'Ocurrió un error con Firebase. Por favor, verifica la configuración e intenta de nuevo.';
    } catch (e) {
      print('Unexpected Error: $e');
      throw 'Ocurrió un error inesperado. Por favor, intenta de nuevo más tarde.';
    }
  }

  // Send password reset email
  Future<void> sendPasswordResetEmail(String email) async {
    try {
      await _auth.sendPasswordResetEmail(email: email);
    } on FirebaseAuthException catch (e) {
      throw _handleAuthException(e);
    }
  }

  // Sign out from both Firebase and clear local storage
  Future<void> signOut() async {
    await _auth.signOut();
  }

  // Sync user data with Django backend
  Future<void> _syncUserWithBackend() async {
    try {
      final token = await userIdToken;
      if (token.isEmpty) {
        throw 'No se pudo obtener el token de autenticación';
      }

      final response = await http.get(
        Uri.parse('$_baseUrl/users/me/'),
        headers: {
          'Authorization': 'Bearer $token',
          'Content-Type': 'application/json',
        },
      );

      if (response.statusCode == 404) {
        // User doesn't exist in Django, create profile
        final createResponse = await http.post(
          Uri.parse('$_baseUrl/users/'),
          headers: {
            'Authorization': 'Bearer $token',
            'Content-Type': 'application/json',
          },
          body: jsonEncode({
            'email': _auth.currentUser?.email,
          }),
        );

        if (createResponse.statusCode != 201) {
          throw 'Error al crear el perfil de usuario';
        }
      } else if (response.statusCode != 200) {
        throw 'Error al sincronizar con el servidor';
      }
    } catch (e) {
      print('Error syncing with backend: $e');
      throw 'Error al conectar con el servidor. Por favor, intenta de nuevo.';
    }
  }

  // Update user profile in Django backend
  Future<void> updateProfile({
    String? sport,
    String? experienceLevel,
    DateTime? dateOfBirth,
  }) async {
    try {
      final token = await userIdToken;
      final response = await http.put(
        Uri.parse('$_baseUrl/users/update_profile/'),
        headers: {
          'Authorization': 'Bearer $token',
          'Content-Type': 'application/json',
        },
        body: jsonEncode({
          if (sport != null) 'sport': sport,
          if (experienceLevel != null) 'experience_level': experienceLevel,
          if (dateOfBirth != null) 'date_of_birth': dateOfBirth.toIso8601String(),
        }),
      );

      if (response.statusCode != 200) {
        throw Exception('Failed to update profile');
      }
    } catch (e) {
      throw Exception('Error updating profile: $e');
    }
  }

  // Handle Firebase Auth exceptions
  String _handleAuthException(FirebaseAuthException e) {
    print('Handling Firebase Auth Exception: ${e.code}');
    switch (e.code) {
      case 'user-not-found':
        return 'No se encontró un usuario con este correo electrónico.';
      case 'wrong-password':
        return 'Contraseña incorrecta.';
      case 'email-already-in-use':
        return 'Ya existe una cuenta con este correo electrónico.';
      case 'invalid-email':
        return 'El correo electrónico no es válido.';
      case 'weak-password':
        return 'La contraseña es demasiado débil.';
      case 'operation-not-allowed':
        return 'La autenticación por correo y contraseña no está habilitada.';
      case 'too-many-requests':
        return 'Demasiados intentos fallidos. Por favor, intenta más tarde.';
      case 'network-request-failed':
        return 'Error de conexión. Por favor, verifica tu conexión a internet.';
      case 'invalid-app-credential':
        return 'Error de configuración de Firebase. Por favor, verifica la configuración.';
      default:
        print('Unhandled Firebase Auth Error Code: ${e.code}');
        return 'Ocurrió un error. Por favor, intenta de nuevo. (${e.code})';
    }
  }
} 