import 'package:flutter/material.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'package:frontend/theme/app_theme.dart';
import 'package:frontend/screens/auth/email_auth_screen.dart';

class AuthScreen extends StatelessWidget {
  const AuthScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 24.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const Spacer(),
              Text(
                'Aumenta tu rendimiento y capacidad de manejar el estrés con la respiración',
                style: AppTypography.h1.copyWith(
                  fontSize: 28,
                  height: 1.3,
                ),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 16),
              Text(
                'La aplicación de breathwork para atletas y empresarios en alto estrés como tu',
                style: AppTypography.bodyLarge.copyWith(
                  color: AppColors.softGray,
                ),
                textAlign: TextAlign.center,
              ),
              const Spacer(),
              _buildAuthButton(
                context,
                'Continuar con Email',
                FontAwesomeIcons.envelope,
                AppColors.white,
                () {
                  Navigator.of(context).push(
                    MaterialPageRoute(
                      builder: (context) => const EmailAuthScreen(),
                    ),
                  );
                },
              ),
              const SizedBox(height: 16),
              _buildAuthButton(
                context,
                'Continuar con Google',
                FontAwesomeIcons.google,
                const Color(0xFF4285F4),
                () {
                  // TODO: Implement Google sign in
                },
              ),
              const SizedBox(height: 16),
              _buildAuthButton(
                context,
                'Continuar con Apple',
                FontAwesomeIcons.apple,
                Colors.black,
                () {
                  // TODO: Implement Apple sign in
                },
                backgroundColor: AppColors.white,
                textColor: Colors.black,
              ),
              const SizedBox(height: 16),
              _buildAuthButton(
                context,
                'Continuar con Facebook',
                FontAwesomeIcons.facebook,
                const Color(0xFF1877F2),
                () {
                  // TODO: Implement Facebook sign in
                },
              ),
              const SizedBox(height: 32),
              RichText(
                textAlign: TextAlign.center,
                text: TextSpan(
                  style: AppTypography.bodySmall.copyWith(
                    color: AppColors.softGray,
                  ),
                  children: [
                    const TextSpan(
                      text: 'Al continuar, aceptas nuestros ',
                    ),
                    TextSpan(
                      text: 'Términos de Servicio',
                      style: TextStyle(
                        color: AppColors.primary,
                        decoration: TextDecoration.underline,
                      ),
                    ),
                    const TextSpan(
                      text: ' y ',
                    ),
                    TextSpan(
                      text: 'Política de Privacidad',
                      style: TextStyle(
                        color: AppColors.primary,
                        decoration: TextDecoration.underline,
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 32),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildAuthButton(
    BuildContext context,
    String text,
    IconData icon,
    Color iconColor,
    VoidCallback onPressed, {
    Color? backgroundColor,
    Color? textColor,
  }) {
    return ElevatedButton(
      onPressed: onPressed,
      style: ElevatedButton.styleFrom(
        backgroundColor: backgroundColor ?? AppColors.deepBlue,
        foregroundColor: textColor ?? AppColors.white,
        padding: const EdgeInsets.symmetric(vertical: 16),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12),
        ),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          FaIcon(
            icon,
            color: iconColor,
            size: 20,
          ),
          const SizedBox(width: 12),
          Text(
            text,
            style: AppTypography.button.copyWith(
              color: textColor ?? AppColors.white,
            ),
          ),
        ],
      ),
    );
  }
} 