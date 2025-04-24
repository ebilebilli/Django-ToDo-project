from django.db import models
from datetime import datetime, timezone, timedelta
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User


class Label(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=70)
    is_trashed = models.BooleanField(default=False)

    def __str__(self):
        return f'Label name: {self.title}'


class Note(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        null=True, 
        blank=True 
    )
    
    label = models.ForeignKey(
        Label,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='notes'
    )
    is_completed = models.BooleanField(default=False)
    is_pinned = models.BooleanField(default=False)
    is_trashed = models.BooleanField(default=False)

    context = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
         return self.context


class Trash_Bin(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        null=True, 
        blank=True 
    )
    label = models.ForeignKey(
        Label, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='trashed_labels'
    )
    note = models.ForeignKey(
        Note, 
        on_delete=models.CASCADE,
        related_name='trashed_notes',
        null=True,
        blank=True
    ) 
   
    deleted_at = models.DateTimeField(auto_now_add=True)
    is_trashed = models.BooleanField(default=True)
     

    class Meta:
        unique_together = [
            ('user', 'note'),
            ('user', 'label')

    ]

    def days_left(self):
        limit_date = self.deleted_at + timedelta(days=30)
        remaining_time = limit_date - datetime.now(timezone.utc)
        days_left = remaining_time.days
        return days_left

    def clean(self):
        if self.note and self.label:
            raise ValidationError('You can choose only one,label or note')
        if not self.note and not self.label:
            raise ValidationError('At least you must choose one of, label or note')      
    
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)
    
    def __str__(self):
        if self.note:
            return self.note.context  
        return ''
