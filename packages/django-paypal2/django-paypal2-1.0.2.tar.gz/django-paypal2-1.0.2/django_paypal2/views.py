import random

from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from paypal.models import PaypalPayment


@csrf_exempt
def sample_pay_view(request):
    if request.method == 'GET':
        return render(request, 'sample_pay.html')
    elif request.method == 'POST':
        pp = PaypalPayment(
            description="sample pay",
        )
        pp.add_item("sample", 'USD', float(request.POST['amount']))
        pp.reference_id = str(random.randint(10000, 99999))
        pp.save()
        return redirect('paypal_redirect', uid=pp.uid)
