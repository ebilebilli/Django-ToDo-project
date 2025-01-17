from django.contrib import admin
from .models import Label, Note


class LabelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title')
    search_fields = ('title', 'user__username')
    list_filter = ('user',)
    ordering = ('id',)
    list_per_page = 20


class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'label', 'context', 'is_completed', 'is_pinned', 'created_at')
    search_fields = ('context', 'label__title')
    list_filter = ('is_completed', 'is_pinned', 'created_at', 'label')
    list_editable = ('is_completed', 'is_pinned')
    ordering = ('-created_at',)
    list_per_page = 20


admin.site.register(Label, LabelAdmin)
admin.site.register(Note, NoteAdmin)
