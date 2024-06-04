from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE)
    ref_code    = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    balance     = models.DecimalField(max_digits=16, decimal_places=2, default=0.0)
    is_referrer = models.BooleanField(default=False)
    is_referral = models.BooleanField(default=False)