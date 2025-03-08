# The Breath Manu App

A high-performance breathwork application designed for athletes, combining personalized breathing exercises, live musical breathing sessions, and comprehensive performance tracking. The app helps athletes optimize their breathing for enhanced performance, better recovery, and improved mental focus.

## Core Features

### 🎯 Performance Tracking
- BOLT score and MBT measurements
- Integration with wearables (Garmin, Apple Watch)
- Comprehensive health metrics dashboard
- Progress visualization and analytics

### 🏃‍♂️ Sport-Specific Training
- Personalized breathing exercises based on sport type
- Pre/post workout breathing routines
- Sport-specific breathing technique tutorials
- Performance state monitoring

### 🎵 Live Musical Breathing Sessions
- Weekly live breathwork sessions
- Music-integrated breathing exercises
- Interactive group sessions
- Recorded sessions library

### 📚 Exercise Library
- Categorized by purpose (focus, stress relief, performance)
- Sport-specific breathing workouts
- Integration guides for different training types
- Custom playlist creation

### 🎮 Personalized Experience
- AI-driven exercise recommendations
- Daily breathing practice plans
- Progress-based difficulty adjustment
- Custom workout integration

## Project Structure

```
thebreathmanu/
├── app/
│   ├── frontend/          # Flutter application
│   └── backend/          # Django application
│       ├── breathing/    # Main app for breathing functionality
│       ├── breathmanu/   # Django project settings
│       ├── manage.py     # Django management script
│       └── requirements.txt
└── breathing_animations/ # Animation assets
```

## Tech Stack

- **Frontend**: Flutter (Dart) for cross-platform mobile/web application
- **Backend**: Django with Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: Django's built-in authentication system
- **Future Integrations**: 
  - Garmin Connect API
  - Apple HealthKit
  - Machine Learning for personalization

## API Endpoints

### Breathing Metrics
- `GET /api/metrics/` - List all metrics
- `POST /api/metrics/` - Record new metrics
- `GET /api/metrics/progress_summary/` - Get progress overview
- `GET /api/metrics/chart_data/?period=[week|month|quarter|year]` - Get chart data
- `GET /api/metrics/weekly_stats/` - Get weekly statistics
- `GET /api/metrics/monthly_stats/` - Get monthly statistics
- `GET /api/metrics/quarterly_stats/` - Get quarterly statistics
- `GET /api/metrics/yearly_stats/` - Get yearly statistics

### User Sessions
- `GET /api/sessions/` - List all sessions
- `POST /api/sessions/` - Create new session
- `POST /api/sessions/{id}/complete/` - Complete a session

## Getting Started

### Frontend Setup (Flutter)
1. Install Flutter SDK
2. Clone the repository
3. Navigate to frontend directory
4. Run `flutter pub get`
5. Start the app with `flutter run`

### Backend Setup (Django)
1. Create and activate virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   cd app/backend
   pip install -r requirements.txt
   ```

3. Set up PostgreSQL:
   ```bash
   createdb breathmanu
   ```

4. Apply migrations:
   ```bash
   python manage.py migrate
   ```

5. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Run development server:
   ```bash
   python manage.py runserver
   ```

## Development Guidelines

- Follow Django REST Framework best practices
- Implement proper error handling and validation
- Write tests for all new features
- Use type hints in Python code
- Document all API endpoints
- Follow PEP 8 style guide

## Contributing

1. Create a feature branch
2. Make your changes
3. Write/update tests
4. Update documentation
5. Submit a pull request

## License

[Your License Here]
