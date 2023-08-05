from django.contrib import admin

from paypal.admin import PaypalPaymentAdmin
from paypal.models import PaypalPayment

admin.site.register(PaypalPayment, PaypalPaymentAdmin)
