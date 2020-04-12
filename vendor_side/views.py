from django.shortcuts import render
from .models import *
from base_tech.models import *
from django.http import JsonResponse, HttpResponseForbidden, FileResponse
from pusher import Pusher
from pusher_push_notifications import PushNotifications
from delivery_side.views import *
import Geohash
from django.utils.timezone import datetime
from datetime import date

pusher = Pusher(app_id=u'884349', key=u'7c495f369f4053064877',
                secret=u'1f0f6089002fcb5d3ce1', cluster=u'ap2', ssl=True)
beams_client = PushNotifications(
    instance_id='b0f7aac1-2560-466f-a93d-aa258d520a5a',
    secret_key='19BC4395F6CB9B17AEE81191B4B03668DDE8850EF5E76BCDBE46BBC0B6BC7DB3',
)

# Create your views here.


def vendor_register(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        items = body['items']
        products = 0
        for item in items:
            prodid = CategorizedProducts.objects.get(
                product_name=item).product_id
            products = products | (1 << prodid)
        geo = Geohash.encode(
            float(body['vendor_lat']), float(body['vendor_long']), 7)
        lat1, lon1 = Geohash.decode(geo)
        try:
            cell = Cells.objects.get(Cell_id=geo)
            cell.Cell_products = cell.Cell_products | products
            cell.no_vendor = cell.no_vendor + 1
            cell.save()
        except Cells.DoesNotExist:
            print("new distance")
            Cells.objects.create(
                Cell_id=geo, Cell_lat=lat1, Cell_long=lon1, no_vendor=1, Cell_products=products, city=body['city'])
        cell = Cells.objects.get(Cell_id=geo)
        Vendors.objects.create(
            name=body['name'],
            phone_no=body['phone_no'],
            vendor_id=body['vendor_id'],
            vendor_lat=body['vendor_lat'],
            vendor_long=body['vendor_long'],
            city=body['city'],
            status='I',
            cell=cell,
            geoha=geo,
            busy=False,
            items=products
        )
        return JsonResponse({'msg': 'success'})
    response = {
        'error': 'Invalid'
    }
    return JsonResponse(response)


def product_register(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        #items = body['items']
        under_category = body['under_category']
        product_name = body['product_name']
        for x in range(1, 100):
            pros = CategorizedProducts.objects.filter(product_id=x)
            if pros == []:
                CategorizedProducts.objects.create(
                    under_category=body['under_category'],
                    product_name=body['product_name'],
                    product_id=x,
                    product_price=body['product_price'],
                    product_rating=body['product_rating'],
                    product_descp=body['product_descp'],
                )
                break
        return JsonResponse({'msg': 'success'})
    response = {
        'error': 'Invalid'
    }
    return JsonResponse(response)


def check_vendor(request):
    if request.method == 'POST':
        print ("Entered check_vendor()")
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        try:
            obj = Vendors.objects.get(vendor_id=body['vendor_id'])
            response = {
                'vendor_phone': obj.phone_no,
                'vendor_name': obj.name,
                'vendor_id': body['vendor_id'],
                'vendor_image': obj.vendor_imagepath.url,
                'found': 'true',
                'vendor_city': obj.city,
                'vendor_address': obj.address,
                'vendor_lat': obj.vendor_lat,
                'vendor_long': obj.vendor_long
            }
        except:
            response = {
                'vendor_phone': '',
                'vendor_name': '',
                'vendor_id': body['vendor_id'],
                'found': 'false',
                'vendor_city': '',
                'vendor_address': ''
            }
        return JsonResponse(response)
    response = {
        'error': 'Invalid'
    }
    return JsonResponse(response)


# def food_ready(request):
#     if request.method == 'POST':
#         body_unicode = request.body.decode('utf-8')
#         body = json.loads(body_unicode)
#         order_id = body['order_id']
#         phone_ven = body['phone_ven']
#         data = {
#             'order_id': body['order_id'],
#             'status': 'food id ready'
#         }
#         response = beams_client.publish_to_users(
#             user_ids=[phone_ven],
#             publish_body={
#                 'fcm': data
#             },
#         )

#         # print(response['publishId'])
#         response = {'success': 'true'}
#         return JsonResponse(response)
#     response = {'success': 'true'}
#     return JsonResponse(response)


# def primary_reached_checkpoint(request):
#     if request.method == 'POST':
#         body_unicode = request.body.decode('utf-8')
#         body = json.loads(body_unicode)
#         order_id = body['order_id']
#         phone = body['phone_no']
#         phones = []
#         delivery = Order_Items.objects.filter(order_id=order_id)
#         for d in delivery:
#             if d.delivery_boy_phone.phone_no != phone:
#                 phones.append(d.delivery_boy_phone.phone_no)
#         phones = unique(phones)
#         # customer_phone = Orders.models.filter(order_id=order_id).customer_phone
#         # phones.append(customer_phone)
#         data = {
#             'order_id': body['order_id'],
#             'status': 'Primary delivery boy reached checkpoint'
#         }
#         response = beams_client.publish_to_users(
#             user_ids=phones,
#             publish_body={
#                 'fcm': data
#             },
#         )
#
#         for phone in phones:
#             fcm_token = Delivery_Boys.objects.get(phone_no=phone)
#             send_notification(fcm_token=fcm_token, data_content=data)
#
#         send_notification()
#
#         # print(response['publishId'])
#         response = {'success': 'true'}
#         return JsonResponse(response)
#     response = {'success': 'true'}
#     return JsonResponse(response)





# def vendor_order_complete(request):
#     if request.method == 'POST':
#         body_unicode = request.body.decode('utf-8')
#         body = json.loads(body_unicode)
#         order_id = body['order_id']
#         phone = body['phone_no']
#         phones = []
#         delivery = Orders.objects.get(order_id=order_id).primary_vendor
#         delivery = Order_Items.objects.filter(
#             order_id=order_id).get(deliveryBoy_type='P').phone_no
#         data = {
#             'order_id': order_id,
#             'status': 'Secondary delivery boy reached checkpoint',
#             'phone_no': phone
#         }
#         response = beams_client.publish_to_users(
#             user_ids=[delivery],
#             publish_body={
#                 'fcm': data
#             },
#         )

#         # print(response['publishId'])
#         response = {'success': 'true'}
#         return JsonResponse(response)
#     response = {'success': 'true'}
#     return JsonResponse(response)


def send_prev_products(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        objs = Vendors.objects.get(
            phone_no=body['vendor_phone'])
        obj_list = []
        for x in range(0, 50):
            if objs.items >> x & 1:
                obj = CategorizedProducts.objects.get(
                    product_id=x)
                prod = {
                    'prod_id': obj.product_id,
                    'prod_name': obj.product_name,
                    'category_name': obj.under_category.categoryName,
                    'category_id': obj.under_category.categoryId,
                    'prod_price': obj.product_price,
                    'prod_rating': obj.product_rating,
                    'prod_desc': obj.product_descp,
                    'prod_img': obj.product_imagepath.url,
                    'check': False
                }
                obj_list.append(prod)
        data = {
            'no_prod': len(obj_list),
            'products': obj_list
        }
        return JsonResponse(data)
    else:
        return JsonResponse({"error": "invalid!"})


# def pusher_authentication(request):
# 	print(request.headers['vendor-phone'])
# 	auth = pusher.authenticate(
# 		channel="private-"+request.headers['vendor-phone'],
# 		socket_id='1234.1234'
# 	)
# 	return JsonResponse(auth)


def send_all_products(request):
    if request.method == 'GET':
        objs = CategorizedProducts.objects.all()
        all_products = list(objs)
        no_prod = len(all_products)
        obj_list = []
        for i in range(no_prod):
            print(all_products[i].product_id)
            get_id = int(all_products[i].product_id)
            obj = CategorizedProducts.objects.get(product_id=get_id)
            print(obj)
            prod = {
                'prod_id': get_id,
                'prod_name': obj.product_name,
                'category_name': obj.under_category.categoryName,
                'category_id': obj.under_category.categoryId,
                'prod_price': obj.product_price,
                'prod_rating': obj.product_rating,
                'prod_desc': obj.product_descp,
                'prod_img': obj.product_imagepath.url,
                'check': False
            }
            obj_list.append(prod)
        data = {
            'no_prod': no_prod,
            'products': obj_list
        }
        print(data['products'][0]['prod_id'])
        return JsonResponse(data)


def save_vendor_products(request):
    if request.method == 'POST':
        print(request.body)
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)
        products = body['products']
        ven = Vendors.objects.get(phone_no=body['vendor_phone'])
        new_products = 0
        print(new_products)
        for product in products:
            print(product)
            item_num = CategorizedProducts.objects.get(
                product_name=str(product)).product_id
            print(item_num)
            new_products = new_products | (1 << item_num)
        ven.items = new_products
        ven.save()
        print(ven.cell)
        vendors = Vendors.objects.filter(cell=ven.cell)
        new_cell = 0
        for vendor in vendors:
            new_cell = new_cell | vendor.items
        ven.cell.Cell_products = new_cell
        ven.cell.save()
        response = {
            'success': 'true'
        }
        return JsonResponse(response)


def activate(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        #print ("Body_unicode: ", body_unicode)
        body = json.loads(body_unicode)
        obj = Vendors.objects.get(phone_no=body['vendor_phone'])
        if body['status'] == 'active':
            obj.status = 'A'
            obj.save()
        else:
            obj.status = 'I'
            obj.save()
        response = {
            'success': 'true',
            'status': body['status']
        }
        return JsonResponse(response)
    response = {
        'success': 'false',
        'status': ''
    }
    return JsonResponse(response)


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


def order_history(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        details = []
        # print(request.POST.get('vendor_phone'))
        order_details = list(prev_orders.objects.filter(order_status='D',
                                                        vendor_phone=body['vendor_phone']))
        print("order_details", order_details)
        order_ids = []
        for order_detail in order_details:
            order_ids.append(order_detail.order_id)
        order_ids = unique(order_ids)
        print("order_ids", order_ids)
        no_order = len(order_ids)
        sorder_items = list(Subscribed_Order_Items.objects.filter(vendor_phone=body['vendor_phone']))
        sorders = []
        for item in sorder_items:
            #obj = Deliverying_Boys_subs.objects.filter(sorder_id=item.sorder_id, vendor_status='I')
            sorders.append(Subscribed_Orders.objects.filter(sorder_id=item.sorder_id)[0])
        sorders = unique(sorders)
        no_sorders = len(sorders)
        myorders = []
        mysorders = []

        for order_id in order_ids:
            ords = Orders.objects.get(order_id=order_id)
            print (f"Order ID : {order_id}")
            d = {}
            d["order_id"] = order_id
            d["time"] = ords.order_time
            d["date"] = ords.order_date
            #d["order_status"] = ord.order_status
            d["price"] = ords.price
            items = []
            products = list(prev_orders.objects.filter(status='A',
                vendor_phone=body['vendor_phone'], order_id=order_id))
            # if len(products) == 1:
            #     imageurl = CategorizedProducts.objects.get(
            #         product_id=0).product_imagepath.url
            # else:
            #     imageurl = CategorizedProducts.objects.get(
            #         product_id=products[0].product_id).product_imagepath.url
            # d["image"] = imageurl
            print(f"Accepted Products : {products}")
            for product in products:
                obj = CategorizedProducts.objects.get(
                    product_id=product.product_id)
                prod = Order_Items.objects.filter(
                    product_id=product.product_id).first()
                if product.product_id == "0":
                    continue

                print("product_id", product.product_id)
                print("prod", prod)
                print("obj", obj)
                if product.status == "A":
                    check = True
                else:
                    check = False
                produ = {
                    'prod_id': obj.product_id,
                    'prod_name': obj.product_name,
                    'prod_quan': prod.quantity,
                    #'prod_size': prod.size,
                    'category_name': obj.under_category.categoryName,
                    'category_id': obj.under_category.categoryId,
                    'prod_price': obj.product_price,
                    'prod_rating': obj.product_rating,
                    'prod_desc': obj.product_descp,
                    'check': check
                }
                items.append(produ)
            d["items"] = items

            print ()
            print (f"Items : {items}\n")

            rejected_items = []
            products = list(prev_orders.objects.filter(status='R',
                vendor_phone=body['vendor_phone'], order_id=order_id))
            # if len(products) == 1:
            #     imageurl = CategorizedProducts.objects.get(
            #         product_id=0).product_imagepath.url
            # else:
            #     imageurl = CategorizedProducts.objects.get(
            #         product_id=products[0].product_id).product_imagepath.url
            # d["image"] = imageurl
            print()
            print(f"Rejected Products : {products}\n")
            for product in products:
                obj = CategorizedProducts.objects.get(
                    product_id=product.product_id)
                prod = Order_Items.objects.filter(
                    product_id=product.product_id).first()
                #if product.product_id == "0":
                #    continue
                print("product_id", product.product_id)
                print("prod", prod)
                print("obj", obj)
                #if product.status == "A":
                #    check = True
                #else:
                #    check = False
                produ = {
                    'prod_id': obj.product_id,
                    'prod_name': obj.product_name,
                    'prod_quan': prod.quantity,
                    # 'prod_size': prod.size,
                    'category_name': obj.under_category.categoryName,
                    'category_id': obj.under_category.categoryId,
                    'prod_price': obj.product_price,
                    'prod_rating': obj.product_rating,
                    'prod_desc': obj.product_descp,
                    'check': check
                }
                rejected_items.append(produ)
            d["rejected_items"] = rejected_items
            #d["rejected_items"] = rejected_items


            #print("orders", myorders)
            myorders.append(d)
        print(f"Rejected Items : {rejected_items}\n")
        print ()
        print(f"Orders : {myorders}\n\n", '-'*40)
        print ("\nSorders\n")
        for sorder in sorders:
            print(f"Sorder : {sorder}\n")
            # delivery_boys = Deliverying_Boys_subs.objects.filter(
            #     sorder_id=sorder.sorder_id, vendor_status='I').order_by('-order_date', '-order_time')
            delivery_phone = []
            delivery_order_date = []
            delivery_order_time = []
            # for boy in delivery_boys:
            #     delivery_phone.append(boy.phone_no.phone_no)
            #     delivery_order_date.append(boy.order_date)
            #     delivery_order_time.append(boy.order_time)
            vendor_subs = Vendors_subs.objects.filter(sorder_id = sorder.sorder_id,
                                                   vendor_status='D',phone_no=body['vendor_phone'])
            print(f"vendor_subs : {vendor_subs}\nlooping over vendor_subs\n")
            for vendor in vendor_subs:
                print (f"Vendor : {vendor}\nSorder.Sorder_ID : {sorder.sorder_id}\nVendor.order_date : {vendor.order_date}")
                try:
                    # delivery_boys = Deliverying_Boys_subs.objects.get(sorder_id=sorder.sorder_id, order_date=vendor.order_date)
                    #delivery_phone.append(delivery_boys.phone_no.phone_no)
                    delivery_order_date.append(vendor.order_date)
                    delivery_order_time.append(vendor.order_time)
                except:
                    print("skipping a deliverying boy since does not exists..........")
                    continue
            print ()
            d = {}
            d["sorder_id"] = sorder.sorder_id
            d["date"] = sorder.order_date
            d["duration"] = sorder.duration
            d["delivery_dates"] = sorder.delivery_dates
            d["delivery_time"] = sorder.delivery_time
            #d["order_status"] = sorder.status
            #d["delivery_phone"] = delivery_phone
            d["delivery_order_date"] = delivery_order_date
            d["delivery_order_time"] = delivery_order_time
            d["sorder_status"] = sorder.status
            # d["price"] = ord.price
            items = []
            products = []
            for product in sorder_items:
                if product.sorder_id == sorder.sorder_id:
                    products.append(product)
            print (f"Sorder Products : {products}")
            for product in products:
                obj = CategorizedProducts.objects.get(
                    product_id=product.product_id)
                quant=product.quantity
                print (f"\nProduct : {product}\nProduct_ID : {product.product_id}")
                print("obj : ", obj)
                print("prod : ", prod)

                prod = {
                    'prod_id': obj.product_id,
                    'prod_name': obj.product_name,
                    'prod_quan': quant,
                    'category_name': obj.under_category.categoryName,
                    'category_id': obj.under_category.categoryId,
                    'prod_price': obj.product_price,
                    'prod_rating': obj.product_rating,
                    'prod_desc': obj.product_descp,
                }
                items.append(prod)
            d["items"] = items

            rejected_items = []
            products = list(prev_orders.objects.filter(status='R',
                vendor_phone=body['vendor_phone'], order_id=sorder.sorder_id))
            print()
            print(f"Sorder Rejected Products : {products}\n")
            for product in products:
                obj = CategorizedProducts.objects.get(
                    product_id=product.product_id)
                # prod = Order_Items.objects.filter(
                #     product_id=product.product_id).first()
                #if product.product_id == "0":
                #    continue

                #print("product_id", product.product_id)
                #print("prod", prod)
                #print("obj", obj)
                #if product.status == "A":
                #    check = True
                #else:
                #    check = False
                produ = {
                    'prod_id': obj.product_id,
                    'prod_name': obj.product_name,
                    # 'prod_quan': prod.quantity,
                    # 'prod_size': prod.size,
                    'category_name': obj.under_category.categoryName,
                    'category_id': obj.under_category.categoryId,
                    'prod_price': obj.product_price,
                    'prod_rating': obj.product_rating,
                    'prod_desc': obj.product_descp,
                }
                rejected_items.append(produ)
            d["rejected_items"] = rejected_items
            # print(myorders)
            mysorders.append(d)
        print("sorders", mysorders)

        dict = {
            "no_order": no_order,
            "orders": myorders,
            "no_sorder": no_sorders,
            "sorders": mysorders
        }

        return JsonResponse(dict, safe=False)
    else:
        return JsonResponse({
            "error": "get method not used"
        })

# def order_ongoing(request):
#     if request.method == 'POST':
#         body_unicode = request.body.decode('utf-8')
#         body = json.loads(body_unicode)
#         details = []
#         # print(request.POST.get('vendor_phone'))
#         order_details = list(Order_Items.objects.filter(
#             vendor_phone=body['vendor_phone']))
#         print("order_details", order_details)
#         order_ids = []
#         for order_detail in order_details:
#             order_ids.append(order_detail.order_id)
#         order_ids = unique(order_ids)
#         print("order_ids", order_ids)
#         no_order = len(order_ids)
#         sorder_items = list(Subscribed_Order_Items.objects.filter(
#             vendor_phone=body['vendor_phone']))
#         sorders = []
#         for item in sorder_items:
#             sorders.append(Subscribed_Orders.objects.get(
#                 sorder_id=item.sorder_id, status='A'))
#         sorders = unique(sorders)
#         no_sorders = len(sorders)
#         mysorders = []
#         myorders = []
#         for order_id in order_ids:
#             print("order_id:", order_id)
#             try:
#                 ord = Orders.objects.get(order_id=order_id)
#                 order_items = list(Order_Items.objects.filter(order_id=order_id))
#                 obj = order_items[0]
#                 delboy = Delivery_Boys.objects.get(phone_no=obj.delivery_boy_phone)
#                 d = {}
#                 d["order_id"] = order_id
#                 d["time"] = ord.order_time
#                 d["date"] = ord.order_date
#                 d["order_status"] = ord.order_status
#                 d["price"] = ord.price
#                 d["delivery_phone"] = delboy.phone_no
#                 d["delivery_name"] = delboy.name
#                 items = []
#                 products = list(prev_orders.objects.filter(
#                     vendor_phone=body['vendor_phone'], order_id=order_id, order_status='A'))
#                 for product in products:
#                     obj = CategorizedProducts.objects.get(
#                         product_id=product.product_id)
#                     prod = Order_Items.objects.filter(
#                         product_id=product.product_id).first()
#                     print("obj", obj)
#                     if product.status == "A":
#                         check = True
#                     else:
#                         check = False
#                     prod = {
#                         'prod_id': obj.product_id,
#                         'prod_name': obj.product_name,
#                         'category_name': obj.under_category.categoryName,
#                         'category_id': obj.under_category.categoryId,
#                         'prod_price': obj.product_price,
#                         'prod_rating': obj.product_rating,
#                         'prod_desc': obj.product_descp,
#                         'check': check
#                     }
#                     items.append(prod)
#                 d["items"] = items
#                 print(myorders)
#                 myorders.append(d)
#             except:
#                 print("not found")
#         for sorder in sorders:
#             delivery_boys = Deliverying_Boys_subs.objects.filter(
#                 sorder_id=sorder.sorder_id, vendor_status='A').order_by('-order_date', '-order_time')
#             delivery_phone = []
#             delivery_order_date = []
#             delivery_order_time = []
#             for boy in delivery_boys:
#                 delivery_phone.append(boy.phone_no.phone_no)
#                 delivery_order_date.append(boy.order_date)
#                 delivery_order_time.append(boy.order_time)
#             d = {}
#             d["sorder_id"] = sorder.sorder_id
#             d["date"] = sorder.order_date
#             d["order_status"] = sorder.status
#             d["delivery_boy_phone"] = delivery_phone
#             d["delivery_order_date"] = delivery_order_date
#             d["delivery_order_time"] = delivery_order_time
#             #d["price"] = ord.price
#             items = []
#             products = []
#             for product in sorder_items:
#                 if product.sorder_id == sorder.sorder_id:
#                     products.append(product)
#             for product in products:
#                 obj = CategorizedProducts.objects.get(
#                     product_id=product.product_id)
#                 prod = Order_Items.objects.filter(
#                     product_id=product.product_id).first()
#                 print("obj", obj.product_id)
#
#                 prod = {
#                     'prod_id': obj.product_id,
#                     'prod_name': obj.product_name,
#                     'category_name': obj.under_category.categoryName,
#                     'category_id': obj.under_category.categoryId,
#                     'prod_price': obj.product_price,
#                     'prod_rating': obj.product_rating,
#                     'prod_desc': obj.product_descp,
#                 }
#                 items.append(prod)
#             d["items"] = items
#             # print(myorders)
#             mysorders.append(d)
#         print(mysorders)
#         dict = {
#             "no_order": no_order,
#             "orders": myorders,
#             "no_sorder": no_sorders,
#             "sorders": mysorders
#         }
#
#         return JsonResponse(dict)


# def delivery_details(request):
#     if request.method == 'POST':
#         objs = Orders_Items.objects.get(
#             order_id=request.POST['order_id'], vendor_phone=request.POST['vendor_phone'])
#         details = list(objs)
#         name = ''
#         phone = ''
#         if not details.delivery_boy_phone.name:
#             name = 'noName'
#             phone = 'noPhone'
#         else:
#             name = details.delivery_boy_phone.name
#             phone = details.delivery_boy_phone.phone_no

#         data = {
#             'order_id': request.POST['order_id'],
#             'vendor_phone': request.POST['vendor_phone'],
#             'del_boy_name': name,
#             'del_boy_phone': phone
#         }
#         return JsonResponse(data)
#     return JsonResponse({'error': 'invalid'})


# def pusher_check(request):
# 	#data = {
# 	#	'products': 'abcd'
# 	#}
# 	#pusher.trigger('my-channel', 'my-event', data)
# 	#return JsonResponse(data)
# 	send_vendor_order('098', '0987', '09876')
# 	return JsonResponse({'abc':'abc'})


def send_vendor_order(order_id, vendor_phone, items, quantities):
    l = len(items)
    order_items = []
    for item in items:
        obj = CategorizedProducts.objects.get(product_name=item)
        d = {
            'category_name': obj.under_category.categoryName,
            'prod_name': obj.product_name,
            'prod_id': obj.product_id,
            'prod_price': obj.product_price,
            'prod_rating': obj.product_rating,
            'prod_desc': obj.product_descp,
            'quantity': quantities[items.index(item)],
            'check': False,
        }
        order_items.append(d)
    data = {
        'order_id': str(order_id),
        #	'vendor_phone': vendor_phone,
        #	'no_prod': l,
        'items': order_items
    }
    print(data)
    # vendor = 'vendor'
    print(type(vendor_phone))
    # phone = str(vendor_phone)
    response = beams_client.publish_to_users(
        user_ids=[vendor_phone],
        publish_body={
            'fcm': data
        },
    )
    return
    # channel_name = 'vendor'+vendor_phone
    # print(data)
    # print(channel_name)
    # pusher.trigger(channel_name, 'my-event', data)


def send_vendor_order_sub(order_id, vendor_phone, items, quantities, duration, days, del_time):
    l = len(items)
    order_items = []
    for item in items:
        obj = CategorizedProducts.objects.get(product_name=item)
        d = {
            'category_name': obj.under_category.categoryName,
            'prod_name': obj.product_name,
            'prod_id': obj.product_id,
            'prod_price': obj.product_price,
            'prod_rating': obj.product_rating,
            'prod_desc': obj.product_descp,
            'quantity': quantities[items.index(item)],
            'check': False,
        }
        order_items.append(d)
    data = {
        'order_id': str(order_id),
        'duration': duration,
        'days': days,
        'del_time': del_time,
        #	'vendor_phone': vendor_phone,
        #	'no_prod': l,
        'items': order_items
    }
    print(data)
    # vendor = 'vendor'
    print(type(vendor_phone))
    # phone = str(vendor_phone)
    response = beams_client.publish_to_users(
        user_ids=[vendor_phone],
        publish_body={
            'fcm': data
        },
    )
    return


def order_prepared(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        data = {
            'order_id': body['order_id'],
            'status': 'prepared'
        }
        vendor_phone = body['vendor_phone']
        print(data)
        phones = []
        ven = Vendors.objects.get(phone_no=vendor_phone)
        pho = Order_Items.models.filter(order_id=order_id).get(
            vendor_phone=vendor_phone).delivery_boy_phone.phone_no
        pven = Orders.models.get(order_id=order_id).primary_vendor2
        phones.append(pho)
        # pusher.trigger('my-channel', 'my-event', data)
        if pven == ven.phone_no:
            customer_phone = Orders.models.filter(
                order_id=order_id).customer_phone
            phones.append(customer_phone)
        response = beams_client.publish_to_users(
            user_ids=phones,
            publish_body={
                'fcm': data
            },
        )
        response = {'success': 'true'}
        return JsonResponse(response)
    response = {'success': 'false'}
    return JsonResponse(response)


def order_dispatched(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        order_id = body['order_id']
        vendor_phone = body['vendor_phone']
        obj = prev_orders.objects.get(
            order_id=order_id, vendor_phone=vendor_phone)
    # if obj[0].order_status == "A":
        ven = Vendors.objects.get(phone_no=vendor_phone)
        if obj.order_status == "A":
            vendor = Vendors.objects.get(phone_no=vendor_phone)
            print(vendor)
            vendor.current_no_orders = vendor.current_no_orders - 1
            print(vendor.current_no_orders)
            vendor.save()
            prev_orders.objects.filter(
                order_id=order_id, vendor_phone=vendor_phone).update(order_status="D")
        type = Orders.models.get(order_id=order_id).primary_vendor2
        # pusher.trigger('my-channel', 'my-event', data)
        if type == ven:
            customer_phone = Orders.models.filter(
                order_id=order_id).customer_phone
            data = {
                'order_id': request.POST['order_id'],
                'status': 'order dispatched'
            }
            response = beams_client.publish_to_users(
                user_ids=[customer_phone],
                publish_body={
                    'fcm': data
                },
            )
        response = {'success': 'true'}
        return JsonResponse(response)

        response = {'success': 'false'}
    return JsonResponse(response)


def send_order_id(request, order_id, vendor_phone):
    fcm_token = Vendors.objects.get(phone_no=vendor_phone).vendor_fcm_token
    send_notification(fcm_token=fcm_token, data_content={'order_id': order_id})


def send_order_items(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        order_id = body['order_id']
        vendor_phone = body['vendor_phone']
        order_items = Order_Items.objects.filter(
            order_id=order_id, vendor_phone=vendor_phone)
        final = []
        for item in order_items:
            product = CategorizedProducts.objects.get(
                product_id=item.product_id)
            d = {}
            d['product_id'] = product.product_id
            d['product_name'] = product.product_name
            d['product_price'] = product.product_price
            d['quantity'] = item.quantity
            final.append(d)
        order = Orders.objects.get(order_id=order_id)
        return JsonResponse({
            'items': final,
            'order_date':order.order_date,
            'order_time': order.order_time,
            #'otp':order_items[0].otp
        })


def send_subscribed_order_items(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        today = datetime.today()
        sorder_id = body['sorder_id']
        vendor_phone = body['vendor_phone']
        sorder_items = Subscribed_Order_Items.objects.filter(
            sorder_id=sorder_id, vendor_phone=vendor_phone)
        objs = Deliverying_Boys_subs.objects.filter(sorder_id=sorder_id, status='A',
                                                    order_date__year=today.year,
                                                    order_date__month=today.month,
                                                    order_date__day=today.day).order_by('order_time')
        final = []
        for item in sorder_items:
            product = CategorizedProducts.objects.get(
                product_id=item.product_id)
            sorder = Subscribed_Orders.objects.filter(sorder_id=item.sorder_id)[0]
            d = {}
            d['product_id']     = product.product_id
            d['product_name']   = product.product_name
            d['product_price']  = product.product_price
            d['quantity']       = item.quantity
            d['duration']       = sorder.duration
            d['order_date']     = sorder.order_date
            d['delivery_dates'] = sorder.delivery_dates
            d['delivery_time']  = sorder.delivery_time
            final.append(d)
        return JsonResponse({
            'items': final,
            #'otp': objs[0].otp
        })


def vendorimageupload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        id = body['id']
        ven = Vendors.objects.get(vendor_id=id)
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        ven.vendor_imagepath = filename
        ven.save()
        uploaded_file_url = fs.url(filename)
        return JsonResponse({'url': uploaded_file_url})
    return JsonResponse({'msg': 'failed'})


def productimageupload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        id = body['id']
        pro = CategorizedProducts.objects.get(product_id=id)
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        pro.product_imagepath = filename
        pro.save()
        uploaded_file_url = fs.url(filename)
        return JsonResponse({'url': uploaded_file_url})
    return JsonResponse({'msg': 'failed'})


def order_ongoing(request):
    if request.method == 'POST':
        today = datetime.today()
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        vendor_phone = body['vendor_phone']
        mysorders = []
        myorders = []

        print("checking sorders")
        sorder_items = Subscribed_Order_Items.objects.filter(vendor_phone=vendor_phone)

        sorder_ids = []
        print("sorder items", sorder_items)
        for item in sorder_items:
            sorder_ids.append(item.sorder_id)
        sorder_ids = unique(sorder_ids)
        print(sorder_ids)
        subs_order_ids = []
        for sorder_id in sorder_ids:
            objs = Vendors_subs.objects.filter(sorder_id=sorder_id, vendor_status='N',
                                                       order_date__year=today.year,
                                                       order_date__month=today.month,
                                                       order_date__day=today.day).order_by('order_time')
            print(objs)
            for obj in objs:
                subs_order_ids.append(obj.sorder_id)
        subs_order_ids = unique(subs_order_ids)
        for sorder_id in subs_order_ids:
            try:
                sorder = Subscribed_Orders.objects.filter(sorder_id=sorder_id)
                sorder = sorder[0]
            except:
                print("no found")
                continue
            #delivery_boy_sub = Deliverying_Boys_subs.objects.get(
            #    sorder_id=sorder.sorder_id, status='A',
            #    order_date__year=today.year,
            #    order_date__month=today.month,
            #    order_date__day=today.day
            #)
            #delivery_boy = delivery_boy_sub.phone_no
            # delivery_phone = []
            # delivery_order_date = []
            # delivery_order_time = []
            # for boy in delivery_boys:
            #     delivery_phone.append(boy.phone_no.phone_no)
            #     delivery_order_date.append(boy.order_date)
            #     delivery_order_time.append(boy.order_time)
            d = {}
            d["sorder_id"] = sorder.sorder_id
            d["date"] = sorder.order_date
            d["duration"] = sorder.duration
            d["otp"] = Vendors_subs.objects.get(sorder_id=sorder_id, vendor_status='N',
                                                       order_date__year=today.year,
                                                       order_date__month=today.month,
                                                       order_date__day=today.day).otp
            d["delivery_boy_phone"] = delivery_boy.phone_no
            d["delivery_boy_name"] = delivery_boy.name
            # d["delivery_order_date"] = delivery_boy_sub.order_date
            # d["delivery_order_time"] = delivery_boy_sub.order_time
            #d["price"] = ord.price
            items = []
            products = []
            for product in sorder_items:
                if product.sorder_id == sorder.sorder_id:
                    products.append(product)
            for product in products:
                obj = CategorizedProducts.objects.get(
                    product_id=product.product_id)
                prod = Order_Items.objects.filter(
                    product_id=product.product_id).first()
                print("obj", obj.product_id)

                prod = {
                    'prod_id': obj.product_id,
                    'prod_name': obj.product_name,
                    'category_name': obj.under_category.categoryName,
                    'category_id': obj.under_category.categoryId,
                    'prod_price': obj.product_price,
                    # 'prod_rating': obj.product_rating,
                    # 'prod_desc': obj.product_descp,
                }
                items.append(prod)
            d["items"] = items
            # print(myorders)
            mysorders.append(d)
        print(mysorders)


        print("checking orders")
        order_items = Order_Items.objects.filter(vendor_phone=vendor_phone)


        print("orderitems", order_items)
        order_ids = []
        for item in order_items:
            print(item.order_id)
            try:
                obj = Orders.objects.get(order_id=item.order_id, order_date__year=today.year,
                                         order_date__month=today.month,
                                         order_date__day=today.day)
            except:
                print("no order")
                continue
            print("obj", obj)
            obj2 = prev_orders.objects.get(order_id=item.order_id, product_id=item.product_id)
            print("obj2", obj2)
            if obj2.order_status == 'A':
                print('appending')
                order_ids.append(obj.order_id)
        order_ids = unique(order_ids)
        for order_id in order_ids:
            ord = Orders.objects.get(order_id=order_id)
            print("order_id", order_id)
            del_boy_orders = DeliveryBoyOrders.objects.get(order_id=order_id)
            delivery_boy = del_boy_orders.del_boy_no
            d = {}
            d["order_id"] = order_id
            d["time"] = ord.order_time
            d["date"] = ord.order_date
            # d["order_status"] = ord.order_status
            d["price"] = ord.price
            d["delivery_boy_phone"] = delivery_boy.phone_no
            d["delivery_boy_name"] = delivery_boy.name

            products = list(prev_orders.objects.filter(
                vendor_phone=body['vendor_phone'], order_id=order_id))
            items = Order_Items.objects.filter(vendor_phone=body['vendor_phone'], order_id=order_id)
            otp = items[0].otp
            d['otp'] = otp
            if len(products) == 1:
                imageurl = CategorizedProducts.objects.get(
                    product_id=0).product_imagepath.url
            else:
                imageurl = CategorizedProducts.objects.get(
                    product_id=products[0].product_id).product_imagepath.url
            #d["image"] = imageurl
            items = []
            for product in products:
                obj = CategorizedProducts.objects.get(
                    product_id=product.product_id)
                prod = Order_Items.objects.filter(
                    product_id=product.product_id).first()
                print("obj", obj)
                # if product.status == "A":
                #     check = True
                # else:
                #     check = False
                prod = {
                    'prod_id': obj.product_id,
                    'prod_name': obj.product_name,
                    'prod_quan': prod.quantity,
                    #'prod_size': prod.size,
                    'category_name': obj.under_category.categoryName,
                    'category_id': obj.under_category.categoryId,
                    'prod_price': obj.product_price,
                    # 'prod_rating': obj.product_rating,
                    # 'prod_desc': obj.product_descp,
                    # 'check': check
                }
                items.append(prod)
            d["items"] = items
            print(myorders)
            myorders.append(d)

        return JsonResponse({
            'mysorders': mysorders,
            'myorders': myorders
        })

def order_ongoing_alt(request):
    if request.method == 'POST':
        today = datetime.today()
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        vendor_phone = body['vendor_phone']
        mysorders = []
        myorders = []

        myorders=prev_orders.objects.filter(vendor_phone=vendor_phone,order_type='N',status='A',order_status='A')
        mysorders=Vendors_subs.objects.filter(phone_no=vendor_phone,vendor_status='N')
        order_id=[]
        sorder_id=[]
        orders=[]
        sorders=[]

        #                   #
        # for normal orders #
        #                   #
        for item in myorders:
           order_id.append(item.order_id)
        order_id = unique(order_id)
        
        for oid in order_id:
            oid=order_id[0]
            ordr=Orders.objects.get(order_id=oid)
            del_boy = Order_Items.objects.get(vendor_phone=body['vendor_phone'], order_id=oid)
            #delivery_boy = del_boy_orders.delivery_boy_phone
            d = {}
            d["order_id"] = oid
            d["time"] = ordr.order_time
            d["date"] = ordr.order_date
            d["price"] = ordr.price
            d["delivery_boy_phone"] = del_boy.delivery_boy_phone.phone_no
            d['otp'] = del_boy.otp
            # if len(products) == 1:
            #     imageurl = CategorizedProducts.objects.get(product_id=0).product_imagepath.url
            # else:
            #     imageurl = CategorizedProducts.objects.get(product_id=products[0].product_id).product_imagepath.url
            #d["image"] = imageurl
            items = []
            for product in myorders.filter(order_id=oid):
                obj = CategorizedProducts.objects.get(product_id=product.product_id)
                prod = Order_Items.objects.get(product_id=product.product_id)
                # if product.status == "A":
                #     check = True
                # else:
                #     check = False
                prod = {
                    'prod_id': obj.product_id,
                    'prod_name': obj.product_name,
                    'prod_quan': prod.quantity,
                    #'prod_size': prd.size,
                    'category_name': obj.under_category.categoryName,
                    'category_id': obj.under_category.categoryId,
                    'prod_price': obj.product_price,
                    # 'prod_rating': obj.product_rating,
                    # 'prod_desc': obj.product_descp,
                    # 'check': check
                }
                items.append(prod)
            d["items"] = items
            orders.append(d)

        #                       #
        # for subscribed orders #
        #                       #        
        for item in mysorders:
           sorder_id.append(item.sorder_id)
        sorder_id = unique(sorder_id)
        for oid in sorder_id:
            ordr=Subscribed_Orders.objects.get(sorder_id=oid,order_date=date.today())
            del_boy = Deliverying_Boys_subs.objects.get(sorder_id=oid,order_date=date.today()).phone_no
            d = {}
            d["sorder_id"] = oid
            d["time"] = ordr.order_time
            d["date"] = ordr.order_date
            d["delivery_boy_phone"] = del_boy.phone_no
            products = list(prev_orders.objects.filter(vendor_phone=body['vendor_phone'], order_id=oid))
            item_otp = Vendors_subs.objects.get(phone_no=body['vendor_phone'], sorder_id=oid,order_date=date.today())
            otp = items_otp[0].otp
            d['otp'] = otp
            # if len(products) == 1:
            #     imageurl = CategorizedProducts.objects.get(
            #         product_id=0).product_imagepath.url
            # else:
            #     imageurl = CategorizedProducts.objects.get(
            #         product_id=products[0].product_id).product_imagepath.url
            #d["image"] = imageurl
            items = []
            for product in products:
                obj = CategorizedProducts.objects.get(product_id=product.product_id)
                prod = Subscribed_Order_Items.objects.filter(product_id=product.product_id,sorder_id=oid).first()
                prod = {
                    'prod_id': obj.product_id,
                    'prod_name': obj.product_name,
                    'prod_quan': prod.quantity,
                    #'prod_size': prod.size,
                    'category_name': obj.under_category.categoryName,
                    'category_id': obj.under_category.categoryId,
                    'prod_price': obj.product_price,
                    # 'prod_rating': obj.product_rating,
                    # 'prod_desc': obj.product_descp,
                    # 'check': check
                }
                items.append(prod)
            d["items"] = items
            sorders.append(d)

        return JsonResponse({
            'mysorders': sorders,
            'myorders': orders
        })
