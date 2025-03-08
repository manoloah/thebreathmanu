from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'exercises', views.BreathingExerciseViewSet, basename='breathing-exercise')
router.register(r'sessions', views.UserSessionViewSet, basename='user-session')
router.register(r'preferences', views.UserPreferenceViewSet, basename='user-preference')
router.register(r'metrics', views.BreathingMetricsViewSet, basename='breathing-metrics')

urlpatterns = [
    path('', include(router.urls)),
] 