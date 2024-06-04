from django.contrib.auth.models import User
# from uuid import uuid4
from decimal import Decimal

from .models import Profile
# Referral


def try_me(fn):
    try:
        return fn
    except Exception as e:
        #logger.error(e)
        return 1, e

def create_user(data):
    # username, password, uuid_code/ref_code = data
    user = User.objects.create_user(username=data[0], password=data[1])
    if not user:
        return 1, f'user not created'
    profile = Profile(user=user)
    if data[2]:
        referrer = Profile.objects.get(ref_code=data[2])
        if not refr:
            return 1, 'error: not user with this ref_code'
        referral = Referral(referrer=referrer.user, referral=user)
        referral.save()
    profile.save()
    return 0, user