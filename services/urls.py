from django.urls import path
from .views import ServiceListCreateView, ServiceRetrieveView

urlpatterns = [
    path('', ServiceListCreateView.as_view(), name='service-list-create'),
    path('<int:pk>/', ServiceRetrieveView.as_view(), name='service-detail'),
]
