from rest_framework import serializers
from .models import Appointment
from users.models import User
from services.models import Service
from services.serializers import ServiceSerializer  # Usa o serializer já existente

# Serializer simples só com os dados necessários do cliente
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone']



class AppointmentSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)
    service = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all()
    )  # <-- Altere aqui para aceitar o ID do serviço
    service_detail = ServiceSerializer(source='service', read_only=True)

    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ['client', 'created_at']

    def validate(self, data):
        request = self.context['request']
        scheduled_datetime = data.get('scheduled_datetime')
        status = data.get('status')

        # Evita conflito de horários
        if scheduled_datetime:
            conflict_exists = Appointment.objects.filter(
                scheduled_datetime=scheduled_datetime
            ).exclude(id=self.instance.id if self.instance else None).exists()
            if conflict_exists:
                raise serializers.ValidationError("Já existe um agendamento nesse horário.")

        # Validação de status
        if 'status' in data:
            current_status = self.instance.status if self.instance else None

            if request.user.is_nail_designer:
                allowed = (current_status == 'pending' and status == 'awaiting_payment') \
                    or (status in ['confirmed', 'completed', 'cancelled'])
                if not allowed:
                    raise serializers.ValidationError(
                        f"Nail Designer não pode alterar de '{current_status}' para '{status}'."
                    )
            else:
                if status != 'cancelled':
                    raise serializers.ValidationError("Clientes só podem cancelar seus agendamentos.")

        # Se cliente marcou que pagou, confirmar automaticamente
        if not request.user.is_nail_designer:
            if data.get('is_partial_paid') is True:
                if self.instance and self.instance.status == 'awaiting_payment':
                    data['status'] = 'confirmed'
                else:
                    raise serializers.ValidationError("Pagamento só pode ser feito após aprovação da Nail Designer.")

        return data

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get('request')
        if request and not request.user.is_nail_designer:
            fields['status'].read_only = False
        return fields
