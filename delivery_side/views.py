from django.shortcuts import render
from .models import *
from base_tech.models import *
from django.http import JsonResponse
from pusher import Pusher
from pusher_push_notifications import PushNotifications
from vendor_side.models import *
from fcm_django.models import FCMDevice
from django.utils.timezone import datetime

pusher = Pusher(app_id=u'884349', key=u'7c495f369f4053064877',
                secret=u'1f0f6089002fcb5d3ce1', cluster=u'ap2', ssl=True)
beams_client = PushNotifications(
    instance_id='b0f7aac1-2560-466f-a93d-aa258d520a5a',
    secret_key='19BC4395F6CB9B17AEE81191B4B03668DDE8850EF5E76BCDBE46BBC0B6BC7DB3',
)

# Create your views here.


def beams_auth(request):
    # Do your normal auth checks here 🔒
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    phone_no = body['phone_no']  # get it from your auth system
#   user_id_in_query_param = request.args.get('user_id')
#   if user_id != user_id_in_query_param:
#     return 'Inconsistent request', 401
    beams_token = beams_client.generate_token(phone_no)
    print(beams_token)
    return JsonResponse(beams_token)


def delivery_register(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        Delivery_Boys.objects.create(
            name=body['name'],
            phone_no=body['phone_no'],
            del_boy_id=body['del_boy_id'],
            address=body['address'],
            status='A',
            city=body['city'],
            total_no_orders=0,
            current_no_orders=0,
            busy=False
        )
        data = {
            "customer_phone": body['name']
        }
        response = beams_client.publish_to_users(
            user_ids=["1"],
            publish_body={
                'fcm': data
            },
        )
        return JsonResponse({'msg': 'success'})
    response = {
        'error': 'Invalid'
    }
    return JsonResponse(response)


def check_delivery_boy(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        try:
            obj = Delivery_Boys.objects.get(
                del_boy_id=body['del_boy_id'])
            response = {
                'del_boy_phone': obj.phone_no,
                'del_boy_name': obj.name,
                'del_boy_id': body['del_boy_id'],
                'delivery_imagepath': obj.delivery_imagepath.url,
                'found': 'true'
            }
        except:
            response = {
                'del_boy_phone': '',
                'del_boy_name': '',
                'del_boy_id': body['del_boy_id'],
                'found': 'false'
            }
        return JsonResponse(response)
    response = {
        'error': 'Invalid'
    }
    return JsonResponse(response)


def activate_delboy(request):
    if request.method == 'POST':
        try:
            obj = Delivery_Boys.objects.get(phone_no=request.POST['delboy_phone'])
            if request.POST['status'] == 'active':
                obj.status = 'A'
                obj.save()
            else:
                obj.status = 'I'
                obj.save()
            response = {
                'delboy_phone': request.POST['delboy_phone'],
                'success': 'true',
                'delboy_city': obj.city,
                'delboy_address': obj.address
            }
            return JsonResponse(response)
        except:
            response = {
                'delboy_phone': request.POST['delboy_phone'],
                'success': 'false'
            }
    return JsonResponse(response)


# def order_confirm(request, phone):
#     if request.method == 'POST':
#         if request.POST['accepted'] == 'true':
#             DeliveryBoyOrders.create(
#                 del_boy_no=Delivery_Boys.objects.get(
#                     phone_no=request.POST['del_boy_no']),
#                 order_id=request.POST['order_id'],
#                 accepted=True
#             )
#
#         else:
#             DeliveryBoyOrders.create(
#                 del_boy_no=Delivery_Boys.objects.get(
#                     phone_no=request.POST['del_boy_no']),
#                 order_id=request.POST['order_id'],
#                 accepted=False
#             )
#         response = {'success': 'true'}
#         return JsonResponse(response)
#     response = {'success': 'false'}
#     return JsonResponse(response)


def unique(list1):
    # intilize a null list
    unique_list = []

    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
    # print list
    return unique_list


def send_delivery_order(data, phone_no):
    print(data)
   # delivery = 'delivery'
   # phone = str(phone_no)
    # channel_name = 'delivery'+phone_no
    # print("pusher request", channel_name)
    # response = beams_client.publish_to_users(
    #     user_ids=[phone_no],
    #     publish_body={
    #         'fcm': data
    #     },
    # )
    delboy = Delivery_Boys.objects.get(phone_no=phone_no)
    fcm_token = delboy.delboy_fcm_token
    cells = data["val_cell"]
    cells = unique(cells)
    cell_data= []
    for cell in cells:
        cell_data.append({
            "cell_lat": cell.Cell_lat,
            "cell_long": cell.Cell_long,
            "cell_city": cell.city
        })
    notification_data = {
        "order_id": data["order_id"],
        "cells": cell_data,
        "isprimary": data["isprimary"]
    }
    send_notification(fcm_token=fcm_token, data_content=notification_data)


def vendor_details(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        order_type = body['order_type']
        if order_type == 'O':

            order_id = body['order_id']
            del_phone = body['phone_no']
            myorder = Order_Items.objects.filter(
                order_id=order_id, delivery_boy_phone=del_phone)
            # vendor_phones =(myorder.vendor_phone)
            print("myorder", myorder)
            vendor_phones = []
            for order in myorder:
                vendor_phones.append(order.vendor_phone)
            print("vendor_phones", vendor_phones)
            vendor_phones = unique(vendor_phones)
            print("vendor_phones_unique", vendor_phones)
            details = []
            for vendor_phone in vendor_phones:
                d = {}
                ven_order = myorder.filter(vendor_phone=vendor_phone)
                print("ven_order", ven_order)
                products = []
                products_name = []
                var = 0
                for product in ven_order:
                    if product.delivery_status == 'P':
                        var += 1
                    print("product", product)
                    print("id", product.product_id)
                    products.append(product.product_id)
                    obj = CategorizedProducts.objects.filter(product_id=product.product_id)
                    print("obj", obj)
                    products_name.append(obj[0].product_name)
                ven_obj = Vendors.objects.get(phone_no=vendor_phone)
                is_picked = False
                if var != 0:
                    is_picked = True
                print("products", products)
                d["vendor_name"] = ven_obj.name
                d["vendor_address"] = ven_obj.address
                d["vendor_lat"] = ven_obj.vendor_lat
                d["vendor_long"] = ven_obj.vendor_long
                d["vendor_phone"] = vendor_phone
                d["vendor_cell_id"] = ven_obj.cell.Cell_id
                d["vendor_cell_lat"] = ven_obj.cell.Cell_lat
                d["vendor_cell_long"] = ven_obj.cell.Cell_long
                d["is_picked"] = is_picked
                # d["products_id"] = products
                # d["products_name"] = products_name
                print("d", d)
                details.append(d)
            dict = {"details": details}
            return JsonResponse(dict, safe=False)
        else:
            today = datetime.today()
            sorder_id = body['order_id']
            sorder_items = Subscribed_Order_Items.objects.filter(sorder_id=sorder_id)
            print(sorder_items)
            vendors = []
            for item in sorder_items:
                vendors.append(item.vendor_phone)
            print(vendors)
            details = []
            for ven_obj in vendors:
                vendor_subs = Vendors_subs.objects.get(order_date__year=today.year,
                                                       order_date__month=today.month,
                                                       order_date__day=today.day,
                                                       sorder_id=sorder_id)
                is_picked = vendor_subs.delivery_status
                if is_picked == 'N':
                    is_picked = False
                else:
                    is_picked = True
                d = {}
                d["vendor_name"] = ven_obj.name
                d["vendor_address"] = ven_obj.address
                d["vendor_lat"] = ven_obj.vendor_lat
                d["vendor_long"] = ven_obj.vendor_long
                d["vendor_phone"] = ven_obj.phone_no
                d['is_picked'] = is_picked
                d['vendor_cell_id'] = ven_obj.cell.Cell_id
                d['vendor_cell_lat'] = ven_obj.cell.Cell_lat
                d['vendor_cell_long'] = ven_obj.cell.Cell_long
                details.append(d)
            return JsonResponse({
                'details': details
            })


def cust_details(request):
    if request.method == 'POST':
        order_id = request.POST['order_id']
        del_phone = request.POST['phone_no']
        myorder = Orders.objects.filter(
            order_id=order_id, delivery_boy_phone=del_phone)
        address = myorder.address
        cust_lat = myorder.cust_lat
        cust_long = myorder.cust_long
        phone_no = myorder.customer_phone
        data = {
            "customer_phone": phone_no.phone_no,
            "cust_lat": cust_lat,
            "cust_long": cust_long,
            "address": address
        }
        print(data)
        return JsonResponse(data, safe=False)


def get_product_details(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        order_type = body['order_type']
        if order_type == 'O':
            order_id = body['order_id']
            otp = body['otp']
            order = Orders.objects.filter(order_id=order_id)[0]
            customer_phone = order.customer_phone
            orders = Order_Items.objects.filter(
                order_id=order.order_id).filter(otp=otp)
            data = []
            for ord in orders:
                obj = CategorizedProducts.objects.get(product_id=ord.product_id)
                d = {
                    'product_id': ord.product_id,
                    'quantity': ord.quantity,
                    'product_name': obj.product_name
                    #'vendor_phone': vendor_phone
                }
                data.append(d)
                print(data)

            response = {'data': data}
            return JsonResponse(response)
        else:
            body = json.loads(body_unicode)
            sorder_id = body['order_id']
            otp = body['otp']
            vendor_subs = Vendors_subs.objects.get(sorder_id=sorder_id, otp=otp)
            vendor = vendor_subs.phone_no
            order_items = Subscribed_Order_Items.objects.filter(sorder_id=sorder_id, vendor_phone=vendor)
            data = []
            for item in order_items:
                d = {}
                obj = CategorizedProducts.objects.get(product_id=item.product_id)
                d = {
                    'product_id': item.product_id,
                    'quantity': item.quantity,
                    'product_name': obj.product_name
                    # 'vendor_phone': vendor_phone
                }
                data.append(d)
            response = {'data': data}
            return JsonResponse(response)
    response = {'msg': 'error'}
    return JsonResponse(response)


def del_boy_details(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        isprimary = body['isprimary']
        del_phone = body['phone_no']
        order_id = body['order_id']
        # filter wrt order_id
        del_boy = Delivery_Boys.objects.get(phone_no=del_phone)
        myorder = Order_Items.objects.filter(order_id=order_id)
        print("myorder", myorder)
        if isprimary == "True":
            del_boy_list = []
            del_name_list = []
            for boy in myorder:
                del_boy_list.append(boy.delivery_boy_phone.phone_no)
                del_name_list.append(boy.delivery_boy_phone.name)

            print(del_boy_list)
            del_boy_list = unique(del_boy_list)
            del_name_list = unique(del_name_list)
            del_boy_list.remove(del_phone)
            del_name_list.remove(del_boy.name)
            print(del_name_list)

            dict = {
                "delivery_boy_phone": del_boy_list,
                "delivery_boy_names": del_name_list
            }
            return JsonResponse(dict, safe=False)

        else:
            primaryBoy = myorder.get(delboy_type="P")
            print(primaryBoy)
            dict = {
                "primary_boy": primaryBoy.delivery_boy_phone.phone_no,
                "primary_name": primaryBoy.delivery_boy_phone.name
            }
            return JsonResponse(dict, safe=False)


# def order_completed_delivery(request):
#     if request.method == 'POST':
#         body_unicode = request.body.decode('utf-8')
#         body = json.loads(body_unicode)
#         del_phone = body['phone_no']
#         order_id = body['order_id']
#         # filter wrt order_id
#         del_boy = Delivery_Boys.objects.get(phone_no=del_phone)
#         myorder = Order_Items.objects.filter(
#             order_id=order_id, delivery_boy_phone=del_phone)
#         del_boy.busy = False
#         del_boy.accepted_or_not = False
#         del_boy.save()
#         print("myorder", myorder)
#         return JsonResponse({'msg': 'success'})
#     return JsonResponse({'msg': 'fail'})


def order_delivered(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        if body['delivered'] == 'true':
            data = {
                'order_id': request.POST['order_id'],
                'status': 'delivered'
            }
            # pusher.trigger('my-channel', 'my-event', data)
            del_phone = body['phone_no']
            del_boy = Delivery_Boys.objects.get(phone_no=del_phone)
            del_boy.busy = False
            del_boy.accepted_or_not = False
            del_boy.save()
            customer_phone = Orders.models.filter(
                order_id=order_id).customer_phone
            response = beams_client.publish_to_users(
                user_ids=[customer_phone],
                publish_body={
                    'fcm': data
                },
            )
            response = {'success': 'true'}
            return JsonResponse(response)
        else:
            data = {
                'order_id': request.POST['order_id'],
                'status': 'could not be delivered'
            }
            # pusher.trigger('my-channel', 'my-event', data)
            customer_phone = Orders.models.filter(
                order_id=order_id).customer_phone
            response = beams_client.publish_to_users(
                user_ids=[customer_phone],
                publish_body={
                    'fcm': data
                },
            )
            response = {'success': 'true'}
            return JsonResponse(response)
    response = {'success': 'true'}
    return JsonResponse(response)


def reached_vendor(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        data = {
            'order_id': body['order_id'],
            'status': 'reached vendor'
        }
        # response = beams_client.publish_to_users(
        #     user_ids=[body['vendor_phone']],
        #     publish_body={
        #         'fcm': data
        #     },
        # )
        vendor_phone = body['vendor_phone']
        vendor = Vendors.objects.get(phone_no=vendor_phone)
        delboy_phone = body['delboy_phone']
        delboy = Delivery_Boys.objects.get(phone_no=delboy_phone)
        # obj = list(Order_Items.objects.filter(order_id=body['order_id']))
        # otp = obj[0].otp
        fcm_token = vendor.vendor_fcm_token
        notification_data = {
            'order_id': body['order_id'],
            'delboy_phone': delboy_phone,
            'delboy_name': delboy.name,
            #'otp': otp
        }
        send_notification(fcm_token=fcm_token, data_content=notification_data)

        print(response['publishId'])
        response = {
            'success': 'true',
        }
        return JsonResponse(response)
    response = {'success': 'true'}
    return JsonResponse(response)


def order_pickedup(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        order_id = body['order_id']
        vendor_phone = body['vendor_phone']
        data = {
            'order_id': body['order_id'],
            'status': 'pickedup'
        }

        # pusher.trigger('my-channel', 'my-event', data)
        obj = Order_Items.objects.filter(order_id=order_id, vendor_phone=vendor_phone)[0]
        order = Orders.objects.filter(order_id=order_id)[0]
        print(obj)
        print(order)
        print(order.primary_vendor)
        if order.primary_vendor.phone_no == vendor_phone and obj.delboy_type == 'P':
            print("both primary")
            customer_phone = Orders.objects.filter(order_id=order_id)[0].customer_phone
            print(customer_phone)

            fcm_token = customer_phone.customer_fcm_token
            send_notification(fcm_token=fcm_token, data_content=data)


        # response = beams_client.publish_to_users(
        #     user_ids=[customer_phone],
        #     publish_body={
        #         'fcm': data
        #     },
        # )
        response = {'success': 'true'}
        return JsonResponse(response)
    response = {'error': 'use post request'}
    return JsonResponse(response)


def reached_customer(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        delboy_no = body['phone_no']
        obj = DeliveryBoyOrders.objects.get(del_boy_no=delboy_no)
        obj.status = 'D'
        obj.save()
        data = {
            'order_id': body['order_id'],
            'status': 'reached customer'
        }
        # pusher.trigger('my-channel', 'my-event', data)
        order = Orders.models.get(order_id=order_id)
        customer_phone = order.customer_phone
        order.order_status = 'D'
        order.save()
        response = beams_client.publish_to_users(
            user_ids=[customer_phone],
            publish_body={
                'fcm': data
            },
        )

        fcm_token = Vendors.objects.get(phone_no=customer_phone)
        send_notification(fcm_token=fcm_token,
                          data_content={'reached': 'true'})

        response = {'success': 'true'}
        return JsonResponse(response)
    response = {'success': 'true'}
    return JsonResponse(response)


# def delivery_boy_reached_vendor(request):
#     if request.method == 'POST':
#         body_unicode = request.body.decode('utf-8')
#         body = json.loads(body_unicode)
#         del_phone = body['phone_no']
#         order_id = body['order_id']
#         del_phone = body['vendor_phone_no']
#         # filter wrt order_id
#         del_boy = Delivery_Boys.objects.get(phone_no=del_phone)
#         myorder = Order_Items.objects.filter(order_id=order_id)
#         return JsonResponse({'msg': 'success'})
#     return JsonResponse({'msg': 'fail'})


def get_deliver_order_history(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        phone_no = body['phone_no']
        orders = DeliveryBoyOrders.objects.filter(del_boy_no=phone_no)
        final = []
        obj_list = []
        no_orders = len(orders)
        for order in orders:
            orde = Orders.objects.get(order_id=cust_orders[i].order_id)
            ord = Order_Items.objects.filter(
                order_id=cust_orders[i].order_id, delivery_boy_phone=dboy)
            d = {}
            d["order_id"] = orde.order_id
            d["time"] = orde.order_time
            d["date"] = orde.order_date
            d["cust_lat"] = orde.cust_lat
            d["cust_long"] = orde.cust_long
            d["order_date"] = orde.order_date
            d["order_time"] = orde.order_time
            d["primary"] = ord.first().delboy_type
            for ob in ord:
                obj = Vendors.objects.get(
                    phone_no=ob.vendor_phone)
                prod = {
                    'vendor_lat': obj.vendor_lat,
                    'vendor_long': obj.vendor_long,
                    'address': obj.address,
                    'name': obj.name
                }
                obj_list.append(prod)
            obj_list = unique(obj_list)
            d['items'] = obj_list
            final.append(d)

        data = {
            'no_orders': no_orders,
            'locations': final
        }
        return JsonResponse(data)


def send_notification(fcm_token, data_content):
    print("sending notification")
    device = FCMDevice.objects.create(
        registration_id=fcm_token, type='android')
    device.send_message(data=data_content)


def secondary_reached_checkpoint(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        order_id = body['order_id']
        phone = body['phone_no']
        phones = []
        delivery = Order_Items.objects.filter(
            order_id=order_id).get(delboy_type='P').phone_no
        if delivery == phone:
            for d in delivery:
                if d.delivery_boy_phone.phone_no != phone:
                    phones.append(d.delivery_boy_phone.phone_no)
            phones = unique(phones)
            # customer_phone = Orders.models.filter(order_id=order_id).customer_phone
            # phones.append(customer_phone)
            data = {
                'order_id': body['order_id'],
                'status': 'Primary delivery boy reached checkpoint'
            }
            response = beams_client.publish_to_users(
                user_ids=phones,
                publish_body={
                    'fcm': data
                },
            )

            for x in phones:
                fcm_token = Delivery_Boys.objects.get(phone_no=x)
                send_notification(fcm_token=fcm_token, data_content=data)


            # print(response['publishId'])
            response = {'success': 'true'}
            return JsonResponse(response)
        else:
            del_boy = Delivery_Boys.objects.get(phone_no=delivery)
            del_boy.busy = False
            del_boy.accepted_or_not = False
            del_boy.save()
            data = {
                'order_id': order_id,
                'status': 'Secondary delivery boy reached checkpoint',
                'phone_no': phone
            }
            response = beams_client.publish_to_users(
                user_ids=[delivery],
                publish_body={
                    'fcm': data
                },
            )
            fcm_token = del_boy.delboy_fcm_token
            send_notification(fcm_token=fcm_token, data_content=data)
            order = DeliveryBoyOrders.objects.get(del_boy_no=phone)
            order.status = 'D'
            order.save()
            # print(response['publishId'])
            response = {'success': 'true'}
            return JsonResponse(response)
    response = {'success': 'true'}
    return JsonResponse(response)


def halt_subscription(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        sorder_id = body['sorder_id']
        sorder = Subscribed_Orders.objects.get(sorder_id=sorder_id)
        if sorder.status == 'A':
            sorder.completion_status = 'I'
            sorder.save()
            return JsonResponse({"success": "True"})
        else:
            return JsonResponse({"success": "False as order is already expired"})


def delimageupload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        id = body['id']
        deli = Delivery_Boys.objects.get(del_boy_id=id)
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        deli.delivery_imagepath = filename
        deli.save()
        uploaded_file_url = fs.url(filename)
        return JsonResponse({'url': uploaded_file_url})
    return JsonResponse({'msg': 'failed'})


def get_customer_details(request):
    if request.method=='POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        order_type = body['order_type']
        if order_type == 'O':
            #phone_no = body['phone_no']
            order_id = body['order_id']
            order = Orders.objects.get(order_id=order_id)
            phone_no = order.customer_phone.phone_no
            print("phone", phone_no)
            user = RegUser.objects.get(phone_no=phone_no)
            data = {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "phone_no": user.phone_no,
                "address": order.address,
                "cust_lat": order.cust_lat,
                "cust_long": order.cust_long,
            }
            return JsonResponse(data)
        else:
            sorder_id = body['order_id']
            sorder = Subscribed_Orders.objects.get(sorder_id=sorder_id)
            phone_no = sorder.customer_phone.phone_no
            user = RegUser.objects.get(phone_no=phone_no)
            data = {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "phone": user.phone_no,
                "address": sorder.address,
                "cust_lat": sorder.cust_lat,
                "cust_long": sorder.cust_long,
            }
            return JsonResponse(data)
    else:
        return JsonResponse({"Error": "use get method"})



def get_checkpoint_details(request):
    if request.method=='POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        order_id = body['order_id']
        phone_no = body['phone_no']
        print(order_id)
        order = Orders.objects.get(order_id=order_id)
        print(order)
        primary_vendor = order.primary_vendor
        print(primary_vendor)
        checkpoint_lat = primary_vendor.vendor_lat
        checkpoint_long = primary_vendor.vendor_long
        checkpoint_address = primary_vendor.address
        order_items = Order_Items.objects.filter(order_id=order_id)
        print(order_items)
        primary_boy_number = order_items.get(delboy_type='P').delivery_boy_phone.phone_no
        print(primary_boy_number)

        phones = []
        for item in order_items:
            if item.delivery_boy_phone.phone_no != primary_boy_number:
                phones.append(item.delivery_boy_phone.phone_no)
        print(phones)
        phones = unique(phones)
        if primary_boy_number == phone_no:
            boy_type = 'P'
            print("boy_type", boy_type)
            data = []
            for phone in phones:
                d = {}
                delivery_boy = Delivery_Boys.objects.get(phone_no=phone)
                d['name'] = delivery_boy.name
                d['phone_no'] = delivery_boy.phone_no
                d['image'] = delivery_boy.delivery_imagepath.url
                d['type'] = 'S'
                data.append(d)
            return JsonResponse({
                'boy_type': boy_type,
                'checkpoint_lat': checkpoint_lat,
                'checkpoint_long': checkpoint_long,
                'checkpoint_address': checkpoint_address,
                'data': data
            })
        else:
            boy_type = 'S'
            print("boy_type", boy_type)
            delivery_boy = Delivery_Boys.objects.get(phone_no=primary_boy_number)
            data = []
            d = {}
            d['name'] = delivery_boy.name
            d['phone_no'] = delivery_boy.phone_no
            d['image'] = delivery_boy.delivery_imagepath.url
            d['type'] = 'P'
            data.append(d)
            return JsonResponse({
                'boy_type': boy_type,
                'checkpoint_lat': checkpoint_lat,
                'checkpoint_long': checkpoint_long,
                'checkpoint_address': checkpoint_address,
                'data': data
            })


def test_notification(request):
    if request.method=='GET':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        fcm_token = body['fcm_token']
        vendor_device = FCMDevice.objects.create(registration_id=fcm_token, type='android')
        vendor_device.send_message(
                                   data={
                                       "title": "hello",
                                       "body": "check",
                                       "cell": [{
                                           "lat": "123552335",
                                           "delivery_long": "123552335",
                                           "order_id": "123552335",
                                       },
                                           {
                                               "lat": "123552335",
                                               "delivery_long": "123552335",
                                               "order_id": "123552335",
                                           },

                                           {
                                               "lat": "123552335",
                                               "delivery_long": "123552335",
                                               "order_id": "123552335",
                                           },

                                           {
                                               "lat": "123552335",
                                               "delivery_long": "123552335",
                                               "order_id": "123552335",
                                           },
                                       ]
                                   }
                                   )
        return JsonResponse({
            'success': 'true'
        })
