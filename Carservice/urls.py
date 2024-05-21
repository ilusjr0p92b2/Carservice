from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mainapp.urls')),
    path('service/', include('service.urls')),
    path('auth/', include('authapp.urls')),
]
