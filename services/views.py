from rest_framework import generics, permissions
from .models import Service
from .serializers import ServiceSerializer
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics

class ServiceListCreateView(generics.ListCreateAPIView):
    queryset = Service.objects.filter(is_active=True)
    serializer_class = ServiceSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return []

    def perform_create(self, serializer):
        user = self.request.user
        if not user.is_nail_designer:
            raise PermissionDenied("Apenas a Nail Designer pode cadastrar serviços.")
        serializer.save()

class ServiceRetrieveView(generics.RetrieveAPIView):
    queryset = Service.objects.filter(is_active=True)
    serializer_class = ServiceSerializer