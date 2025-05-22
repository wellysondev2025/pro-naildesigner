from django.urls import path
from .views import SendPhoneVerificationCodeView, ValidatePhoneCodeView

urlpatterns = [
    path('send-code/', SendPhoneVerificationCodeView.as_view(), name='send_code'),
    path('validate-code/', ValidatePhoneCodeView.as_view(), name='validate_code'),
]
