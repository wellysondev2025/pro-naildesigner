from rest_framework import viewsets, permissions
from .models import Appointment
from rest_framework.decorators import action
from .serializers import AppointmentSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.dateparse import parse_date
from django.utils.timezone import make_aware
from datetime import datetime, timedelta


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'scheduled_datetime']

    def perform_create(self, serializer):
        user = self.request.user
        # if not user.phone_verified:
        #     raise PermissionDenied("Você precisa verificar seu telefone para criar agendamentos.")
        serializer.save(client=user)

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

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request  # <-- Garantido aqui!
        return context
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def occupied_times(self, request):
        """
        Retorna horários ocupados para um serviço em um dia específico.
        Query params:
         - service: ID do serviço
         - date: data no formato YYYY-MM-DD
        """
        service_id = request.query_params.get('service')
        date_str = request.query_params.get('date')

        if not service_id or not date_str:
            return Response({"error": "Parâmetros 'service' e 'date' são obrigatórios."}, status=400)

        # Parse da data
        date_obj = parse_date(date_str)
        if not date_obj:
            return Response({"error": "Data inválida."}, status=400)

        # Obtem todos os agendamentos para o serviço na data
        start_datetime = make_aware(datetime.combine(date_obj, datetime.min.time()))
        end_datetime = start_datetime + timedelta(days=1)

        appointments = Appointment.objects.filter(
            service_id=service_id,
            scheduled_datetime__gte=start_datetime,
            scheduled_datetime__lt=end_datetime,
            status__in=['pending', 'awaiting_payment', 'confirmed']  # só bloqueia horários não cancelados
        )

        # Calcula os horários ocupados com base no horário inicial e duração do serviço
        occupied_slots = []
        for appt in appointments:
            start = appt.scheduled_datetime
            duration = timedelta(minutes=appt.service.duration_minutes)
            end = start + duration
            occupied_slots.append({
                "start": start.isoformat(),
                "end": end.isoformat(),
            })

        return Response(occupied_slots)
