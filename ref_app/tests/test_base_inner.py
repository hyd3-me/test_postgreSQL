from django.test import TestCase, TransactionTestCase
from django.http import HttpRequest
from django.utils import timezone
# from unittest import skip
from datetime import timedelta
import uuid

#from noteqq import test_data
from ref_app import utils
from ref_app import data_app


class UserTest(TestCase):

    def test_try_me_func(self):
        test_wrong_data_arr = ['username', 'userpwd']
        err, resp = utils.create_user(test_wrong_data_arr)
        self.assertTrue(err)
        self.assertTrue(isinstance(resp, Exception))

    def test_create_user(self):
        err, user1 = utils.create_user(data_app.USER1)
        self.assertFalse(err)
        self.assertEqual(user1.username, data_app.USER1[0])
        self.assertEqual(user1.profile.balance, 0)
        self.assertFalse(user1.profile.is_referral)
        self.assertFalse(user1.profile.is_referrer)
        self.assertTrue(isinstance(user1.profile.ref_code, uuid.UUID))
    
    def test_can_get_referrer_by_ref_code(self):
        err, user1 = utils.create_user(data_app.USER1)
        err, resp = utils.get_referrer_by_ref_code(user1.profile.ref_code)
        self.assertFalse(err)
        self.assertEqual(user1, resp)
    
    def test_create_referral_obj(self):
        err, user1 = utils.create_user(data_app.USER1)
        pass
