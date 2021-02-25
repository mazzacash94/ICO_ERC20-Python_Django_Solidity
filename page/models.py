from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Wallet(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=50)
    privateKey = models.BinaryField(max_length=70)

    def __str__(self):
        return self.address


class History(models.Model):

    paymentTx = models.TextField()
    contractTx = models.TextField()
