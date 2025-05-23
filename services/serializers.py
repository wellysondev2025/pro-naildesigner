from rest_framework import serializers
from .models import Service

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

    def update(self, instance, validated_data):
        # Atualiza campos sem resetar valores não enviados, especialmente is_active e image
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
