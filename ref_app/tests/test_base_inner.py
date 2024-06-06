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
        err, referrer = utils.get_referrer_by_ref_code(user1.profile.ref_code)
        self.assertFalse(err)
        self.assertEqual(user1, referrer)
    
    def test_create_referral_obj(self):
        err, user1 = utils.create_user(data_app.USER1)
        err, ref_code = utils.get_ref_code_by_user(user1)
        err, user2 = utils.create_user((*data_app.USER2, ref_code))
        self.assertFalse(err)
        self.assertEqual(f'refs {user1.username} >> {user2.username}', str(user2.referral))
        self.assertEqual(user2.referral.num_purchases, 0)
        self.assertEqual(user2.referral.total_amount, 0)
        all_referral_obj = utils.get_all_referral_from_db()
        self.assertEqual(all_referral_obj.count(), 1)
        self.assertIn(f'refs {user1.username} >> {user2.username}', str(all_referral_obj))
    
    def test_can_create_2_referral_obj(self):
        err, user1 = utils.create_user(data_app.USER1)
        err, ref_code = utils.get_ref_code_by_user(user1)
        err, user2 = utils.create_user((*data_app.USER2, ref_code))
        err, user3 = utils.create_user((*data_app.USER3, ''))
        err, ref_code = utils.get_ref_code_by_user(user3)
        err, user4 = utils.create_user((*data_app.USER4, ref_code))
        self.assertFalse(err)
        self.assertEqual(f'refs {user3.username} >> {user4.username}', str(user4.referral))
        self.assertEqual(user4.referral.num_purchases, 0)
        self.assertEqual(user4.referral.total_amount, 0)
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
    
    def test_get_user_by_id(self):
        s, user1 = utils.create_user(data_app.USER1)
        err, user_from_db = utils.get_user_by_id(user1.id)
        self.assertFalse(err)
        self.assertEqual(user1, user_from_db)
    
    def test_user_is_referrer(self):
        err, user1 = utils.create_user(data_app.USER1)
        err, ref_code = utils.get_ref_code_by_user(user1)
        err, user2 = utils.create_user((*data_app.USER2, ref_code))
        err, user_from_db = utils.get_user_by_id(user1.id)
        err, resp = utils.user_is_referrer(user_from_db)
        self.assertFalse(err)
    
    def test_user_is_referral(self):
        err, user1 = utils.create_user(data_app.USER1)
        err, ref_code = utils.get_ref_code_by_user(user1)
        err, user2 = utils.create_user((*data_app.USER2, ref_code))
        err, user_from_db = utils.get_user_by_id(user2.id)
        err, resp = utils.user_is_referral(user_from_db)
        self.assertFalse(err)
    
    def test_can_get_ref_code_by_user(self):
        err, user1 = utils.create_user(data_app.USER1)
        err, resp = utils.get_ref_code_by_user(user1)
        self.assertFalse(err)
        self.assertEqual(user1.profile.ref_code, resp)
    
    def test_can_create_user_with_ref_code(self):
        err, user1 = utils.create_user(data_app.USER1)
        err, ref_code = utils.get_ref_code_by_user(user1)
        err, user2 = utils.create_user((*data_app.USER2, ref_code))
        self.assertFalse(err)
        self.assertEqual(user2.referral.referrer, user1)
        all_referral_obj = utils.get_all_referral_from_db()
        self.assertEqual(all_referral_obj.count(), 1)
        err, user3 = utils.create_user((*data_app.USER3, ref_code))
        all_referral_obj = utils.get_all_referral_from_db()
        self.assertEqual(all_referral_obj.count(), 2)
    
    def test_can_get_referrals_by_user(self):
        err, user1 = utils.create_user(data_app.USER1)
        err, refs = utils.get_referrals_by_user(user1)
        # list of referrals is empty
        self.assertTrue(err)
        err, ref_code = utils.get_ref_code_by_user(user1)
        err, user2 = utils.create_user((*data_app.USER2, ref_code))
        err, refs = utils.get_referrals_by_user(user1)
        self.assertFalse(err)
        self.assertEqual(refs.count(), 1)
        err, user3 = utils.create_user((*data_app.USER3, ref_code))
        err, refs = utils.get_referrals_by_user(user1)
        self.assertFalse(err)
        self.assertEqual(refs.count(), 2)
    
    def test_get_money_is_work(self):
        err, user1 = utils.create_user(data_app.USER1)
        self.assertFalse(err)
        err, resp = utils.get_money(user1)
        self.assertFalse(err)
        self.assertEqual(data_app.BONUS9999, user1.profile.balance)

    def test_can_buy_item(self):
        err, user1 = utils.create_user(data_app.USER1)
        err, user1 = utils.get_money(user1)
        err, resp = utils.buy_item(user1, data_app.REQ_BUY1)
        self.assertFalse(err)
        self.assertEqual(user1.profile.balance, data_app.BONUS9999 - data_app.REQ_BUY1)
    
    def test_cant_buy_item(self):
        err, user1 = utils.create_user(data_app.USER1)
        err, resp = utils.buy_item(user1, data_app.REQ_BUY1)
        self.assertTrue(err)
        self.assertEqual(user1.profile.balance, 0)
    
    def test_can_track_referral_purchases(self):
        err, user1 = utils.create_user(data_app.USER1)
        err, ref_code = utils.get_ref_code_by_user(user1)
        err, user2 = utils.create_user((*data_app.USER2, ref_code))
        err, resp = utils.get_money(user2)
        err, resp = utils.buy_item(user2, data_app.REQ_BUY1)
        self.assertEqual(user2.referral.total_amount, data_app.REQ_BUY1)
        self.assertEqual(user2.referral.num_purchases, 1)
        err, resp = utils.buy_item(user2, data_app.REQ_BUY2)
        self.assertEqual(user2.referral.total_amount, data_app.REQ_BUY1 + data_app.REQ_BUY2)
        self.assertEqual(user2.referral.num_purchases, 2)
        err, resp = utils.buy_item(user2, data_app.REQ_BUY5)
        self.assertEqual(user2.referral.total_amount, data_app.REQ_BUY1 + data_app.REQ_BUY2 + data_app.REQ_BUY5)
        self.assertEqual(user2.referral.num_purchases, 3)
        err, user3 = utils.create_user((*data_app.USER3, ref_code))
        err, resp = utils.get_money(user3)
        err, resp = utils.buy_item(user3, data_app.REQ_BUY1)
        self.assertEqual(user3.referral.total_amount, data_app.REQ_BUY1)
        self.assertEqual(user3.referral.num_purchases, 1)
        err, resp = utils.buy_item(user3, data_app.REQ_BUY2)
        self.assertEqual(user3.referral.total_amount, data_app.REQ_BUY1 + data_app.REQ_BUY2)
        self.assertEqual(user3.referral.num_purchases, 2)
        err, resp = utils.buy_item(user3, data_app.REQ_BUY5)
        self.assertEqual(user3.referral.total_amount, data_app.REQ_BUY1 + data_app.REQ_BUY2 + data_app.REQ_BUY5)
        self.assertEqual(user3.referral.num_purchases, 3)