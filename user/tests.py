from django.test import TestCase, Client
from .models import User


# Create your tests here.
class TestUser(TestCase):
    def test_get_index_page(self):
        client = Client()
        resp = client.get('/')
        self.assertEqual(resp.status_code, 200)
        # self.assertNotContains(resp.session, "sessionid")

    def test_get_login_page(self):
        client = Client()
        resp = client.get("/user/login/")
        self.assertEqual(resp.status_code, 200)



