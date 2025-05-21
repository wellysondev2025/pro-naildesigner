from rest_framework import generics
from .models import GalleryImage
from .serializers import GalleryImageSerializer

class GalleryImageListView(generics.ListAPIView):
    queryset = GalleryImage.objects.all().order_by('-uploaded_at')
    serializer_class = GalleryImageSerializer
