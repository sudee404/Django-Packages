from django.test import TestCase, Client
from django.urls import reverse
from .models import MyUser


class MyUserModelTest(TestCase):
    def setUp(self):
        self.user = MyUser.objects.create_user(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='testpassword',
        )

    def test_user_creation(self):
        self.assertEqual(MyUser.objects.count(), 1)
        self.assertEqual(MyUser.objects.get(
            email='test@example.com').first_name, 'Test')

    def test_user_password(self):
        self.assertTrue(self.user.check_password('testpassword'))
        self.assertFalse(self.user.check_password('wrongpassword'))


class MyUserViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = MyUser.objects.create_user(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='testpassword',
        )

    def test_login(self):
        response = self.client.post(reverse('login'), {
            'email': 'test@example.com',
            'password': 'testpassword',
        })
        self.assertEqual(response.status_code, 302)
        # self.assertRedirects(response, reverse('login'))

    def test_login_fail(self):
        response = self.client.post(reverse('login'), {
            'email': 'test@example.com',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid email or password")

    def test_register(self):

        response = self.client.post(reverse('register'), {
            'email': 'test2@example.com',
            'first_name': 'Test2',
            'last_name': 'User2',
            'password': 'testpassword2',
            'password2': 'testpassword2',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(MyUser.objects.count(), 2)
        new_user = MyUser.objects.get(email='test2@example.com')
        self.assertEqual(new_user.first_name, 'Test2')
        self.assertEqual(new_user.last_name, 'User2')
        self.assertTrue(new_user.check_password('testpassword2'))
