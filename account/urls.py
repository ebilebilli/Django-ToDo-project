from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

app_name = 'account'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login' ),
    path('register/', views.register_request, name='register' )
]