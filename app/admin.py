from django.contrib import admin
from .models import Label, Note, Trash_Bin


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'is_trashed')
    list_filter = ('is_trashed', 'created_at')
    search_fields = ('title',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(user=request.user)
        return qs


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('context', 'label', 'status', 'is_completed', 'is_pinned', 'is_trashed', 'created_at')
    list_filter = ('status', 'is_completed', 'is_pinned', 'is_trashed', 'created_at')
    search_fields = ('context',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(label__user=request.user)
        return qs


@admin.register(Trash_Bin)
class TrashBinAdmin(admin.ModelAdmin):
    list_display = ('note', 'label', 'user', 'deleted_at', 'days_left')
    list_filter = ('deleted_at',)
    search_fields = ('note__context', 'label__title')
    date_hierarchy = 'deleted_at'
    ordering = ('-deleted_at',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(user=request.user)
        return qs
