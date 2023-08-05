from django.test import RequestFactory, TestCase

from paypal.models import PaypalPayment
from paypal.views import PaypalRedirectView


class PaypalRedirectViewTest(TestCase):
    def test_create(self):
        pp = PaypalPayment(description="hello")
        pp.add_item("vpn", 'USD', 1.11)
        pp.save()

        view = PaypalRedirectView.as_view()
        factory = RequestFactory()
        req = factory.get('/')

        resp = view(req, uid=pp.uid)
        self.assertTrue('paypal' in resp.url, '跳转到paypal')