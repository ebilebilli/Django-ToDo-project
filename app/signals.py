import logging
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.core.cache import cache

from .models import Note, Label, Trash_Bin


logger = logging.getLogger('app')

#Cache signals
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


#Logging signals
@receiver(post_save, sender=Label)
def log_label_save(sender, instance, created, **kwargs):
    user = instance.user 
    if created:
        logger.info(f'[CreateLabel] User {user.id if user else "Unknown"} created label {instance.id}')
    else:
        logger.info(f'[LabelDetail-Patch] User {user.id if user else "Unknown"} updated label {instance.id}')


@receiver(post_save, sender=Note)
def log_note_save(sender, instance, created, **kwargs):
    user = instance.user 
    if created:
        logger.info(f'[CreateNote] User {user.id if user else "Unknown"} created note {instance.id}')
    else:
        logger.info(f'[NoteDetail-Patch] User {user.id if user else "Unknown"} updated note {instance.id}')

@receiver(post_save, sender=Trash_Bin)
def log_trash_bin_save(sender, instance, created, **kwargs):
    user = instance.user 
    if created:
        if instance.label:
            logger.info(f'[MoveLabelToTrash] User {user.id if user else "Unknown"} added label {instance.label.id} to trash bin')
        elif instance.note:
            logger.info(f'[MoveNoteToTrash] User {user.id if user else "Unknown"} added note {instance.note.id} to trash bin')

@receiver(post_delete, sender=Trash_Bin)
def log_trash_bin_delete(sender, instance, **kwargs):
    user = instance.user 
    if instance.label:
        logger.info(f'[LabelInTrashDetail] User {user.id if user else "Unknown"} restored label {instance.label.id} from trash')
    elif instance.note:
        logger.info(f'[NoteInTrashDetail] User {user.id if user else "Unknown"} restored note {instance.note.id} from trash')