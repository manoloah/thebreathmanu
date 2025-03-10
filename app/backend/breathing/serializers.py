from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import BreathingExercise, UserSession, UserPreference, BreathingMetrics

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'date_of_birth', 'sport', 'experience_level', 'created_at', 'updated_at']
        read_only_fields = ['id', 'email', 'created_at', 'updated_at']

class BreathingExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = BreathingExercise
        fields = '__all__'

class UserSessionSerializer(serializers.ModelSerializer):
    exercise_name = serializers.CharField(source='exercise.name', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = UserSession
        fields = '__all__'

class UserPreferenceSerializer(serializers.ModelSerializer):
    favorite_exercises = BreathingExerciseSerializer(many=True, read_only=True)

    class Meta:
        model = UserPreference
        fields = '__all__'
        read_only_fields = ('user',)

class BreathingMetricsSerializer(serializers.ModelSerializer):
    bolt_score_change = serializers.IntegerField(read_only=True)
    mbt_steps_change = serializers.IntegerField(read_only=True)
    weekly_bolt_average = serializers.SerializerMethodField()
    weekly_mbt_average = serializers.SerializerMethodField()
    monthly_progress = serializers.SerializerMethodField()

    class Meta:
        model = BreathingMetrics
        fields = '__all__'
        read_only_fields = ('user', 'date', 'time', 'created_at', 'updated_at')

    def get_weekly_bolt_average(self, obj):
        return BreathingMetrics.get_weekly_average(obj.user, 'bolt_score')

    def get_weekly_mbt_average(self, obj):
        return BreathingMetrics.get_weekly_average(obj.user, 'mbt_steps')

    def get_monthly_progress(self, obj):
        return BreathingMetrics.get_monthly_progress(obj.user) 