// Copy this file to firebase_config.dart and replace the values with your Firebase configuration
import 'package:firebase_core/firebase_core.dart';

class FirebaseConfig {
  static const FirebaseOptions webOptions = FirebaseOptions(
    apiKey: "YOUR_API_KEY",
    authDomain: "YOUR_AUTH_DOMAIN",
    projectId: "YOUR_PROJECT_ID",
    storageBucket: "YOUR_STORAGE_BUCKET",
    messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
    appId: "YOUR_APP_ID",
  );
} 