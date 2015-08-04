# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from .models import Character


class CharactersAppViewsTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user_1 = User.objects.create_user(
            'test_user',
            'test_user@elohel.biz',
            'mah_test_password'
        )
        cls.character_1 = Character.objects.create(
            user=cls.user_1,
            name='Test Character 1',
            char_id=12345,
            key_id=98765,
            v_code='heres_a_v_code_123',
        )

    # def setUp(self):
    #     self.user_1 = User.objects.create_user(
    #         'test_user',
    #         'test_user@elohel.biz',
    #         'mah_test_password'
    #     )
    #     self.character_1 = Character.objects.create(
    #         user=self.user_1,
    #         name='Test Character 1',
    #         char_id=12345,
    #         key_id=98765,
    #         v_code='heres_a_v_code_123',
    #     )

    def test_character_add_view_renders_correct_template(self):
        uri = reverse('characters:add')
        response = self.client.get(uri)

        self.assertTemplateUsed(response, 'characters/character_add_form.html')

    def test_character_add_view_returns_200_as_status_code(self):
        uri = reverse('characters:add')
        response = self.client.get(uri)
        status_code = response.status_code

        self.assertEqual(200, status_code)

    def test_character_list_view_renders_correct_template(self):
        self.client.login(username='test_user', password='mah_test_password')

        uri = reverse('characters:list')
        response = self.client.get(uri)

        self.assertTemplateUsed(response, 'characters/character_list_view.html')

    def test_character_list_view_returns_200_as_status_code(self):
        self.client.login(username='test_user', password='mah_test_password')

        uri = reverse('characters:list')
        response = self.client.get(uri)
        status_code = response.status_code

        self.assertEqual(200, status_code)

    def test_character_detail_view_renders_correct_template(self):
        self.client.login(username='test_user', password='mah_test_password')

        uri = reverse('characters:detail', kwargs={'pk': self.character_1.pk})
        response = self.client.get(uri)

        self.assertTemplateUsed(response, 'characters/character_detail_view.html')

    def test_character_detail_view_returns_200_as_status_code(self):
        self.client.login(username='test_user', password='mah_test_password')

        uri = reverse('characters:detail', kwargs={'pk': self.character_1.pk})
        response = self.client.get(uri)
        status_code = response.status_code

        self.assertEqual(200, status_code)

    def test_asset_list_view_renders_correct_template(self):
        self.client.login(username='test_user', password='mah_test_password')

        uri = reverse('characters:asset_list', kwargs={'pk': self.character_1.pk})
        response = self.client.get(uri)

        self.assertTemplateUsed(response, 'characters/asset_list_view.html')

    def test_asset_list_view_returns_200_as_status_code(self):
        self.client.login(username='test_user', password='mah_test_password')

        uri = reverse('characters:asset_list', kwargs={'pk': self.character_1.pk})
        response = self.client.get(uri)
        status_code = response.status_code

        self.assertEqual(200, status_code)

    def test_order_list_view_renders_correct_template(self):
        self.client.login(username='test_user', password='mah_test_password')

        uri = reverse('characters:order_list', kwargs={'pk': self.character_1.pk})
        response = self.client.get(uri)

        self.assertTemplateUsed(response, 'characters/orders_list_view.html')

    def test_order_list_view_returns_200_as_status_code(self):
        self.client.login(username='test_user', password='mah_test_password')

        uri = reverse('characters:order_list', kwargs={'pk': self.character_1.pk})
        response = self.client.get(uri)
        status_code = response.status_code

        self.assertEqual(200, status_code)
