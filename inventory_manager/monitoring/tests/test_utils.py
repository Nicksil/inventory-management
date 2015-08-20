from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from model_mommy import mommy

from characters.models import Order


class TestMonitoringUtils(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user_attribs = mommy.prepare('User')
        cls.user = User.objects.create_user(
            username=cls.user_attribs.username,
            password=cls.user_attribs.password)

        cls.char = mommy.make('Character', user=cls.user)
        cls.order_1 = mommy.make(
            'Order',
            character=cls.char,
            vol_remaining=10,
            qty_threshold=15)
        cls.order_2 = mommy.make(
            'Order',
            character=cls.char,
            vol_remaining=20,
            qty_threshold=15)

    def test_check_qty_threshold(self):
        self.client.login(
            username=self.user.username, password=self.user_attribs.password)

        uri = reverse('monitoring:check_qty_threshold', kwargs={'pk': self.char.pk})
        response = self.client.get(uri, follow=True)

        message_text = 'The following orders have quantities at or below their quantity threshold: {}'.format(
            self.order_1.item.type_name)
        self.assertContains(response, message_text)

        expected_redirect_uri = reverse('characters:order_list', kwargs={'pk': self.char.pk})
        self.assertRedirects(response, expected_redirect_uri)

        # Now check as if no orders have met threshold
        update_order = Order.objects.get(pk=self.order_1.pk)
        update_order.vol_remaining = 20
        update_order.save()

        uri = reverse('monitoring:check_qty_threshold', kwargs={'pk': self.char.pk})
        response = self.client.get(uri, follow=True)

        message_text = 'The following orders have quantities at or below their quantity threshold: {}'.format(
            self.order_1.item.type_name)
        self.assertNotContains(response, message_text)

        expected_redirect_uri = reverse('characters:order_list', kwargs={'pk': self.char.pk})
        self.assertRedirects(response, expected_redirect_uri)
