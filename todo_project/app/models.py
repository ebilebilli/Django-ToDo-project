from django.db import models
from django.contrib.auth.models import User


class Label(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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

    context = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.context}'