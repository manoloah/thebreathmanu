import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

/// AppColors defines all the colors used in the Breath Manu app.
/// This class provides static access to brand colors for consistent usage across the app.
class AppColors {
  // Private constructor to prevent instantiation
  AppColors._();

  // Main Colors
  static const Color backgroundBlue = Color(0xFF132737);
  static const Color white = Color(0xFFFFFFFF);
  static const Color deepBlue = Color(0xFF003366);
  static const Color modernGreen = Color(0xFF00B383);
  static const Color softGray = Color(0xFFB0B0B0);
  static const Color redOrange = Color(0xFFFF4500);
  static const Color purple = Color(0xFF6A0DAD);

  // Semantic Colors
  static const Color primary = modernGreen;
  static const Color secondary = deepBlue;
  static const Color accent = purple;
  static const Color error = redOrange;
  static const Color background = backgroundBlue;
  static const Color surface = white;
  static const Color onBackground = white;
  static const Color onSurface = deepBlue;
}

/// AppTypography defines all the text styles used in the Breath Manu app.
/// This class provides static access to typography styles for consistent usage across the app.
class AppTypography {
  // Private constructor to prevent instantiation
  AppTypography._();

  // Base text styles
  static final TextStyle _unboundedBase = GoogleFonts.unbounded();
  static final TextStyle _cabinBase = GoogleFonts.cabin();

  // Headings
  static TextStyle h1 = _unboundedBase.copyWith(
    fontSize: 32,
    fontWeight: FontWeight.bold,
    color: AppColors.onBackground,
    height: 1.2,
  );

  static TextStyle h2 = _unboundedBase.copyWith(
    fontSize: 24,
    fontWeight: FontWeight.bold,
    color: AppColors.onBackground,
    height: 1.2,
  );

  static TextStyle h3 = _unboundedBase.copyWith(
    fontSize: 20,
    fontWeight: FontWeight.bold,
    color: AppColors.onBackground,
    height: 1.3,
  );

  // Body text
  static TextStyle bodyLarge = _cabinBase.copyWith(
    fontSize: 16,
    fontWeight: FontWeight.normal,
    color: AppColors.onBackground,
    height: 1.5,
  );

  static TextStyle bodyMedium = _cabinBase.copyWith(
    fontSize: 14,
    fontWeight: FontWeight.normal,
    color: AppColors.onBackground,
    height: 1.5,
  );

  static TextStyle bodySmall = _cabinBase.copyWith(
    fontSize: 12,
    fontWeight: FontWeight.normal,
    color: AppColors.onBackground,
    height: 1.5,
  );

  // Special styles
  static TextStyle button = _cabinBase.copyWith(
    fontSize: 16,
    fontWeight: FontWeight.bold,
    color: AppColors.white,
    letterSpacing: 0.5,
  );

  static TextStyle caption = _cabinBase.copyWith(
    fontSize: 12,
    fontWeight: FontWeight.normal,
    fontStyle: FontStyle.italic,
    color: AppColors.softGray,
    height: 1.4,
  );
}

/// AppTheme provides the main theme configuration for the Breath Manu app.
/// This class creates a ThemeData object that can be used in the MaterialApp.
class AppTheme {
  // Private constructor to prevent instantiation
  AppTheme._();

  /// Get the main theme for the app
  static ThemeData get theme {
    return ThemeData(
      // Base colors
      primaryColor: AppColors.primary,
      scaffoldBackgroundColor: AppColors.background,
      colorScheme: const ColorScheme(
        primary: AppColors.primary,
        secondary: AppColors.secondary,
        surface: AppColors.surface,
        background: AppColors.background,
        error: AppColors.error,
        onPrimary: AppColors.white,
        onSecondary: AppColors.white,
        onSurface: AppColors.onSurface,
        onBackground: AppColors.onBackground,
        onError: AppColors.white,
        brightness: Brightness.dark,
      ),

      // Text theme
      textTheme: TextTheme(
        displayLarge: AppTypography.h1,
        displayMedium: AppTypography.h2,
        displaySmall: AppTypography.h3,
        bodyLarge: AppTypography.bodyLarge,
        bodyMedium: AppTypography.bodyMedium,
        bodySmall: AppTypography.bodySmall,
        labelLarge: AppTypography.button,
        labelSmall: AppTypography.caption,
      ),

      // Button theme
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: AppColors.primary,
          foregroundColor: AppColors.white,
          textStyle: AppTypography.button,
          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(8),
          ),
        ),
      ),
    );
  }
} 