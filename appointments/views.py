from rest_framework import viewsets, permissions
from .models import Appointment
from rest_framework.decorators import action
from .serializers import AppointmentSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'scheduled_datetime']

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)
    
    def get_queryset(self):
        user = self.request.user
        # Nail designer vê todos, clientes veem só os seus
        if user.is_nail_designer:
            return Appointment.objects.all()
        return Appointment.objects.filter(client=user)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my(self, request):
        """Retorna somente os agendamentos do cliente autenticado"""
        user = request.user
        queryset = Appointment.objects.filter(client=user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
