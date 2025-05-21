from django.urls import path
from .views import GalleryImageListView

urlpatterns = [
    path('images/', GalleryImageListView.as_view(), name='gallery-image-list'),
]
