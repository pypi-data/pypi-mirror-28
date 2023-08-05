from unittest.mock import Mock

from django.test import TestCase

from paypal.models import PaypalPayment
from paypal.signals import payment_succeed


class PaypalPaymentTest(TestCase):
    def test_add_item(self):
        pp = PaypalPayment()

        pp.add_item('simple', 'USD', 0.233)
        pp.add_item('hello', 'USD', 1.01,
                    quantity=3,
                    sku='HL',
                    description='test item',
                    tax=0.07)
        self.assertEqual(pp.currency, 'USD')
        self.assertEqual(str(pp.amount_total), '3.33')
        self.assertEqual(pp.amount_details['subtotal'], '3.26')
        self.assertEqual(pp.amount_details['tax'], '0.07')

    def test_signal_payment_succeed(self):
        pp = PaypalPayment()
        pp.add_item('simple', 'USD', 0.233)
        pp.save()

        mock = Mock()
        payment_succeed.connect(mock)

        pp.state = PaypalPayment.STATE_APPROVED
        pp.save()
        self.assertEqual(mock.call_count, 1)

        pp.save()
        self.assertEqual(mock.call_count, 1, '只有切换到APPROVED的时候才抛signal')
