from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    path('account/', include('account.urls')),  
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
