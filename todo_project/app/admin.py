from django.contrib import admin

# Register your models here.
from .models import Label, Note

admin.site.register(Label)
admin.site.register(Note)