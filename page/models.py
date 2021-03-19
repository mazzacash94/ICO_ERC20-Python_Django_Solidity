from django.db import models

# Create your models here.


class History(models.Model):

    faucetTx = models.TextField()
    contractTx = models.TextField()
