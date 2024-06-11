from django.urls import reverse

from ref_app.tests.test_base_http import BaseUser
from ref_app import utils, data_app, forms


def create_ref_link(ref_code):
    domain = 'localhost'
    return f'http://{domain}:8000{reverse(data_app.REG_PATH)}?ref={ref_code}'

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
        err, user = utils.get_first_user()
        self.assertFalse(err)
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
    
    def test_use_template_for_profile_page(self):
        resp = self.client.get(reverse(data_app.PROFILE_PATH))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'profile.html')
    
    def test_has_link_to_store_page(self):
        resp = self.client.get(reverse(data_app.PROFILE_PATH))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, '<a href="/store/">store</a>', html=True)
    
    def test_use_template_for_store_page(self):
        resp = self.client.get(reverse(data_app.STORE_PATH))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'store.html')
    
    def test_can_buy_item1(self):
        err, user = self.make_user_and_login()
        s, resp1 = utils.get_money(user)
        resp1 = self.client.post(reverse('post_buy'), {
            'id': 1}, follow=True)
        self.assertRedirects(resp1, reverse(data_app.HOME_PATH))
        s, balance1 = utils.get_balance_by_user(user)
        self.assertEqual(balance1, data_app.BONUS9999-data_app.REQ_BUY1)
    
    def test_can_get_ref_code_link(self):
        s, user1 = utils.create_user(data_app.USER1)
        err, ref_code = utils.get_ref_code(user1)
        ref_link = create_ref_link(ref_code)
        resp = self.client.get(ref_link)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, ref_code)
    
    def test_use_registration_form(self):
        s, user1 = utils.create_user(data_app.USER1)
        err, ref_code = utils.get_ref_code(user1)
        ref_link = create_ref_link(ref_code)
        resp = self.client.get(ref_link)
        self.assertIsInstance(resp.context['form'], forms.RegistrationForm)
    
    def test_can_reg_with_ref_code(self):
        s, user1 = utils.create_user(data_app.USER1)
        ref_code = utils.get_ref_code(user1)
        ref_link = create_ref_link(ref_code)
        user_tuple = data_app.USER2
        resp1 = self.client.post(ref_link, {
            'username': user_tuple[0],
            'password': user_tuple[1],
            'ref_code': ref_code}, follow=True)
        self.assertRedirects(resp1, reverse(data_app.PROFILE_PATH))
        err, user = utils.get_last_user()
        self.assertEqual(user.username, user_tuple[0])
        err, user_from_db = utils.get_user_by_id(user1.id)
        self.assertTrue(user_from_db.profile.is_referrer)
    
    def test_has_link_to_give_money_page(self):
        resp = self.client.get(reverse(data_app.STORE_PATH))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, '<a href="/give_money/">give_money</a>', html=True)
    
    def test_give_money(self):
        err, user = self.make_user_and_login()
        resp = self.client.get(reverse(data_app.GIVE_MONEY_PATH), follow=True)
        self.assertRedirects(resp, reverse(data_app.STORE_PATH))
        s, balance = utils.get_balance_by_user(user)
        self.assertContains(
            resp, f'<p>my balance: {balance:.2f}</p>', html=True)
    
    def test_referrer_can_get_bonus(self):
        s, user1 = utils.create_user(data_app.USER1)
        ref_code = utils.get_ref_code(user1)
        ref_link = create_ref_link(ref_code)
        user_tuple = data_app.USER2
        resp1 = self.client.post(ref_link, {
            'username': user_tuple[0],
            'password': user_tuple[1],
            'ref_code': ref_code}, follow=True)
        resp = self.client.get(reverse(data_app.GIVE_MONEY_PATH), follow=True)
        resp1 = self.client.post(reverse('post_buy'), {
            'id': data_app.GOOD1.get('id')}, follow=True)
        percent5 = 0.05 * data_app.REQ_BUY1
        s, balance1 = utils.get_balance_by_user(user1)
        self.assertEqual(balance1, percent5)
    
    def test_has_link_to_all_refs_page(self):
        resp = self.client.get(reverse(data_app.PROFILE_PATH))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, '<a href="/all_refs/">all refs</a>', html=True)
    
    def test_use_template_for_all_refs_page(self):
        resp = self.client.get(reverse(data_app.ALL_REFS_PATH))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'all_refs.html')