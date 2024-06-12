from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

#Lo declaro por si en un momento se llega a modificar la tabla User.
class User(AbstractUser):

    def __str__(self):
        return self.username
    