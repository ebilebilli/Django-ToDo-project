from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

from .models import Note, Label


@receiver(post_save, sender=Note)
def clear_note_cache(sender, instance, **kwargs):
    cache.delete_pattern(f'note_list_{instance.user.id}*')
    if instance.label:
        cache.delete_pattern(f'label_{instance.label.id}_note_list_{instance.user.id}*')
    cache.delete_pattern(f'note_detail_{instance.id}_user_{instance.user.id}')

@receiver(post_save, sender=Label)
def clear_label_cache(sender, instance, **kwargs):
    cache.delete_pattern(f'label_list_{instance.user.id}*')
    cache.delete_pattern(f'label_detail_{instance.id}_user_{instance.user.id}')

@receiver(post_delete, sender=Note)
def clear_note_cache_on_delete(sender, instance, **kwargs):
    cache.delete_pattern(f'note_list_{instance.user.id}*')
    if instance.label:
        cache.delete_pattern(f'label_{instance.label.id}_note_list_{instance.user.id}*')
    cache.delete_pattern(f'note_detail_{instance.id}_user_{instance.user.id}')

@receiver(post_delete, sender=Label)
def clear_label_cache_on_delete(sender, instance, **kwargs):
    cache.delete_pattern(f'label_list_{instance.user.id}*')
    cache.delete_pattern(f'label_detail_{instance.id}_user_{instance.user.id}')