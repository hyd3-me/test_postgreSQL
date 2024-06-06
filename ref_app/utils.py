from django.contrib.auth.models import User
# from uuid import uuid4
from decimal import Decimal

from .models import Profile, Referral
from ref_app import data_app


def try_me(fn):
    # return func resp or err
    def do_func(*args):
        try:
            return fn(*args)
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
        err, referrer = get_referrer_by_ref_code(data[2])
        if err:
            return 1, 'error: not user with this ref_code'
        err, referral_obj = create_referral_obj((referrer, user))
        referral_obj.save()
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
        args[0].profile.is_referrer = True
        args[0].profile.save()
        args[1].profile.is_referral = True
        args[1].profile.save()
        referral_obj.save()
        return 0, referral_obj

@try_me
def get_user_by_id(user_id):
    user = User.objects.get(id=user_id)
    if not user:
        return 1, f'user not found'
    else:
        return 0, user

@try_me
def get_all_referral_from_db():
    return Referral.objects.all()

@try_me
def get_ref_code_by_user(user_obj):
    ref_code = user_obj.profile.ref_code
    if ref_code:
        return 0, ref_code
    else:
        return 1, 'ref_code not found'

@try_me
def get_referrals_by_user(_user_obj):
    refs = _user_obj.referrer.all()
    if not refs:
        return 1, f'referrals not found'
    else:
        return 0, refs

@try_me
def get_money(_user_obj):
    _user_obj.profile.balance += data_app.BONUS9999
    _user_obj.profile.save()
    return 0, _user_obj