from django.db import models
from django.contrib.auth.models import User


class Sites(models.Model):
    sitename = models.CharField(max_length=350)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)

    class Meta:
        unique_together = ('sitename', 'user')

    def __str__(self):
        return self.sitename


class Credentials(models.Model):
    username = models.CharField(max_length=350)
    password = models.CharField(max_length=350)
    Site = models.ForeignKey(Sites, on_delete=models.CASCADE)

    def __str__(self):
        return "f{self.username}, {self.password}"
