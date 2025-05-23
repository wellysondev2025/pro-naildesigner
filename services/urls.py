from django.urls import path
from .views import PublicServiceListView, ServiceListCreateView, ServiceRetrieveUpdateDestroyView

urlpatterns = [
    # rota pública para clientes só verem serviços ativos
    path('public/', PublicServiceListView.as_view(), name='public-service-list'),

    # rota de gerenciamento (Nail Designer) listar e criar
    path('', ServiceListCreateView.as_view(), name='service-list-create'),

    # detalhe/editar/deletar
    path('<int:pk>/', ServiceRetrieveUpdateDestroyView.as_view(), name='service-detail'),
]
