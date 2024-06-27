from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

#Lo declaro por si en un momento se llega a modificar la tabla User.
class Users(AbstractUser):

    def __str__(self):
        return self.username
    
class Chats(models.Model):
    id_usuario = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, null=True)
    start_date = models.DateField(auto_now=True)
    session_key = models.TextField() 

class Messages(models.Model):
    chat = models.ForeignKey(Chats, on_delete=models.CASCADE)
    message = models.TextField()
    send_or_input = models.CharField(max_length=5)
    date_send = models.DateTimeField(auto_now=True)