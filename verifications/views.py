from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import PhoneVerificationCode
from twilio.rest import Client
from django.conf import settings

class SendPhoneVerificationCodeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        code_obj, created = PhoneVerificationCode.objects.get_or_create(user=user)
        
        if not created and not code_obj.is_expired():
            send_sms(user.phone, code_obj.code)
            return Response({'detail': 'Código reenviado'}, status=status.HTTP_200_OK)

        code_obj.code = PhoneVerificationCode.generate_code()
        code_obj.save()
        send_sms(user.phone, code_obj.code)
        return Response({'detail': 'Código enviado'}, status=status.HTTP_200_OK)


class ValidatePhoneCodeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        code_input = request.data.get('code')
        user = request.user

        try:
            code_obj = PhoneVerificationCode.objects.get(user=user)
        except PhoneVerificationCode.DoesNotExist:
            return Response({'detail': 'Código não encontrado'}, status=status.HTTP_404_NOT_FOUND)

        if code_obj.is_expired():
            return Response({'detail': 'Código expirado'}, status=status.HTTP_400_BAD_REQUEST)

        if code_obj.code == code_input:
            user.phone_verified = True
            user.save()
            code_obj.delete()
            return Response({'detail': 'Telefone verificado com sucesso'}, status=status.HTTP_200_OK)

        return Response({'detail': 'Código inválido'}, status=status.HTTP_400_BAD_REQUEST)


def send_sms(phone_number, code):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    client.messages.create(
        to=phone_number,
        from_=settings.TWILIO_PHONE_NUMBER,
        body=f"Seu código de verificação é: {code}"
    )
