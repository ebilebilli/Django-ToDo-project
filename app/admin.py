from django.contrib import admin
from .models import Label, Note, Trash_Bin

class LabelAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user') 
    search_fields = ('title', 'user__username')  
    ordering = ('id',)
    list_per_page = 20

class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'label', 'context', 'is_completed', 'is_pinned', 'created_at')
    search_fields = ('context', 'label__title')  
    list_filter = ('is_completed', 'is_pinned', 'created_at', 'label')
    list_editable = ('is_completed', 'is_pinned')
    ordering = ('-created_at',)
    list_per_page = 20

class TrashBinAdmin(admin.ModelAdmin):
    list_display = ('bin_name', 'note', 'deleted_at', 'time_left')  
    search_fields = ('bin_name',)  
    list_filter = ('deleted_at',)  
    ordering = ('-deleted_at',)  

    def time_left(self, obj):
        return obj.time_left()  # time_left() metodunun nəticəsini göstərmək

admin.site.register(Trash_Bin, TrashBinAdmin)
admin.site.register(Label, LabelAdmin)
admin.site.register(Note, NoteAdmin)
