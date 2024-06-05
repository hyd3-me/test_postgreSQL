from django.contrib.auth.models import User
# from uuid import uuid4
from decimal import Decimal

from .models import Profile, Referral
# Referral


def try_me(fn):
    # return func resp or err
    def do_func(args):
        try:
            return fn(args)
        except Exception as e:
            #logger.error(e)
            return 1, e
    return do_func

@try_me
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

@try_me
def get_referrer_by_ref_code(_ref_code):
    profile = Profile.objects.get(ref_code=_ref_code)
    if not profile:
        return 1, 'not user with same ref_code'
    else:
        return 0, profile.user

@try_me
def create_referral_obj(args):
    # args = #1referrer #2 referral
    referral_obj = Referral(referrer=args[0], referral=args[1])
    if not referral_obj:
        return 1, 'dont create referral obj'
    else:
        return 0, referral_obj
