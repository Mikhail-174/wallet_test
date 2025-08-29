from django.db import models
import uuid

class Wallet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.DecimalField(max_digits=52, decimal_places=2, default=0)

    def __str__(self):
        return str(self.account)