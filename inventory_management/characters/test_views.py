from __future__ import absolute_import

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import Client
from django.test import TestCase

from .models import Character


class CharacterViewsTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user',
            password='test_user_password',
        )

        self.char_1 = Character.objects.create(
            user=self.user,
            name='Test Character 1',
            char_id=123456,
            key_id=67890,
            v_code='testv_code123',
        )

        self.char_2 = Character.objects.create(
            user=self.user,
            name='Test Character 2',
            char_id=654321,
            key_id=9876,
            v_code='testv_code321',
        )

        self.client = Client()

    def test_character_list_view_returns_correct_number_of_characters(self):
        self.client.login(
            username=self.user.username,
            password='test_user_password'
        )
        uri = reverse('characters:list')
        response = self.client.get(uri)
        character_list_len = len(response.context['characters'])
        self.assertEqual(character_list_len, 2)

    def test_login_view(self):
        uri = reverse('login')
        response = self.client.post(
            uri,
            {'username': 'test_user', 'password': 'test_user_password'},
            follow=True
        )
        self.assertContains(response, '<p>test_user</p>')

    def test_logout_view(self):
        self.client.login(
            username=self.user.username,
            password='test_user_password'
        )
        # Test to see if index page shows logged-in user's username
        uri = reverse('index')
        response = self.client.get(uri)
        self.assertContains(response, '<h1>Index</h1>')
        self.assertContains(response, '<p>test_user</p>')

        # Log-out user, test for no username on index page
        uri = reverse('logout')
        response = self.client.get(
            uri,
            follow=True
        )
        self.assertContains(response, '<h1>Index</h1>')
        self.assertNotContains(response, '<p>test_user</p>')
