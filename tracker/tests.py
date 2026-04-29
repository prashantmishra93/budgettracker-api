from django.test import TestCase
from .views.registerView import RegisterView

# Create your tests here.

class APITest(TestCase):
    def test_register_api(self):
        response = self.client.post('/api/register', {
            'username': "anoop",
            "email": "anoop@gmail.com",
            "password":"anoop123"
        })
        self.assertEqual(response.status_code, 201)
