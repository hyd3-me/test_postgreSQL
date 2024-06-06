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
        err, user2 = utils.create_user(data_app.USER2)
        err, resp = utils.create_referral_obj((user1, user2))
        self.assertFalse(err)
        self.assertEqual(f'refs {user1.username} >> {user2.username}', str(resp))
        self.assertEqual(resp.num_purchases, 0)
        self.assertEqual(resp.total_amount, 0)
        all_referral_obj = utils.get_all_referral_from_db()
        self.assertEqual(all_referral_obj.count(), 1)
        self.assertIn(f'refs {user1.username} >> {user2.username}', str(all_referral_obj))
    
    def test_can_create_2_referral_obj(self):
        err, user1 = utils.create_user(data_app.USER1)
        err, user2 = utils.create_user(data_app.USER2)
        err, resp = utils.create_referral_obj((user1, user2))
        err, user3 = utils.create_user(data_app.USER3)
        err, user4 = utils.create_user(data_app.USER4)
        err, resp = utils.create_referral_obj((user3, user4))
        self.assertFalse(err)
        self.assertEqual(f'refs {user3.username} >> {user4.username}', str(resp))
        self.assertEqual(resp.num_purchases, 0)
        self.assertEqual(resp.total_amount, 0)
        all_referral_obj = utils.get_all_referral_from_db()
        self.assertEqual(all_referral_obj.count(), 2)
        self.assertIn(f'refs {user1.username} >> {user2.username}', str(all_referral_obj))
        self.assertIn(f'refs {user3.username} >> {user4.username}', str(all_referral_obj))
    
    def test_cant_craete_referral_obj_to_same_referral(self):
        err, user1 = utils.create_user(data_app.USER1)
        err, user2 = utils.create_user(data_app.USER2)
        err, resp = utils.create_referral_obj((user1, user2))
        err, user3 = utils.create_user(data_app.USER3)
        err, resp = utils.create_referral_obj((user3, user2))
        self.assertTrue(err)
        # print(resp)
    
    def test_get_user_by_id(self):
        s, user1 = utils.create_user(data_app.USER1)
        err, user_from_db = utils.get_user_by_id(user1.id)
        self.assertFalse(err)
        self.assertEqual(user1, user_from_db)
    
    def test_user_is_referrer(self):
        err, user1 = utils.create_user(data_app.USER1)
        err, user2 = utils.create_user(data_app.USER2)
        err, resp = utils.create_referral_obj((user1, user2))
        err, user_from_db = utils.get_user_by_id(user1.id)
        self.assertTrue(user_from_db.profile.is_referrer)
    
    def test_user_is_referral(self):
        err, user1 = utils.create_user(data_app.USER1)
        err, user2 = utils.create_user(data_app.USER2)
        err, resp = utils.create_referral_obj((user1, user2))
        err, user_from_db = utils.get_user_by_id(user2.id)
        self.assertTrue(user_from_db.profile.is_referral)
    
    def test_can_get_ref_code_by_user(self):
        err, user1 = utils.create_user(data_app.USER1)
        err, resp = utils.get_ref_code_by_user(user1)
        self.assertFalse(err)
        self.assertEqual(user1.profile.ref_code, resp)
