from django.db import models

class Wallet(models.Model):
    account = models.FloatField(max_digits=52, decimal_places=2, default=0)

    def __str__(self):
        return str(self.account)