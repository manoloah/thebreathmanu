from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import BreathingExercise, UserSession, UserPreference, BreathingMetrics, UserProfile
from .serializers import (
    BreathingExerciseSerializer,
    UserSessionSerializer,
    UserPreferenceSerializer,
    UserSerializer,
    BreathingMetricsSerializer
)

User = get_user_model()

class BreathingExerciseViewSet(viewsets.ModelViewSet):
    queryset = BreathingExercise.objects.all()
    serializer_class = BreathingExerciseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class UserSessionViewSet(viewsets.ModelViewSet):
    serializer_class = UserSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserSession.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        session = self.get_object()
        session.end_time = timezone.now()
        session.save()
        return Response({'status': 'session completed'})

class UserPreferenceViewSet(viewsets.ModelViewSet):
    serializer_class = UserPreferenceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserPreference.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def my_preferences(self, request):
        preference, created = UserPreference.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(preference)
        return Response(serializer.data)

class BreathingMetricsViewSet(viewsets.ModelViewSet):
    serializer_class = BreathingMetricsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BreathingMetrics.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def progress_summary(self, request):
        """Get a summary of user's breathing metrics progress"""
        latest_metric = self.get_queryset().first()
        if not latest_metric:
            return Response({
                'message': 'No metrics recorded yet'
            }, status=status.HTTP_404_NOT_FOUND)

        return Response({
            'latest_bolt_score': latest_metric.bolt_score,
            'latest_mbt_steps': latest_metric.mbt_steps,
            'weekly_bolt_average': BreathingMetrics.get_weekly_average(request.user, 'bolt_score'),
            'weekly_mbt_average': BreathingMetrics.get_weekly_average(request.user, 'mbt_steps'),
            'monthly_progress': BreathingMetrics.get_monthly_progress(request.user)
        })

    @action(detail=False, methods=['get'])
    def chart_data(self, request):
        """Get data formatted for charts"""
        period = request.query_params.get('period', 'month')
        if period not in ['week', 'month', 'quarter', 'year']:
            return Response(
                {'error': 'Invalid period. Choose from: week, month, quarter, year'},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = BreathingMetrics.get_chart_data(request.user, period)
        return Response(data)

    @action(detail=False, methods=['get'])
    def weekly_stats(self, request):
        """Get weekly statistics"""
        weeks = int(request.query_params.get('weeks', 4))
        data = BreathingMetrics.get_weekly_stats(request.user, weeks=weeks)
        return Response(data)

    @action(detail=False, methods=['get'])
    def monthly_stats(self, request):
        """Get monthly statistics"""
        months = int(request.query_params.get('months', 12))
        data = BreathingMetrics.get_monthly_stats(request.user, months=months)
        return Response(data)

    @action(detail=False, methods=['get'])
    def quarterly_stats(self, request):
        """Get quarterly statistics"""
        quarters = int(request.query_params.get('quarters', 4))
        data = BreathingMetrics.get_quarterly_stats(request.user, quarters=quarters)
        return Response(data)

    @action(detail=False, methods=['get'])
    def yearly_stats(self, request):
        """Get yearly statistics"""
        years = int(request.query_params.get('years', 2))
        data = BreathingMetrics.get_yearly_stats(request.user, years=years)
        return Response(data)

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    def get_object(self):
        return self.request.user

    @action(detail=False, methods=['GET'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['PUT'])
    def update_profile(self, request):
        user = request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user_profile(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
        return Response({
            'email': request.user.email,
            'profile': {
                'sport': profile.sport,
                'experience_level': profile.experience_level,
                'date_of_birth': profile.date_of_birth,
            }
        })
    except UserProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_user_profile(request):
    try:
        UserProfile.objects.get(user=request.user)
        return Response({'detail': 'Profile already exists'}, status=status.HTTP_400_BAD_REQUEST)
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(
            user=request.user,
            sport=request.data.get('sport'),
            experience_level=request.data.get('experience_level'),
            date_of_birth=request.data.get('date_of_birth')
        )
        return Response({
            'email': request.user.email,
            'profile': {
                'sport': profile.sport,
                'experience_level': profile.experience_level,
                'date_of_birth': profile.date_of_birth,
            }
        }, status=status.HTTP_201_CREATED) 