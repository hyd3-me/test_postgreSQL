from django.urls import reverse

from ref_app.tests.test_base_http import BaseUser
from ref_app import utils, data_app

class UserTest(BaseUser):

    def est_use_template_to_index(self):
        resp = self.client.get(reverse(data_app.HOME_PATH))
        self.assertTemplateUsed(resp1, 'index.html')
    
    def test_redirect_unauth_user_to_login(self):
        resp = self.client.get(reverse(data_app.HOME_PATH))
        self.assertRedirects(resp, reverse(data_app.LOGIN_PATH))
