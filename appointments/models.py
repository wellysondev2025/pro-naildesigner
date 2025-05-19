from django.db import models
from django.conf import settings
from services.models import Service

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('awaiting_payment', 'Aguardando Pagamento'),
        ('confirmed', 'Confirmado'),
        ('completed', 'Concluído'),
        ('cancelled', 'Cancelado'),
    ]

    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    scheduled_datetime = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)  # <- novo campo
    is_partial_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.client.username} - {self.service.name} em {self.scheduled_datetime}"
