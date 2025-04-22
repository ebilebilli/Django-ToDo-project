from django.urls import path
from .views import *

app_name = 'app'

urlpatterns = [
    # Label endpoints
    path('labels/', LabelListAPIView.as_view(), name='label-list'),
    path('labels/<int:label_id>/', LabelDetailAPIView.as_view(), name='label-detail'),
    path('labels/create/', CreateLabelAPIView.as_view(), name='label-create'),
    path('labels/<int:label_id>/trash/', MoveLabelToTrashAPIView.as_view(), name='label-to-trash'),

    # Note endpoints
    path('notes/', NoteListAPIView.as_view(), name='note-list'),
    path('notes/<int:note_id>/', NoteDetailAPIView.as_view(), name='note-detail'),
    path('notes/<int:note_id>/', NotePinChangeAPIView.as_view(), name='note-pin-change'),
    path('notes/create/', CreateNoteAPIView.as_view(), name='note-create'),
    path('notes/<int:note_id>/trash/', MoveNoteToTrashAPIView.as_view(), name='note-to-trash'),
    path('labels/<int:label_id>/notes/', NoteListForLabelAPIView.as_view(), name='note-list-for-label'),

    # Trash-bin endpoints (labels)
    path('trash/labels/', TrashBinLabelListAPIView.as_view(), name='trash-label-list'),
    path('trash/labels/<int:label_id>/', LabelInTrashDetailAPIView.as_view(), name='trash-label-detail'),

    # Trash-bin endpoints (notes)
    path('trash/notes/', TrashBinNoteListAPIView.as_view(), name='trash-note-list'),
    path('trash/notes/<int:note_id>/', NoteInTrashDetailAPIView.as_view(), name='trash-note_-detail'),
]