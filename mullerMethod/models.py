from django.db import models

# Create your models here.


class UserData(models.Model):
    username = models.CharField(max_length=12)
    password = models.CharField(max_length=25)

    def __str__(self):
        return self.username
