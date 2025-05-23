from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_nail_designer = models.BooleanField(default=False)
    phone = models.CharField(max_length=20, unique=True, null=True, blank=True)
    phone_verified = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username
