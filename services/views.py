from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.exceptions import PermissionDenied
from .models import Service
from .serializers import ServiceSerializer
from .permissions import IsNailDesignerOrReadOnly

# Listagem pública: só serviços ativos, leitura para qualquer um
class PublicServiceListView(generics.ListAPIView):
    queryset = Service.objects.filter(is_active=True)
    serializer_class = ServiceSerializer
    permission_classes = []  # sem autenticação

# Listagem e criação para Nail Designer: lista todos (ativos e inativos), permite criar
class ServiceListCreateView(generics.ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    parser_classes = [MultiPartParser, FormParser]  # Suporta upload de arquivos

    def get_permissions(self):
        # Protege a criação para nail designer autenticado
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        user = self.request.user
        if not user.is_nail_designer:
            raise PermissionDenied("Apenas a Nail Designer pode cadastrar serviços.")
        serializer.save()

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.is_nail_designer:
            return Service.objects.all()
        else:
            return Service.objects.none()

# Retrieve / update / destroy (editar, ativar/desativar)
class ServiceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsNailDesignerOrReadOnly]
    parser_classes = [JSONParser, MultiPartParser, FormParser]  # Suporta upload de arquivos na edição
