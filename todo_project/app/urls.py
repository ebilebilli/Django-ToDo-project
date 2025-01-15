from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.home_page, name='index'),
    path('create_new_note/', views.create_new_note, name='create_new_note'),
    path('complete_task/<int:pk>/', views.complete_note, name='complete_note'),
    path('delete-note/<int:pk>/', views.delete_note, name='delete_note'),
    path('pin_note/<int:pk>', views.pin_note, name='pin_note') 
]

