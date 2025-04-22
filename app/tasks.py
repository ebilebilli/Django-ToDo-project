from celery import shared_task
from django.db import transaction
from datetime import datetime, timezone, timedelta
from app.models import Trash_Bin

@shared_task
def clean_expired_trashbins():
    expired_date = datetime.now(timezone.utc) - timedelta(days=30)
    expired_bins = Trash_Bin.objects.filter(deleted_at__lt=expired_date)
    count = expired_bins.count()
    if count > 0:
        with transaction.atomic():
            expired_bins.delete()
   
