from django.db import models
from django.contrib.auth.models import User

class CustomUser(User):
    pass


class EmaiConfirmation(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
