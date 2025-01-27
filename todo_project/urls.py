from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    path('detail_page/<int:pk>/', views.detail_page, name='detail_page'),
    path('trash_bin/', views.trash_bin, name='trash_bin')  
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
