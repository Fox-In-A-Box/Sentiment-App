from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('sentiment_api.urls')),
    path('', include('sentiment_frontend.urls')),
]
