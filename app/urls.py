from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.home_page, name='index'),
    path('detail_page/<int:pk>', views.detail_page, name='detail_page'),
    path('get_notes/<int:label_id>/', views.get_notes, name='get_notes'),
    path('edit_note/<int:pk>', views.edit_note, name='edit_note'),
    path('create_new_label/', views.create_new_label, name='create_new_label'), 
    path('create_new_note/', views.create_new_note, name='create_new_note'),
    path('complete_note/<int:pk>/', views.complete_note, name='complete_note'),
    path('delete-note/<int:pk>/', views.delete_note, name='delete_note'),
    path('delete-note_permanently/<int:pk>/', views.delete_note_permanently, name='delete_note_permanently'),
    path('restore_note/<int:pk>/', views.restore_note, name='restore_note'),
    path('trash_bin/', views.trash_bin, name='trash_bin'),
    path('delete-old-notes/', views.delete_old_note, name='delete_old_notes'),
    path('delete-label/<int:pk>/', views.delete_label, name='delete_label'),
    path('pin_note/<int:pk>/', views.pin_note, name='pin_note') 
]

