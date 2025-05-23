# scripts/populate.py

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nail_salon_backend.settings")
django.setup()

from django.contrib.auth import get_user_model
from services.models import Service

User = get_user_model()

# Superusuário (Nail Designer)
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser(
        username="admin",
        email="admin@email.com",
        password="admin123",
        is_nail_designer=True
    )
    print("✅ Superusuário 'admin' criado!")
else:
    print("ℹ️ Superusuário 'admin' já existe.")

# Usuários comuns
for i in range(1, 3):
    username = f"cliente{i}"
    phone = f"1199999999{i}"  # telefone único para cada usuário
    if not User.objects.filter(username=username).exists():
        User.objects.create_user(
            username=username,
            email=f"{username}@email.com",
            password="cliente123",
            phone=phone
        )
        print(f"✅ Usuário comum '{username}' criado.")
    else:
        print(f"ℹ️ Usuário '{username}' já existe.")

# Serviços
servicos = [
    {"name": "Manicure Simples", "description": "Corte e esmaltação", "price": 30.0, "duration_minutes": 40},
    {"name": "Pedicure", "description": "Higienização e esmaltação dos pés", "price": 35.0, "duration_minutes": 45},
    {"name": "Alongamento de Unha", "description": "Unhas em gel", "price": 90.0, "duration_minutes": 90},
    {"name": "Design de Sobrancelha", "description": "Design com pinça", "price": 25.0, "duration_minutes": 20},
    {"name": "Francesinha", "description": "Detalhe clássico nas unhas", "price": 10.0, "duration_minutes": 10},
    {"name": "Unha Decorada", "description": "Decoração personalizada", "price": 20.0, "duration_minutes": 30},
]

for s in servicos:
    if not Service.objects.filter(name=s["name"]).exists():
        Service.objects.create(**s)
        print(f"✅ Serviço '{s['name']}' criado.")
    else:
        print(f"ℹ️ Serviço '{s['name']}' já existe.")
