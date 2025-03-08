import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:frontend/config/firebase_config.dart';
import 'package:frontend/theme/app_theme.dart';
import 'package:frontend/screens/auth/auth_screen.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp(
    options: FirebaseConfig.webOptions,
  );
  runApp(const BreathManuApp());
}

class BreathManuApp extends StatelessWidget {
  const BreathManuApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Breath Manu',
      theme: AppTheme.theme,
      home: const AuthScreen(),
    );
  }
}

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    // Get the text theme from the context
    final textTheme = Theme.of(context).textTheme;

    return Scaffold(
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'Welcome to\nBreath Manu',
                style: textTheme.displayLarge,
              ),
              const SizedBox(height: 16),
              Text(
                'Your personal breathing coach for enhanced athletic performance',
                style: textTheme.bodyLarge,
              ),
              const SizedBox(height: 32),
              Text(
                'Featured Exercises',
                style: textTheme.displaySmall,
              ),
              const SizedBox(height: 16),
              _buildFeatureCard(
                context,
                title: 'Pre-Workout Breathing',
                description: 'Optimize your breathing for maximum performance',
                icon: Icons.fitness_center,
              ),
              const SizedBox(height: 16),
              _buildFeatureCard(
                context,
                title: 'Recovery Session',
                description: 'Enhance your post-workout recovery',
                icon: Icons.refresh,
              ),
            ],
          ),
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          // TODO: Implement quick start session
        },
        backgroundColor: AppColors.primary,
        child: const Icon(Icons.play_arrow),
      ),
    );
  }

  Widget _buildFeatureCard(
    BuildContext context, {
    required String title,
    required String description,
    required IconData icon,
  }) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppColors.deepBlue,
        borderRadius: BorderRadius.circular(12),
      ),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: AppColors.primary.withOpacity(0.1),
              borderRadius: BorderRadius.circular(8),
            ),
            child: Icon(
              icon,
              color: AppColors.primary,
              size: 24,
            ),
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  title,
                  style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                        fontWeight: FontWeight.bold,
                      ),
                ),
                const SizedBox(height: 4),
                Text(
                  description,
                  style: Theme.of(context).textTheme.bodyMedium,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
