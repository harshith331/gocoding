from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.utils.translation import get_language
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
import razorpay
import json

from . import Checksum

from paytm.models import PaytmHistory
# Create your views here.

razorpay_client = razorpay.Client(
    auth=("rzp_test_igH2yh6dAH6ZYY", "KLQIH1VDQikVYMTishkW37yI"))


@login_required
def home(request):
    return HttpResponse("<html><a href='" + settings.HOST_URL + "/paytm/payment'>PayNow</html>")


def payment(request):
    MERCHANT_KEY = settings.PAYTM_MERCHANT_KEY
    MERCHANT_ID = settings.PAYTM_MERCHANT_ID
    get_lang = "/" + get_language() if get_language() else ''
    CALLBACK_URL = settings.HOST_URL + settings.PAYTM_CALLBACK_URL
    # Generating unique temporary ids
    order_id = Checksum.__id_generator__()
    phone_no = request.POST['phone_no']
    user = RegUser.objects.filter(phone_no=phone_no)
    amount = request.POST['amount']
    # address = request.POST.get['address1']
    # city = request.POST.get('city', '')
    # state = request.POST.get('state', '')
    # zip_code = request.POST.get('zip_code', '')
    # bill_amount = request.POST["TXN_AMOUNT"]
    # bill_amount = request.POST["order_id"]
    if bill_amount:
        data_dict = {
            'MID': MERCHANT_ID,
            'ORDER_ID': order_id,
            'TXN_AMOUNT': str(amount),
            'CUST_ID': phone_no,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': settings.PAYTM_WEBSITE,
            'CHANNEL_ID': 'WAP',
            'EMAIL': user.email,  # customer email id
            'MOBILE_NO': phone_no,  # customer 10 digit mobile no.
            'CALLBACK_URL': CALLBACK_URL,
        }
        param_dict = data_dict
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(
            data_dict, MERCHANT_KEY)
        return JsonResponse(param_dict)
    return HttpResponse("Bill Amount Could not find. ?bill_amount=10")


@csrf_exempt
def response(request):
    if request.method == "POST":
        MERCHANT_KEY = settings.PAYTM_MERCHANT_KEY
        data_dict = {}
        for key in request.POST:
            data_dict[key] = request.POST[key]

        print(data_dict)
        verify = Checksum.verify_checksum(
            data_dict, MERCHANT_KEY, data_dict['CHECKSUMHASH'])
        if verify:
            # PaytmHistory.objects.create(user=request.user, **data_dict)
            # return render(request,"response.html",{"paytm":data_dict})
            return JsonResponse(data_dict)
        else:
            return HttpResponse("checksum verify failed")
    return HttpResponse(status=200)


def app_charge(request):
    if request.method == "POST":
        amount = request.POST["TXN_AMOUNT"]
        order_currency = 'INR'
        amount = amount*100
        pay_details = razorpay_client.order.create(
            amount=amount, currency=order_currency, payment_capture='0')
        return json.dumps(pay_details)


def razor_final(request):
    if request.method == "POST":
        order_id = request.POST["order_id"]
        payment_id = request.POST["razorpay_payment_id"]
        razorpay_order_id = request.POST["razorpay_order_id"]
        razorpay_signature = request.POST["razorpay_signature"]
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': razorpay_signature
        }
        res = client.utility.verify_payment_signature(params_dict)
        if res:
            RazorPay.objects.create(
                ORDERID=order_id,
                razorpay_order_id=razorpay_order_id,
                razorpay_payment_id=payment_id
            )
            return JsonResponse({'msg': 'success'})
        else:
            return JsonResponse({'msg': 'payment unsuccessful'})
