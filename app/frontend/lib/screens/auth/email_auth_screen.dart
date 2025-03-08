import 'package:flutter/material.dart';
import 'package:frontend/services/auth_service.dart';
import 'package:frontend/theme/app_theme.dart';

class EmailAuthScreen extends StatefulWidget {
  const EmailAuthScreen({super.key});

  @override
  State<EmailAuthScreen> createState() => _EmailAuthScreenState();
}

class _EmailAuthScreenState extends State<EmailAuthScreen> {
  final _formKey = GlobalKey<FormState>();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  final _confirmPasswordController = TextEditingController();
  final _authService = AuthService();

  bool _isSignUp = false;
  bool _isLoading = false;
  bool _obscurePassword = true;
  String? _errorMessage;

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    _confirmPasswordController.dispose();
    super.dispose();
  }

  Future<void> _submitForm() async {
    if (_formKey.currentState?.validate() ?? false) {
      setState(() {
        _isLoading = true;
        _errorMessage = null;
      });

      try {
        if (_isSignUp) {
          await _authService.signUpWithEmail(
            _emailController.text,
            _passwordController.text,
          );
        } else {
          await _authService.signInWithEmail(
            _emailController.text,
            _passwordController.text,
          );
        }
        // Navigate to home screen or onboarding
        if (mounted) {
          Navigator.of(context).pop();
        }
      } catch (e) {
        setState(() {
          _errorMessage = e.toString();
        });
      } finally {
        if (mounted) {
          setState(() {
            _isLoading = false;
          });
        }
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () => Navigator.of(context).pop(),
          color: AppColors.white,
        ),
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24.0),
          child: Form(
            key: _formKey,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                Text(
                  _isSignUp ? 'Crear cuenta' : 'Iniciar sesión',
                  style: AppTypography.h1,
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 32),
                TextFormField(
                  controller: _emailController,
                  keyboardType: TextInputType.emailAddress,
                  style: AppTypography.bodyLarge.copyWith(color: AppColors.white),
                  decoration: _buildInputDecoration('Correo electrónico'),
                  validator: (value) {
                    if (value == null || value.isEmpty) {
                      return 'Por favor ingresa tu correo electrónico';
                    }
                    if (!RegExp(r'^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$')
                        .hasMatch(value)) {
                      return 'Por favor ingresa un correo electrónico válido';
                    }
                    return null;
                  },
                ),
                const SizedBox(height: 16),
                TextFormField(
                  controller: _passwordController,
                  obscureText: _obscurePassword,
                  style: AppTypography.bodyLarge.copyWith(color: AppColors.white),
                  decoration: _buildInputDecoration('Contraseña', isPassword: true),
                  validator: (value) {
                    if (value == null || value.isEmpty) {
                      return 'Por favor ingresa tu contraseña';
                    }
                    if (_isSignUp && value.length < 6) {
                      return 'La contraseña debe tener al menos 6 caracteres';
                    }
                    return null;
                  },
                ),
                if (_isSignUp) ...[
                  const SizedBox(height: 16),
                  TextFormField(
                    controller: _confirmPasswordController,
                    obscureText: _obscurePassword,
                    style:
                        AppTypography.bodyLarge.copyWith(color: AppColors.white),
                    decoration:
                        _buildInputDecoration('Confirmar contraseña', isPassword: true),
                    validator: (value) {
                      if (value != _passwordController.text) {
                        return 'Las contraseñas no coinciden';
                      }
                      return null;
                    },
                  ),
                ],
                if (_errorMessage != null) ...[
                  const SizedBox(height: 16),
                  Text(
                    _errorMessage!,
                    style: AppTypography.bodyMedium.copyWith(
                      color: AppColors.error,
                    ),
                    textAlign: TextAlign.center,
                  ),
                ],
                const SizedBox(height: 32),
                ElevatedButton(
                  onPressed: _isLoading ? null : _submitForm,
                  style: ElevatedButton.styleFrom(
                    padding: const EdgeInsets.symmetric(vertical: 16),
                    backgroundColor: AppColors.primary,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                  child: _isLoading
                      ? const SizedBox(
                          height: 20,
                          width: 20,
                          child: CircularProgressIndicator(
                            strokeWidth: 2,
                            valueColor:
                                AlwaysStoppedAnimation<Color>(AppColors.white),
                          ),
                        )
                      : Text(
                          _isSignUp ? 'Crear cuenta' : 'Iniciar sesión',
                          style: AppTypography.button,
                        ),
                ),
                const SizedBox(height: 16),
                TextButton(
                  onPressed: () {
                    setState(() {
                      _isSignUp = !_isSignUp;
                      _errorMessage = null;
                    });
                  },
                  child: Text(
                    _isSignUp
                        ? '¿Ya tienes una cuenta? Inicia sesión'
                        : '¿No tienes una cuenta? Regístrate',
                    style: AppTypography.bodyMedium.copyWith(
                      color: AppColors.primary,
                    ),
                  ),
                ),
                if (!_isSignUp) ...[
                  TextButton(
                    onPressed: () {
                      // TODO: Implement forgot password
                    },
                    child: Text(
                      '¿Olvidaste tu contraseña?',
                      style: AppTypography.bodyMedium.copyWith(
                        color: AppColors.softGray,
                      ),
                    ),
                  ),
                ],
              ],
            ),
          ),
        ),
      ),
    );
  }

  InputDecoration _buildInputDecoration(String label, {bool isPassword = false}) {
    return InputDecoration(
      labelText: label,
      labelStyle: AppTypography.bodyMedium.copyWith(color: AppColors.softGray),
      filled: true,
      fillColor: AppColors.deepBlue,
      border: OutlineInputBorder(
        borderRadius: BorderRadius.circular(12),
        borderSide: BorderSide.none,
      ),
      suffixIcon: isPassword
          ? IconButton(
              icon: Icon(
                _obscurePassword ? Icons.visibility_off : Icons.visibility,
                color: AppColors.softGray,
              ),
              onPressed: () {
                setState(() {
                  _obscurePassword = !_obscurePassword;
                });
              },
            )
          : null,
    );
  }
} 