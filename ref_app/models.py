from django.db import models
from django.contrib.auth.models import User

import uuid

# Create your models here.

class Profile(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE)
    ref_code    = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    balance     = models.DecimalField(max_digits=16, decimal_places=2, default=0.0)
    is_referrer = models.BooleanField(default=False)
    is_referral = models.BooleanField(default=False)

class Referral(models.Model):
    referrer        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referrer')
    referral        = models.OneToOneField(User, on_delete=models.CASCADE)
    date_joined     = models.DateTimeField(auto_now_add=True)
    num_purchases   = models.PositiveIntegerField(default=0)
    total_amount    = models.DecimalField(max_digits=16, decimal_places=2, default=0.0)

    def __str__(self):
        return f'refs {self.referrer} >> {self.referral}'
