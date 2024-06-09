from django.urls import reverse

from ref_app.tests.test_base_http import BaseUser
from ref_app import utils, data_app

class UserTest(BaseUser):

    def test_redirect_unauth_user_to_login_from_index(self):
        resp = self.client.get(reverse(data_app.HOME_PATH))
        self.assertRedirects(resp, reverse(data_app.LOGIN_PATH))
    
    def test_use_template_for_login_page(self):
        resp = self.client.get(reverse(data_app.LOGIN_PATH))
        self.assertTemplateUsed(resp, 'login.html')
    
    def test_has_link_to_register_new_user(self):
        resp = self.client.get(reverse(data_app.LOGIN_PATH))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, '<a href="/register">+new user</a>', html=True)
    
    def test_can_register_new_user(self):
        resp = self.reg_me(data_app.USER1)
        err, user = utils.get_user_by_id(1)
        self.assertEqual(user.username, data_app.USER1[0])
    
    def test_use_template_for_index_page(self):
        err, user = self.make_user_and_login()
        resp = self.client.get(reverse(data_app.HOME_PATH))
        self.assertTemplateUsed(resp, 'index.html')
    
    def test_use_template_for_register_page(self):
        resp = self.client.get(reverse(data_app.REG_PATH))
        self.assertTemplateUsed(resp, 'register.html')
    
    def test_redirect_after_registration_to_profile_page(self):
        resp = self.reg_me(data_app.USER1)
        self.assertRedirects(resp, reverse(data_app.PROFILE_PATH))
    