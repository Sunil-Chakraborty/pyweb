# photo_gallery/urls.py
from django.urls import path
from .views import gallery_view


app_name = 'photo_gallery'

urlpatterns = [
    path('gallery/', gallery_view, name='gallery'),
]
