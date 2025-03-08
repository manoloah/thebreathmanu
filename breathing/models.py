from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Avg, Max, Min
from collections import defaultdict

class BreathingExercise(models.Model):
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    duration_minutes = models.IntegerField(help_text="Approximate duration in minutes")
    video_url = models.URLField(blank=True, null=True)
    audio_url = models.URLField(blank=True, null=True)
    instructions = models.TextField(help_text="Step by step instructions for the exercise")
    benefits = models.TextField(help_text="Benefits of this breathing exercise")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class UserSession(models.Model):
    MOOD_CHOICES = [
        ('very_bad', 'Very Bad'),
        ('bad', 'Bad'),
        ('neutral', 'Neutral'),
        ('good', 'Good'),
        ('very_good', 'Very Good'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise = models.ForeignKey(BreathingExercise, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    duration_minutes = models.IntegerField(null=True, blank=True)
    mood_before = models.CharField(max_length=20, choices=MOOD_CHOICES, null=True, blank=True)
    mood_after = models.CharField(max_length=20, choices=MOOD_CHOICES, null=True, blank=True)
    notes = models.TextField(blank=True)
    energy_level = models.IntegerField(null=True, blank=True, help_text="Energy level after practice (1-10)")
    focus_level = models.IntegerField(null=True, blank=True, help_text="Focus level after practice (1-10)")
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.exercise.name} - {self.start_time}"

    def save(self, *args, **kwargs):
        if self.end_time and self.start_time:
            duration = self.end_time - self.start_time
            self.duration_minutes = duration.seconds // 60
        super().save(*args, **kwargs)

class UserPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_exercises = models.ManyToManyField(BreathingExercise, blank=True)
    daily_reminder = models.TimeField(null=True, blank=True)
    notification_enabled = models.BooleanField(default=True)
    theme = models.CharField(max_length=20, default='light')
    practice_goal_minutes = models.IntegerField(default=10, help_text="Daily practice goal in minutes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s preferences"

class BreathingMetrics(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='breathing_metrics')
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    
    # BOLT Score (Body Oxygen Level Test)
    bolt_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="BOLT score in seconds"
    )
    
    # Maximum Breathlessness Test
    mbt_steps = models.IntegerField(
        validators=[MinValueValidator(0)],
        help_text="Number of steps achieved in Maximum Breathlessness Test"
    )
    
    # Optional notes about the test conditions
    notes = models.TextField(blank=True)
    
    # Test conditions that might affect results
    stress_level = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Stress level during test (1-10)",
        null=True,
        blank=True
    )
    
    hours_slept = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(24)],
        help_text="Hours of sleep before test",
        null=True,
        blank=True
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-time']
        verbose_name = "Breathing Metrics"
        verbose_name_plural = "Breathing Metrics"

    def __str__(self):
        return f"{self.user.username}'s metrics - {self.date}"

    @property
    def bolt_score_change(self):
        """Calculate change from previous BOLT score"""
        previous_metric = BreathingMetrics.objects.filter(
            user=self.user,
            date__lt=self.date
        ).order_by('-date', '-time').first()
        
        if previous_metric:
            return self.bolt_score - previous_metric.bolt_score
        return None

    @property
    def mbt_steps_change(self):
        """Calculate change from previous MBT steps"""
        previous_metric = BreathingMetrics.objects.filter(
            user=self.user,
            date__lt=self.date
        ).order_by('-date', '-time').first()
        
        if previous_metric:
            return self.mbt_steps - previous_metric.mbt_steps
        return None

    @classmethod
    def get_weekly_average(cls, user, metric_type='bolt_score'):
        """Get average for the last 7 days"""
        seven_days_ago = datetime.now().date() - timedelta(days=7)
        metrics = cls.objects.filter(
            user=user,
            date__gte=seven_days_ago
        )
        if metric_type == 'bolt_score':
            values = [m.bolt_score for m in metrics]
        else:
            values = [m.mbt_steps for m in metrics]
        
        return sum(values) / len(values) if values else 0

    @classmethod
    def get_monthly_progress(cls, user):
        """Get monthly progress summary"""
        thirty_days_ago = datetime.now().date() - timedelta(days=30)
        metrics = cls.objects.filter(
            user=user,
            date__gte=thirty_days_ago
        ).order_by('date')
        
        if not metrics:
            return None
            
        first_metric = metrics.first()
        last_metric = metrics.last()
        
        return {
            'bolt_score_change': last_metric.bolt_score - first_metric.bolt_score,
            'mbt_steps_change': last_metric.mbt_steps - first_metric.mbt_steps,
            'measurements_count': metrics.count(),
            'start_date': first_metric.date,
            'end_date': last_metric.date
        }

    @classmethod
    def get_time_period_stats(cls, user, start_date, end_date, metric_type='bolt_score'):
        """Get statistics for a specific time period"""
        metrics = cls.objects.filter(
            user=user,
            date__gte=start_date,
            date__lte=end_date
        )
        
        if not metrics.exists():
            return None

        values = [getattr(m, metric_type) for m in metrics]
        return {
            'average': sum(values) / len(values),
            'max': max(values),
            'min': min(values),
            'count': len(values),
            'first_date': metrics.first().date,
            'last_date': metrics.last().date,
            'improvement': values[-1] - values[0] if len(values) > 1 else 0
        }

    @classmethod
    def get_weekly_stats(cls, user, weeks=4):
        """Get weekly statistics for the specified number of weeks"""
        end_date = timezone.now().date()
        start_date = end_date - timedelta(weeks=weeks)
        
        metrics = cls.objects.filter(
            user=user,
            date__gte=start_date,
            date__lte=end_date
        ).order_by('date')

        weekly_data = defaultdict(lambda: {'bolt_scores': [], 'mbt_steps': []})
        
        for metric in metrics:
            # Get the monday of the week for this metric
            week_start = metric.date - timedelta(days=metric.date.weekday())
            weekly_data[week_start]['bolt_scores'].append(metric.bolt_score)
            weekly_data[week_start]['mbt_steps'].append(metric.mbt_steps)

        result = []
        for week_start in sorted(weekly_data.keys()):
            week_data = weekly_data[week_start]
            result.append({
                'week_start': week_start,
                'week_end': week_start + timedelta(days=6),
                'bolt_score_avg': sum(week_data['bolt_scores']) / len(week_data['bolt_scores']),
                'mbt_steps_avg': sum(week_data['mbt_steps']) / len(week_data['mbt_steps']),
                'measurements_count': len(week_data['bolt_scores'])
            })
        
        return result

    @classmethod
    def get_monthly_stats(cls, user, months=12):
        """Get monthly statistics for the specified number of months"""
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=30 * months)
        
        metrics = cls.objects.filter(
            user=user,
            date__gte=start_date,
            date__lte=end_date
        ).order_by('date')

        monthly_data = defaultdict(lambda: {'bolt_scores': [], 'mbt_steps': []})
        
        for metric in metrics:
            month_key = f"{metric.date.year}-{metric.date.month:02d}"
            monthly_data[month_key]['bolt_scores'].append(metric.bolt_score)
            monthly_data[month_key]['mbt_steps'].append(metric.mbt_steps)

        result = []
        for month_key in sorted(monthly_data.keys()):
            month_data = monthly_data[month_key]
            result.append({
                'month': month_key,
                'bolt_score_avg': sum(month_data['bolt_scores']) / len(month_data['bolt_scores']),
                'mbt_steps_avg': sum(month_data['mbt_steps']) / len(month_data['mbt_steps']),
                'measurements_count': len(month_data['bolt_scores'])
            })
        
        return result

    @classmethod
    def get_quarterly_stats(cls, user, quarters=4):
        """Get quarterly statistics"""
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=90 * quarters)
        
        metrics = cls.objects.filter(
            user=user,
            date__gte=start_date,
            date__lte=end_date
        ).order_by('date')

        quarterly_data = defaultdict(lambda: {'bolt_scores': [], 'mbt_steps': []})
        
        for metric in metrics:
            quarter = (metric.date.month - 1) // 3 + 1
            quarter_key = f"{metric.date.year}-Q{quarter}"
            quarterly_data[quarter_key]['bolt_scores'].append(metric.bolt_score)
            quarterly_data[quarter_key]['mbt_steps'].append(metric.mbt_steps)

        result = []
        for quarter_key in sorted(quarterly_data.keys()):
            quarter_data = quarterly_data[quarter_key]
            result.append({
                'quarter': quarter_key,
                'bolt_score_avg': sum(quarter_data['bolt_scores']) / len(quarter_data['bolt_scores']),
                'mbt_steps_avg': sum(quarter_data['mbt_steps']) / len(quarter_data['mbt_steps']),
                'measurements_count': len(quarter_data['bolt_scores'])
            })
        
        return result

    @classmethod
    def get_yearly_stats(cls, user, years=2):
        """Get yearly statistics"""
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=365 * years)
        
        metrics = cls.objects.filter(
            user=user,
            date__gte=start_date,
            date__lte=end_date
        ).order_by('date')

        yearly_data = defaultdict(lambda: {'bolt_scores': [], 'mbt_steps': []})
        
        for metric in metrics:
            year_key = str(metric.date.year)
            yearly_data[year_key]['bolt_scores'].append(metric.bolt_score)
            yearly_data[year_key]['mbt_steps'].append(metric.mbt_steps)

        result = []
        for year_key in sorted(yearly_data.keys()):
            year_data = yearly_data[year_key]
            result.append({
                'year': year_key,
                'bolt_score_avg': sum(year_data['bolt_scores']) / len(year_data['bolt_scores']),
                'mbt_steps_avg': sum(year_data['mbt_steps']) / len(year_data['mbt_steps']),
                'measurements_count': len(year_data['bolt_scores']),
                'improvement': {
                    'bolt_score': year_data['bolt_scores'][-1] - year_data['bolt_scores'][0],
                    'mbt_steps': year_data['mbt_steps'][-1] - year_data['mbt_steps'][0]
                } if len(year_data['bolt_scores']) > 1 else None
            })
        
        return result

    @classmethod
    def get_chart_data(cls, user, period='month'):
        """
        Get data formatted for charts
        period can be: 'week', 'month', 'quarter', 'year'
        """
        if period == 'week':
            data = cls.get_weekly_stats(user, weeks=4)
            date_key = 'week_start'
        elif period == 'month':
            data = cls.get_monthly_stats(user, months=12)
            date_key = 'month'
        elif period == 'quarter':
            data = cls.get_quarterly_stats(user, quarters=4)
            date_key = 'quarter'
        else:  # year
            data = cls.get_yearly_stats(user, years=2)
            date_key = 'year'

        return {
            'labels': [str(item[date_key]) for item in data],
            'datasets': [
                {
                    'label': 'BOLT Score Average',
                    'data': [item['bolt_score_avg'] for item in data]
                },
                {
                    'label': 'MBT Steps Average',
                    'data': [item['mbt_steps_avg'] for item in data]
                }
            ]
        } 