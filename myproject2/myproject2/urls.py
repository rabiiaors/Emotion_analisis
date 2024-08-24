# myproject/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Emotion_detection.urls')),  # 'emotion' uygulamasının URL'lerini dahil edin
]

