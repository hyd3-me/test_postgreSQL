from django.test import TestCase
from django.urls import reverse
# from unittest import skip
# from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from ref_app import utils, data_app

class BaseUser(TestCase):

    def reg_me(self, user_tuple=data_app.USER1):
        resp1 = self.client.post(reverse(data_app.REG_PATH), {
            'username': user_tuple[0],
            'password':user_tuple[1]}, follow=True)
        return resp1

    def login(self, user_tuple=data_app.USER1):
        resp1 = self.client.post(reverse(data_app.LOGIN_PATH), {
            'username': user_tuple[0],
            'password': user_tuple[1]}, follow=True)
        return resp1

    def logout(self):
        resp1 = self.client.get(reverse(data_app.LOGOUT_PATH), follow=True)
        return resp1

    def make_user_and_login(self, user_tuple=data_app.USER1, p_login=True):
        s, user1 = utils.create_user(user_tuple)
        if p_login: resp1 = self.login(user_tuple)
        return 0, user1