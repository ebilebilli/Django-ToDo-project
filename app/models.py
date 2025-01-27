from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Label(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=70)

    def __str__(self):
        return f'Label name: {self.title}'


class Note(models.Model):
    label = models.ForeignKey(
        Label,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    Processing = 'processing'
    Completed = 'completed'
    
    STATUS_BAR_LIST = [
        (Processing, 'Processing'),
        (Completed, 'Completed')
    ]    
    
    is_completed = models.BooleanField(default=False)
    is_pinned = models.BooleanField(default=False)
    is_trashed = models.BooleanField(default=False)

    context = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.context}'


class Trash_Bin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    bin_name = models.CharField(max_length=100)
    deleted_at = models.DateTimeField(auto_now_add=True)

    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    label = models.ForeignKey(
        Label,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    
    def __str__(self):
        return f'{self.bin_name}'

    def time_left(self):
        limit_date = self.deleted_at + timedelta(days=30)
        remaining_time = limit_date - timezone.now()
        days_left = remaining_time.days

        return days_left