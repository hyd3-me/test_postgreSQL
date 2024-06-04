from django.test import TestCase, TransactionTestCase
from django.http import HttpRequest
from django.utils import timezone
# from unittest import skip
from datetime import timedelta

#from noteqq import test_data
from ref_app import utils
from ref_app import data_app


class UserTest(TestCase):

    def test_create_user(self):
        err, user1 = utils.create_user(data_app.USER1)
        self.assertFalse(err)
        self.assertEqual(user1.username, data_app.USER1[0])
