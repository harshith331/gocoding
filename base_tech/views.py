from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse, FileResponse
from django.middleware.csrf import get_token
from rest_framework.views import APIView
from .models import *
from vendor_side.models import *
from .serializers import *
from rest_framework.response import Response
import io
from math import cos, asin, sqrt
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import itertools
#from background_task import background
from vendor_side.views import *
from delivery_side.views import *
from django.utils import timezone
import datetime
import requests
from django.utils.safestring import mark_safe
import json
import requests
from geographiclib.geodesic import Geodesic
from copy import deepcopy
import uuid
import firebase_admin
import google
from firebase_admin import credentials, firestore
import Geohash
import time
from random import random


class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


def user_list(request):
    return render(request, 'base_tech/abc.html', {})

# DEFAULT page


def index(request):
    print(request.scheme)
    return render(request, 'base_tech/index.html')


# Sending CSRF Token
def getaccess(request):
    return JsonResponse({'csrfToken': get_token(request)})


def initialsignup(request):
    if request.method == 'POST':
        no = request.POST['phone_no']
        try:
            obj = RegUser.objects.get(pk=no)
            print(obj.first_name)
            response = {'error': '', 'found': 'true', 'phone_no': no, 'first_name': obj.first_name, 'email': obj.email,
                        'last_name': obj.last_name, 'wallet_amt': obj.wallet_amt}
        except:
            print("hello")
            response = {'error': '', 'found': 'false', 'phone_no': no,
                        'first_name': '', 'email': '', 'last_name': '', 'wallet_amt': '0'}
        return JsonResponse(response)


def validate_Email(email):
    from django.core.exceptions import ValidationError
    from django.core.validators import validate_email
    try:
        validate_email(email)
    except ValidationError as e:
        return False
    else:
        return True

def SignUp(request):
    if request.method=='POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        response = {
            'success': 'false',
            'error_msg': {
                'phone_no':'',
                'email':''
            }
        }
        if validate_Email(body['email']):
            response['error_msg']['email'] = ''
        else:
            response['error_msg']['email'] = 'invalid email'
            return JsonResponse(response)

        try:
            r =  RegUser.objects.get(phone_no=body['phone_no'])
            response['error_msg']['phone_no'] = 'account with this phone no already exists.'
        except RegUser.DoesNotExist:
            pass
        try:
            r =  RegUser.objects.get(email=body['email'])
            response['error_msg']['email'] = 'account with this email already exists.'
        except  RegUser.DoesNotExist:
            pass
        
        if response['error_msg']['phone_no'] != '' or response['error_msg']['email'] != '':
            return JsonResponse(response)
        else:   
            r = RegUser(first_name=body['first_name'],
                        last_name=body['last_name'],
                        phone_no=body['phone_no'],
                        email=body['email'])
            r.save()
            response['success'] = 'true'
        return JsonResponse(response)
#
#class SignUp(APIView):
#    def post(self, request):
#        print("Inside signup")
#        response = JsonResponse({'Error': 'True'})
#        print("Inside POST")
#        serializer = RegUserSerializer(data=request.data)
#        response = {'success': 'false', 'error': 'invalid data'}
#        if serializer.is_valid():
#            serializer.save()
#            email_err = ""
#            phone_err = ""
#            err_msg = {'phone_no': phone_err, 'email': email_err}
#            response = {'success': 'true', 'error': err_msg}
#            return JsonResponse(response)
#        print(serializer.errors)
#        try:
#            email_err = serializer.errors['email'][0]
#        except:
#            email_err = ""
#        try:
#            phone_err = serializer.errors['phone_no'][0]
#        except:
#            phone_err = ""
#        err_msg = {'phone_no': phone_err, 'email': email_err}
#        response = {'success': 'false', 'error': err_msg}
#        return JsonResponse(response)
#
#
# Signing in User
# def loginuser(request):
#     print("Inside login")
#
#     if request.method == 'POST':
#         print("Inside POST")
#         username = request.POST['username']
#         raw_password = request.POST['password']
#         user = authenticate(username=username, password=raw_password)
#         if user is not None:
#             login(request, user)
#             logging_in_user = User.objects.get(username=username)
#
#             response = {'username': logging_in_user.username, 'email': logging_in_user.email,
#                         'first_name': logging_in_user.first_name, 'last_name': logging_in_user.last_name}
#             return JsonResponse(response)
#         else:
#             return JsonResponse({'Error': 'Error Signing in !!!'})
#     else:
#         print("Not POST")
#         return JsonResponse({'Error': 'Not a post call !!!'})


# def loadAllCategories(request):
#     username = request.POST['username']
#     if User.objects.filter(username=username):
#         items = Category.objects.all()
#         myCategories = []
#         for item in items:
#             dict = {}
#             dict["categoryId"] = item.categoryId
#             dict["categoryName"] = item.categoryName
#             dict["categoryImagePath"] = item.categoryImagePath
#             myCategories.append(dict)

#         return JsonResponse({'categories': myCategories})

#     else:
#         return JsonResponse({'categories': []})


def loadSingleCategory(request, categoryId):
    products = CategorizedProducts.objects.filter(under_category=categoryId)
    myProducts = []
    for product in products:
        dict = {}
        dict["under_category"] = product.under_category
        dict["product_name"] = product.product_name
        dict["product_descp"] = product.product_descp
        dict["product_id"] = product.product_id
        dict["product_price"] = product.product_price
        dict["product_rating"] = product.product_rating
        dict["product_imagepath"] = product.product_imagepath
        myProducts.append(dict)

    return JsonResponse({'products': myProducts})


# def hotel_image_view(request):
#     if request.method == 'POST':
#         form = HotelForm(request.POST, request.FILES)

#         if form.is_valid():
#             form.save()
#             return redirect('success')
#     else:
#         form = HotelForm()
#     return render(request, 'base_tech/hotel_image_form.html', {'form': form})


def success(request):
    return HttpResponse('successfuly uploaded')


# def display_hotel_images(request):
#     if request.method == 'GET':
#         Hotels = Hotel.objects.all()
#         print(Hotels[0].hotel_Main_Img.url)
#         return render(request, 'base_tech/display_hotel_images.html',
#                       {'hotel_images': Hotels})


# def send_file(response):
#     img = open('media/images/Screenshot_from_2019-06-27_01-12-24.png', 'rb')
#     response = FileResponse(img)
#     return response


# def distance(lat1, lon1, lat2, lon2):
#     p = 0.017453292519943295
#     a = 0.5 - cos((lat2-lat1)*p)/2+cos(lat1*p) * \
#         cos(lat2*p)*(1-cos((lon2-lon1)*p))/2
#     return 12742*asin(sqrt(a))


def distance(lat1, lon1, lat2, lon2):
    api_key = 'AIzaSyB7URlD8s2pt2MjUIM4e6C2nL2-5XhKDqo'
    # print(lat1)
    # print(lon2)
    # print(lat2)
    # print(lon2)
    url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
    r = requests.get("https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins="+str(
        lat1)+","+str(lon1)+"&destinations="+str(lat2)+","+str(lon2)+"&key=AIzaSyB7URlD8s2pt2MjUIM4e6C2nL2-5XhKDqo")
    # print(r.url())
    x = r.json()
    #print(x)
    for r in x['rows']:
        for ri in r['elements']:
            #print(ri)
            m = float(ri['distance']['value'])/1000
    return m


def geodistance(geo1, geo2):
    lat1, lon1 = Geohash.decode(geo1)
    lat2, lon2 = Geohash.decode(geo2)
    return distance(lat1, lon1, lat2, lon2)


def geodistance2(lat1, lon1, lat2, lon2):
    ph = Geohash.encode(lat1, lon1, 7)
    ph2 = Geohash.encode(lat2, lon2, 7)
    try:
        geo = geohash_distance.objects.get(geohash1=ph, geohash2=ph2)
        return geo.dist
    except geohash_distance.DoesNotExist:
        geohash_distance.objects.create(
            geohash1=ph, geohash2=ph2, dist=geodistance(ph, ph2))
    return geodistance(ph, ph2)


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


# def useid(request, image_id):
#     path = "%s"
#     img = open(path, 'rb')
#     response = FileResponse(img)
#     return response


def get_bearing(lat1, lat2, long1, long2):
    brng = Geodesic.WGS84.Inverse(lat1, long1, lat2, long2)['azi1']
    return brng


def sector_check(lat1, long1, lat2, long2, lat3, long3):
    angle = get_bearing(lat1, lat2, long1, long2) - \
        get_bearing(lat2, lat3, long2, long3)
    if(angle >= 0):
        angle = 180 - angle
        return angle, 0
    else:
        angle = -180 - angle
        return angle, 1


def get_order_history(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body['cust_phone'])
        objs = Orders.objects.filter(customer_phone=RegUser.objects.get(
            phone_no=body['cust_phone']))
        cust_orders = list(objs)
        no_orders = len(cust_orders)
        obj_list = []
        print(cust_orders)
        for i in range(no_orders):
            d = {}
            ord = Order_Items.objects.filter(order_id=cust_orders[i].order_id)
            d["order_id"] = cust_orders[i].order_id
            d["order_date"] = cust_orders[i].order_date
            d["order_time"] = cust_orders[i].order_time
            d["price"] = cust_orders[i].price
            items = []
            for ob in ord:
                obj = CategorizedProducts.objects.get(
                    product_id=ob.product_id)
                if len(ord) == 1:
                    imageurl = CategorizedProducts.objects.get(
                        product_id=0).product_imagepath.url
                else:
                    imageurl = obj.product_imagepath.url
                prod = {
                    'prod_id': obj.product_id,
                    'prod_name': obj.product_name,
                    'category_name': obj.under_category.categoryName,
                    'category_id': obj.under_category.categoryId,
                    'prod_price': obj.product_price,
                    'prod_rating': obj.product_rating,
                    'prod_desc': obj.product_descp,
                    # 'prod_img': obj.product_imagepath,
                    'check': False,
                    'prod_img': imageurl,
                }
                items.append(prod)
            d["items"] = items
            obj_list.append(d)
        data = {
            'no_orders': no_orders,
            'orders': obj_list
        }
        return JsonResponse(data)


# def is_Sublist(l, s):
#     sub_set = False
#     if s == []:
#         sub_set = True
#     elif s == l:
#         sub_set = True
#     elif len(s) > len(l):
#         sub_set = False

#     else:
#         for i in range(len(l)):
#             if l[i] == s[0]:
#                 n = 1
#                 while (n < len(s)) and (l[i+n] == s[n]):
#                     n += 1

#                 if n == len(s):
#                     sub_set = True

#     return sub_set


def vendor_assignment(vendors, ar2, order_id, order_products):
    print("vendors=", vendors)
    print(order_products)
    if (len(vendors) == 0):
        print("len_vendors")
        print(order_products)
        return order_products
    if order_products == 0:
        return order_products
    # n = order_products

    cmax = 0
    check = 0
    for vendor in vendors:
        products_vendor = vendor.items
        order_accepted = products_vendor & order_products
        m = bin(order_accepted).count('1')
        if m > cmax:
            cmax = m
            vmax = vendor
            check = 1
    previous_order_state = order_products
    if check == 0:
        return order_products
    print(vmax.phone_no)
    print(vmax.items)
    print("common pro", cmax)
    # cmax=0
    # vmax=vendors[0]
    # for count,ven in zip(product_count,vendors):
    #      if count>=cmax:
    #          cmax=count
    #          vmax=ven
    # print("vendors_max",vmax)
    # print("count_max",cmax)
    order_accepted = order_products & vmax.items

    current_order_state = order_products ^ vmax.items
    current_order_state = order_products & current_order_state
    print(current_order_state)
    total_orders = []
    order_quantities = []
    order_size = []
    # products_selected_vendor = Vendor_Products.objects.filter(
    #     vendor_phone=vmax).items
    # order_accepted = products_selected_vendor ^ order_products
    # order_accepted = order_accepted & order_products
    # k=0
    # for quan in ar2:
    #     if ar2>0 and products_selected_vendor & k:
    #         total_orders.append(iteminfo.objects.filter(item_no==(k+1)))
    #         order_quantities.append(quan)
    # print(total_orders)
    # rejected_orders = []

    for x in range(0, 40):
        if order_accepted >> x & 1:
            itemin = CategorizedProducts.objects.get(product_id=x).product_name
            total_orders.append(itemin)
            order_quantities.append(ar2[x])

    print(total_orders)
    print(order_quantities)
    print(vmax.phone_no)
    send_vendor_order(order_id, vmax.phone_no,
                      total_orders, order_quantities)
    # rejected orders

    # for item in total_orders:
    #     if item not in total_orders:
    #         rejected_orders.append(item)
    post_data = {
        "total_orders": total_orders,
        "order_quantities": order_quantities,
        "Vendor_phone": vmax.phone_no
    }

    # vendor_assigned_list.append(vmax)
    # accepted_orders_list.append(accepted_orders)
    # rejected_orders_list.append(rejected_orders)

    vendors.remove(vmax)

    print("end of v_assign")
    print(ar2)
    neworder_products = vendor_assignment(
        vendors, ar2, order_id, current_order_state)
    return neworder_products


def cell_sort(cells, cellpros, ar2, user_latitude, user_longitude, city, order_id, order_products):
    print("cell_sort_top", cells)
    print(order_products)
    if len(cells) == 0:
        print("len_cells=0")
        return order_products
    if order_products == 0:
        print("len_ar1=0")
        return order_products
    # n = bin(order_products).count('1')
    print(order_products)
    count_max = 0
    mindistance = 100
    for cell, cellpro in zip(cells, cellpros):
        products = cellpro
        order_accepted = products & order_products
        m = bin(order_accepted).count('1')
        if m == count_max:
            dist = geodistance2(cell.Cell_lat, cell.Cell_long,
                                user_latitude, user_longitude)
            if dist < mindistance:
                closest_cell = cell
                mindistance = dist
        if m > count_max:
            count_max = m
            dist = geodistance2(cell.Cell_lat, cell.Cell_long,
                                user_latitude, user_longitude)
            mindistance = dist
            closest_cell = cell
            closest_cell_prod = cellpro

    vendors = []
    print("products in cells", count_max)
    print("closest_cell", closest_cell)
    vendors_all = list(Vendors.objects.filter(cell=closest_cell))
    not_vendors = list(prev_orders.objects.filter(order_id=order_id))
    notvens = []
    for notven in not_vendors:
        notvens.append(notven.vendor_phone)
    # print(notvens)
    for vendor in vendors_all:
        # if vendor.current_no_orders < 5:
        if vendor.phone_no not in notvens:
            vendors.append(vendor)

    new_order_products = vendor_assignment(
        vendors, ar2, order_id, order_products)

    # print(new_ar2)

    cells.remove(closest_cell)
    cellpros.remove(cellpro)

    # new_order_products = Orders.objects.get(order_id=order_id).pending_order

    new_order_products = cell_sort(
        cells, cellpros, ar2, user_latitude, user_longitude, city, order_id, new_order_products)
    return new_order_products


def vendor_assignment_sub(vendors, ar2, order_id, order_products, duration, days, del_time):
    print("a", vendors)
    print(order_products)
    if (len(vendors) == 0):
        print("len_vendors")
        print(order_products)
        return order_products
    if order_products == 0:
        return order_products
    # n = order_products

    cmax = 0
    check = 0
    for vendor in vendors:
        products_vendor = vendor.items
        order_accepted = products_vendor & order_products
        m = bin(order_accepted).count('1')
        if m > cmax:
            cmax = m
            vmax = vendor
            check = 1
    previous_order_state = order_products
    if check == 0:
        return order_products
    print(vmax.phone_no)
    print(vmax.items)
    # cmax=0
    # vmax=vendors[0]
    # for count,ven in zip(product_count,vendors):
    #      if count>=cmax:
    #          cmax=count
    #          vmax=ven
    # print("vendors_max",vmax)
    # print("count_max",cmax)
    order_accepted = order_products & vmax.items

    current_order_state = order_products ^ vmax.items
    current_order_state = order_products & current_order_state
    print(current_order_state)
    total_orders = []
    order_quantities = []
    order_size = []
    # products_selected_vendor = Vendor_Products.objects.filter(
    #     vendor_phone=vmax).items
    # order_accepted = products_selected_vendor ^ order_products
    # order_accepted = order_accepted & order_products
    # k=0
    # for quan in ar2:
    #     if ar2>0 and products_selected_vendor & k:
    #         total_orders.append(iteminfo.objects.filter(item_no==(k+1)))
    #         order_quantities.append(quan)
    # print(total_orders)
    # rejected_orders = []

    for x in range(0, 40):
        if order_accepted >> x & 1:
            itemin = CategorizedProducts.objects.get(product_id=x).product_name
            total_orders.append(itemin)
            order_quantities.append(ar2[x])

    print(total_orders)
    print(order_quantities)
    print(vmax.phone_no)
    send_vendor_order_sub(order_id, vmax.phone_no,
                          total_orders, order_quantities, duration, days, del_time)
    # rejected orders

    # for item in total_orders:
    #     if item not in total_orders:
    #         rejected_orders.append(item)
    # post_data = {
    #     "total_orders": total_orders,
    #     "order_quantities": order_quantities,
    #     "Vendor_phone": vmax.phone_no
    # }

    # vendor_assigned_list.append(vmax)
    # accepted_orders_list.append(accepted_orders)
    # rejected_orders_list.append(rejected_orders)

    vendors.remove(vmax)

    print("end of v_assign")
    print(ar2)
    neworder_products = vendor_assignment_sub(
        vendors, ar2, order_id, current_order_state, duration, days, del_time)
    return neworder_products


def cell_sort_sub(cells, cellpros, ar2, user_latitude, user_longitude, city, order_id, order_products, duration, days, del_time):
    print("cell_sort_top", cells)
    print(order_products)
    if len(cells) == 0:
        print("len_cells=0")
        return order_products
    if order_products == 0:
        print("len_ar1=0")
        return order_products
    # n = bin(order_products).count('1')
    print(order_products)
    count_max = 0
    mindistance = 100
    for cell, cellpro in zip(cells, cellpros):
        products = cellpro
        order_accepted = products & order_products
        m = bin(order_accepted).count('1')
        if m == count_max:
            dist = geodistance2(cell.Cell_lat, cell.Cell_long,
                                user_latitude, user_longitude)
            if dist < mindistance:
                closest_cell = cell
                mindistance = dist
        if m > count_max:
            count_max = m
            dist = geodistance2(cell.Cell_lat, cell.Cell_long,
                                user_latitude, user_longitude)
            mindistance = dist
            closest_cell = cell
            closest_cell_prod = cellpro

    vendors = []
    print("products in cells", count_max)
    print("closest_cell", closest_cell)
    vendors_all = list(Vendors.objects.filter(cell=closest_cell))
    not_vendors = list(prev_orders.objects.filter(order_id=order_id))
    notvens = []
    for notven in not_vendors:
        notvens.append(notven.vendor_phone)
    # print(notvens)
    for vendor in vendors_all:
        # if vendor.current_no_orders < 5:
        if vendor.phone_no not in notvens:
            vendors.append(vendor)

    new_order_products = vendor_assignment_sub(
        vendors, ar2, order_id, order_products, duration, days, del_time)

    # print(new_ar2)

    cells.remove(closest_cell)
    cellpros.remove(cellpro)

    # new_order_products = Orders.objects.get(order_id=order_id).pending_order

    new_order_products = cell_sort_sub(
        cells, cellpros, ar2, user_latitude, user_longitude, city, order_id, new_order_products, duration, days, del_time)
    return new_order_products


def delivery_boy_assignment(vendor_assigned_list, cells, cell_distance, user_latitude, user_longitude, city, phone_no, order_id):
    cell_inside = []
    dist_inside = []
    max_u2d = 0
    #distance_sector = []
    final_vendor_cell = []
    print("insidecbcm")
    final_distance_cell = []
    # final_aol = []
    final_deliverBoy = []
    if (not len(firebase_admin._apps)):
        cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred)
    db = firestore.client()
    deliveryBoy_list = list(Delivery_Boys.objects.filter(
        city__iexact=city, status="A"))  # busy="true"

    for boy in deliveryBoy_list:
        doc_rf = db.collection(u'DeliveryBoyLocation').document(
            u'{}'.format(boy.phone_no))
        doc = doc_rf.get()
        boy.lat = doc.to_dict()['geo_point'].latitude
        boy.long = doc.to_dict()['geo_point'].longitude
        # print("boy lat long", boy.lat, boy.long)
        boy.save()

    order = Orders.objects.get(order_id=order_id)
    # inside_2_km = 0
    # city = city, ))
    checkpoint_lat = user_latitude
    checkpoint_long = user_longitude
    # , status = 'I',busy = False))
    # print("deliveryBoy_list", deliveryBoy_list)
    min_checkpoint = 1000
    for cell, dist in zip(cells, cell_distance):
        # print(dist)
        if dist < 1:
            cell_inside.append(cell)
            # print("val_inside", cell_inside)
            dist_inside.append(dist)
            # cells.remove(cell)
            # cell_distance.remove(dist)
            # vendor aur unki distance aa gayi
        if(dist < min_checkpoint):
            min_checkpoint = dist
            pcell = cell
            ven = Vendors.objects.filter(cell=cell).first()
            checkpoint_lat = ven.vendor_lat
            checkpoint_long = ven.vendor_long
            primary_vendor = ven
            primary_vendor2 = ven.phone_no
            # if dist < 2:
            #     inside_2_km = 1
            # distance_sector.append(dist)
    for cell, dist in zip(cell_inside, dist_inside):
        cells.remove(cell)
        cell_distance.remove(dist)
    print(cells)
    order.primary_cell = pcell
    order.save()
    vens = Vendors.objects.all()
    if min_checkpoint > 2:
        for ven in vens:
            if geodistance2(user_latitude, user_longitude, ven.vendor_lat, ven.vendor_long) < 2 and geodistance2(user_latitude, user_longitude, ven.vendor_lat, ven.vendor_long) < min_checkpoint:
                checkpoint_lat = ven.vendor_lat
                checkpoint_long = ven.vendor_long
                primary_vendor = ven
                min_checkpoint = geodistance2(user_latitude, user_longitude,
                                              ven.vendor_lat, ven.vendor_long)
                # inside_2_km = 1
    print("inside", cell_inside)
    # jo 1 km ke ander hai
    if(cells == []):
        # bacha hai
        max_distance = 0
        for v1, d1 in zip(cell_inside, dist_inside):
            if(d1 >= max_distance):
                farthest_cell = v1
                max_distance = d1
    # unme se farthest distance nikal li
        while True:
            firstmin = deliveryBoy_list[0]
            for i in range(0, len(deliveryBoy_list)):
                if geodistance2(deliveryBoy_list[i].lat, deliveryBoy_list[i].long, farthest_cell.Cell_lat, farthest_cell.Cell_long) < geodistance2(firstmin.lat, firstmin.long, farthest_cell.Cell_lat, farthest_cell.Cell_long):
                    firstmin = deliveryBoy_list[i]
            val_cell = []
            val_name = []
            val_address = []
            val_lat = []
            val_long = []
            for ven in vendor_assigned_list:
                if ven.cell in cell_inside:
                    val_cell.append(ven.cell)
                    val_name.append(ven.name)
                    val_address.append(ven.address)
                    val_lat.append(ven.vendor_lat)
                    val_long.append(ven.vendor_long)
            # print(firstmin)
            primaryBoy = firstmin
            print("firstmin", primaryBoy)
            data = {
                "order_id": str(order_id),
                "vendor_name": val_name,
                "vendor_address": val_address,
                "vendor_lat": val_lat,
                "vendor_long": val_long,
                "vendor_cell": val_cell,
                "checkpoint_lat": checkpoint_lat,
                "checkpoint_long": checkpoint_long,
                "user_latitude": user_latitude,
                "user_longitude": user_longitude,
                "user_phone": phone_no,
                "split": False,
                "isprimary": True
            }
            print(data)
            send_delivery_order(data, primaryBoy.phone_no)
            print("waiting for 30 seconds")
            time.sleep(60)
            if primaryBoy.accepted_or_not == True:
                break
        for v1 in cell_inside:
            final_vendor_cell.append(v1)
            final_deliverBoy.append(primaryBoy)
        return final_vendor_cell, final_deliverBoy, primaryBoy

    primary_boy_selected = 0
    # this_has_pcell = 0
    # print("delivery list", deliveryBoy_list)
    while True:
        count_sector = 0
        # print("delivery list", deliveryBoy_list)
        while True:
            max_u2d = 0
            if deliveryBoy_list == []:
                for cell in reversed(cells):
                    cell_inside.append(cell)
                    cells.remove(cell)
                break
            for vendor_cell, dist in zip(reversed(cells), reversed(cell_distance)):
                # if vendor_cell in final_vendor_cell:
                #     continue
                count_sector = count_sector+1
                print("vendor_cell", vendor_cell)
                cells.remove(vendor_cell)
                cell_distance.remove(dist)
                max_u2c = dist
                farthest_cell = vendor_cell

                vendor_cell_sector = []
                vendor_cell_dist = []
                pos_v = []
                neg_v = []
                pos_d = []
                neg_d = []
            # if vendor_cell == pcell:
            #     this_has_pcell = 1
                for cell, d1 in zip(reversed(cells), reversed(cell_distance)):
                    # if (v1 not in final_vendor_cell):
                    #     if v1!=vendor_cell:
                    angle, sign = sector_check(vendor_cell.Cell_lat, vendor_cell.Cell_long,
                                               user_latitude, user_longitude, cell.Cell_lat, cell.Cell_long)
                    # print(angle, sign)
                    if abs(angle) < 30:
                        if sign == 0:
                            pos_v.append(cell)
                            pos_d.append(d1)
                        else:
                            neg_v.append(cell)
                            neg_d.append(d1)
                if len(pos_v) > len(neg_v):
                    for v1, d1 in zip(pos_v, pos_d):
                        # print("inside if_poslen", v1)
                        vendor_cell_sector.append(v1)
                        vendor_cell_dist.append(d1)
                        cells.remove(v1)
                        cell_distance.remove(d1)
                        if(d1 > max_u2c):
                            max_u2c = d1
                            farthest_cell = v1

                else:
                    for v1, d1 in zip(neg_v, neg_d):
                        # print("inside if_neglen", v1)
                        vendor_cell_sector.append(v1)
                        vendor_cell_dist.append(d1)
                        cells.remove(v1)
                        cell_distance.remove(d1)

                        if(d1 > max_u2c):
                            max_u2c = d1
                            farthest_cell = v1
                print("vendor_cell_sector", vendor_cell_sector)
                # print("farthest_cell", farthest_cell)
                if deliveryBoy_list == []:
                    for cell in reversed(cells):
                        cell_inside.append(cell)
                        cells.remove(cell)
                    break
                min = 10000
                for boy in deliveryBoy_list:
                    d = geodistance2(
                        boy.lat, boy.long, farthest_cell.Cell_lat, farthest_cell.Cell_long)
                    if(d < min):
                        min = d
                        closestBoy = boy
                # print(cells)
                # print(closestBoy)
                # print("dist+min", dist+min)
                if (max_u2c+min) > max_u2d and primary_boy_selected == 0:
                    max_u2d = (max_u2c+min)
                    # print("min_u2d", max_u2d)
                    primaryBoy = closestBoy

                for vcs, dista in zip(vendor_cell_sector, vendor_cell_dist):
                    final_deliverBoy.append(closestBoy)
                    final_vendor_cell.append(vcs)
                    final_distance_cell.append(dista)

                final_deliverBoy.append(closestBoy)
                final_vendor_cell.append(vendor_cell)
                final_distance_cell.append(dist)
                # print(deliveryBoy_list)
                deliveryBoy_list.remove(closestBoy)
            if cells == []:
                break
        # print("primary boy selected", primary_boy_selected)
        # print("primary boy", primaryBoy)
        if primary_boy_selected == 0:
            for v1, d1 in zip(cell_inside, dist_inside):
                final_vendor_cell.append(v1)
                final_distance_cell.append(d1)
                final_deliverBoy.append(primaryBoy)
        print("before acc", final_vendor_cell)
        print("before acc", final_deliverBoy)
        # print(final_distance_cell)
        unique_deliver_boy = unique(final_deliverBoy)
        for boy in unique_deliver_boy:
            # indices = [i for i, x in enumerate(final_deliverBoy) if x == boy]
            # if boy.accepted_or_not == 0:
            vendor_list = []
            vendor_address = []
            vendor_lat = []
            vendor_long = []
            val_cell = []

            for boy2, cell in zip(final_deliverBoy, final_vendor_cell):
                if boy == boy2:
                    for ven in vendor_assigned_list:
                        if ven.cell == cell:
                            vendor_list.append(ven.name)
                            vendor_address.append(ven.address)
                            vendor_lat.append(ven.vendor_lat)
                            vendor_long.append(ven.vendor_long)
                            val_cell.append(ven.cell)
            if boy == primaryBoy:
                isprimary = True
                primary_boy_selected = 1
            else:
                isprimary = False
            data = {
                "order_id": str(order_id),
                "vendor_name": vendor_list,
                "vendor_address": vendor_address,
                "vendor_lat": vendor_lat,
                "vendor_long": vendor_long,
                "checkpoint_lat": checkpoint_lat,
                "checkpoint_long": checkpoint_long,
                "user_latitude": user_latitude,
                "user_longitude": user_longitude,
                "user_phone": phone_no,
                "split": count_sector > 1,
                "isprimary": isprimary,
                "val_cell": val_cell
            }
            print("boy", boy)
            send_delivery_order(data, boy.phone_no)
            # print("data",data)
        # this_has_pcell = 0
        print("primary boy", primaryBoy)
        print("waiting for 30 seconds")
        time.sleep(60)
        flag = 0
        print("final", final_vendor_cell, "final", final_deliverBoy)
        fvc = []
        fdb = []
        fdc = []
        for boy2, cell, dist in zip(final_deliverBoy, final_vendor_cell, final_distance_cell):
            fdb.append(boy2)
            fvc.append(cell)
            fdc.append(dist)
        for boy2, cell, dist in zip(final_deliverBoy, final_vendor_cell, final_distance_cell):
            # print(boy2.accepted_or_not)
            boy3 = Delivery_Boys.objects.get(phone_no=boy2.phone_no)
            if boy3.accepted_or_not == False:
                # print("boy3", boy3)
                # print("primaryBoy", primaryBoy)
                if boy3 == primaryBoy:
                    primary_boy_selected = 0
                fdb.remove(boy3)
                fvc.remove(cell)
                fdc.remove(dist)
                if cell not in cell_inside:
                    cells.append(cell)
                    cell_distance.append(dist)
                flag = 1
            if boy3.accepted_or_not == False and deliveryBoy_list == []:
                return [], [], boy3
        final_deliverBoy = fdb
        final_vendor_cell = fvc
        final_distance_cell = fdc
        if flag == 0:
            break
        print(cells)
        print(cell_distance)
    for cell in cell_inside:
        if cell not in final_vendor_cell:
            final_vendor_cell.append(cell)
            final_deliverBoy.append(primaryBoy)
    print("final2", final_vendor_cell, "final2", final_deliverBoy)
    print("checkpoint: ", checkpoint_lat, " ", checkpoint_long)
    return final_vendor_cell, final_deliverBoy, primaryBoy


def create_vendor_assigned_list(order_id):
    print("calling vendor assigned list")
    print("order id:", order_id)
    ven = []
    orders = prev_orders.objects.filter(order_id=order_id)
    for order in orders:
        if order.status == 'A':
            vendor = Vendors.objects.get(phone_no=order.vendor_phone)
            ven.append(vendor)
    ven = unique(ven)
    return ven


def create_vendor_assigned_list_sub(sorder_id):
    ven = []
    orders = Subscribed_Order_Items.objects.filter(sorder_id=sorder_id)
    for order in orders:
        ven.append(order.vendor_phone)
    ven = unique(ven)
    return ven


def place_order(request):
    if request.method == 'POST':

        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        print(body)
        items = body['items']
        city = body['city']
        user_latitude = float(body['order_lat'])
        user_longitude = float(body['order_long'])
        payment_done = body['payment_done']
        order_id = body['order_id']

        print(items)
        # items ki detail ayi
        ar2 = []
        buckets = []
        for i in range(0, 50):
            ar2.append(0)
        products = 0
      #  print(request.POST.getlist('items'))
        for item in items:
            prodid = CategorizedProducts.objects.get(
                product_name=item['product_name']).product_id
            itemcount = int(item['itemcount'])
            ar2[prodid] = itemcount
            products = products | (1 << prodid)
        print(ar2)
        # yaha tak
        if order_id == "":
            order_id = uuid.uuid4()
            print(order_id)

            Orders.objects.create(
                customer_phone=RegUser.objects.get(phone_no=body['phone_no']),
                order_id=order_id,
                address=body['address'],
                cust_lat=user_latitude,
                cust_long=user_longitude,
                pending_order=products
            )
        if payment_done == "0":
            response = {'success': 'False',
                        "order_id": order_id}
            return JsonResponse(response, safe=False)
        i = 0
        #cells = list(Cells.objects.filter(city__iexact = city))
        cells_all = list((Cells.objects.filter(city__iexact=city)))

        vendor_assigned_list = []
        no = 0
        ord = products
        while ord != 0 and no < 2:
            cells = []
            cellpro = []
            for cell in cells_all:
                d = (geodistance2(user_latitude, user_longitude,
                                  cell.Cell_lat, cell.Cell_long))  # isko geohash karna hai
                pro = 0
                if d <= 7:
                    cells.append(cell)
                    vendors_all = list(
                        Vendors.objects.filter(cell=cell))
                    not_vendors = list(
                        prev_orders.objects.filter(order_id=order_id))
                    notvens = []
                    for notven in not_vendors:
                        notvens.append(notven.vendor_phone)
                    # print(notvens)
                    for vendor in vendors_all:
                        # if vendor.current_no_orders < 5:
                        if vendor.phone_no not in notvens:
                            pro = pro | vendor.items
                    cellpro.append(pro)
            print(cells)
            print(cellpro)
            latest_sit = cell_sort(cells, cellpro, deepcopy(
                ar2), user_latitude, user_longitude, city, order_id, ord)
            print("one complete")
            no = no + 1
            time.sleep(60)
            ord = Orders.objects.get(order_id=order_id).pending_order
            print("ord = ", ord)

        vendor_assigned_list = create_vendor_assigned_list(order_id)
        print("final vendor list")
        print(vendor_assigned_list)

        cell_final = []
        cell_dist_final = []

        for ven in vendor_assigned_list:
            if ven.cell not in cell_final:
                cell_final.append(ven.cell)
                d = (geodistance2(user_latitude, user_longitude,
                                  ven.cell.Cell_lat, ven.cell.Cell_long))
                cell_dist_final.append(d)
        print("cell_final")
        print(cell_final)
        print(cell_dist_final)

        left_products = []
        successful_orders = []
        for x in range(0, 50):
            if ord >> x & 1:
                left_products.append(
                    CategorizedProducts.objects.get(product_id=x).product_name)
            elif products >> x & 1:
                successful_orders.append(
                    CategorizedProducts.objects.get(product_id=x).product_name)

        if vendor_assigned_list != []:
            final_vendor_cell, final_deliverBoy, primaryBoy = delivery_boy_assignment(
                vendor_assigned_list, cell_final, cell_dist_final, user_latitude, user_longitude, city, body['phone_no'], order_id)
            if final_vendor_cell == []:
                print("no del boy del")
                return JsonResponse({'msg': 'no delivery boy selected'})
            i = 0
            # if products==0:
            print(final_vendor_cell, "fdv", final_deliverBoy, "fvd", primaryBoy)
            for ven in vendor_assigned_list:
                otp = int(random()*100000)
                ven_accepted_order = prev_orders.objects.filter(
                    vendor_phone=ven.phone_no).filter(order_id=order_id, status='A')
                for ven_order in ven_accepted_order:
                    delivery_boy_phone = final_deliverBoy[final_vendor_cell.index(
                        ven.cell)]
                    if delivery_boy_phone == primaryBoy:
                        value = "P"
                    else:
                        value = "S"
                    print(ven_order)
                    # obj = CategorizedProducts.objects.get(
                    #     product_id=ven_order)
                    Order_Items.objects.create(
                        product_id=ven_order.product_id,
                        quantity=ar2[int(ven_order.product_id)],
                        order_id=order_id,
                        delivery_boy_phone=final_deliverBoy[final_vendor_cell.index(
                            ven.cell)],
                        delboy_type=value,
                        vendor_phone=ven.phone_no,
                        otp=otp
                    )
                    # fcm_token = Vendors.objects.get(phone_no=ven.phone_no).vendor_fcm_token
                    # send_notification(fcm_token=fcm_token, data_content={"order_id": order_id,
                    #                                                      "otp": otp})

            response = {
                #       'success': 'true',
                'order_id': order_id,
                'primaryBoy_name': primaryBoy.name,
                'primaryBoy_phone': primaryBoy.phone_no,
                "left_prod": left_products,
                "successful_orders": successful_orders
            }

            return JsonResponse(response)
        else:
            response = {'success': 'False',
                        "msg": 'none accepted'}
            return JsonResponse(response, safe=False)


def subscribe_order(request):
    if request.method == 'POST':
        print(request.POST)
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        sorder_id = uuid.uuid4()
        items = body['items']
        duration = body['duration']
        days = body['days']
        city = body['city']
        del_time = body['del_time']
        ar2 = []
        buckets = []
        for i in range(0, 50):
            ar2.append(0)
        products = 0

      #  print(request.POST.getlist('items'))
        for item in items:
            prodid = CategorizedProducts.objects.get(
                product_name=item['product_name']).product_id
            itemcount = int(item['itemcount'])
            ar2[prodid] = itemcount
            products = products | (1 << prodid)

        ord = products
        print(ord)
        Subscribed_Orders.objects.create(
            sorder_id=sorder_id,
            customer_phone=RegUser.objects.get(
                phone_no=body['phone_no']),
            address=body['address'],
            delivery_dates=days,
            delivery_time=del_time,
            pending_order=products,
            duration=duration,
            status='A',
            cust_lat=body['cust_lat'],
            cust_long=body['cust_long'],
            end_date=body['end_date']
        )
        print(sorder_id)
        user_latitude = float(body['cust_lat'])
        user_longitude = float(body['cust_long'])
        cells_all = list((Cells.objects.filter(city__iexact=city)))
        no = 0
        ord = products
        while ord != 0 and no < 2:
            cells = []
            cellpro = []
            for cell in cells_all:
                d = (geodistance2(user_latitude, user_longitude,
                                  cell.Cell_lat, cell.Cell_long))  # isko geohash karna hai
                pro = 0
                if d <= 7:
                    cells.append(cell)
                    vendors_all = list(
                        Vendors.objects.filter(cell=cell))
                    not_vendors = list(
                        prev_orders.objects.filter(order_id=sorder_id))
                    notvens = []
                    for notven in not_vendors:
                        notvens.append(notven.vendor_phone)
                    # print(notvens)
                    for vendor in vendors_all:
                        # if vendor.current_no_orders < 5:
                        if vendor.phone_no not in notvens:
                            pro = pro | vendor.items
                    cellpro.append(pro)
            print(cells)
            print(cellpro)
            latest_sit = cell_sort_sub(cells, cellpro, deepcopy(
                ar2), user_latitude, user_longitude, city, sorder_id, ord, duration, days, del_time)
            print("one complete")
            no = no + 1
            time.sleep(60)
            ord = Subscribed_Orders.objects.get(
                sorder_id=sorder_id).pending_order
            print("ord = ", ord)

        vendors_assigned = create_vendor_assigned_list_sub(sorder_id)
        print(vendors_assigned)
        min = 0
        far_ven = vendors_assigned[0]
        for ven in vendors_assigned:
            d = (geodistance2(user_latitude, user_longitude,
                              cell.Cell_lat, cell.Cell_long))
            if d > min:
                far_ven = ven
                min = d

        sord = Subscribed_Orders.objects.get(sorder_id=sorder_id)
        sord.far_vendor = far_ven
        sord.save()
        left_products = []
        successful_orders = []
        for x in range(0, 50):
            if ord >> x & 1:
                left_products.append(
                    CategorizedProducts.objects.get(product_id=x).product_name)
            elif products >> x & 1:
                successful_orders.append(
                    CategorizedProducts.objects.get(product_id=x).product_name)
        response = {'sorder_id': sorder_id,
                    'left_products': left_products,
                    'successful_orders': successful_orders
                    }

        return JsonResponse(response)


def subscribe_order2(request):
    if request.method == 'POST':
        print(request.POST)
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        sorder_id = body['sorder_id']
        sorders = Subscribed_Order_Items.objects.filter(sorder_id=sorder_id)
        print(sorders)
        sord = Subscribed_Orders.objects.get(sorder_id=sorder_id)
        city = body['city']
        if (not len(firebase_admin._apps)):
            cred = credentials.Certificate("serviceAccountKey.json")
            firebase_admin.initialize_app(cred)
        db = firestore.client()
        deliveryBoy_list = list(Delivery_Boys.objects.filter(
            city__iexact=city, status="A"))  # busy="true"

        for boy in deliveryBoy_list:
            doc_rf = db.collection(u'DeliveryBoyLocation').document(
                u'{}'.format(boy.phone_no))
            doc = doc_rf.get()
            boy.lat = doc.to_dict()['geo_point'].latitude
            boy.long = doc.to_dict()['geo_point'].longitude
            print("boy lat long", boy.lat, boy.long)
            boy.save()
        order_details = []
        for sorder in sorders:
            d = {
                'vendor_lat': sorder.vendor_phone.vendor_lat,
                'vendor_long': sorder.vendor_phone.vendor_long,
            }
            print("creating model")
            Vendors_subs.objects.create(
                phone_no=sorder.vendor_phone,
                sorder_id=sorder_id,
                vendor_status='N',
                otp=int(random() * 100000)
            )
            order_details.append(d)
        data = {
            'order_id': str(sorder_id),
            'ispramary': True,
            'val_cell': order_details
        }
        min = 999999
        far_vendor = Subscribed_Orders.objects.get(
            sorder_id=sorder_id).far_vendor
        vens = create_vendor_assigned_list_sub(sorder_id)
        while True:
            if deliveryBoy_list == []:
                return JsonResponse({'msg': 'no del boy available'})
            for boy in deliveryBoy_list:
                d = (geodistance2(boy.lat, boy.long,
                                  far_vendor.vendor_lat, far_vendor.vendor_long))
                if d < min:
                    min = d
                    del_boy = boy
            print(del_boy)
            send_delivery_order(data, del_boy.phone_no)
            time.sleep(60)
            print(del_boy.accepted_or_not)
            if del_boy.accepted_or_not == True:
                data2 = {
                    'del_boy': str(del_boy.name)
                }
                response = beams_client.publish_to_users(
                    user_ids=[str(sord.customer_phone)],
                    publish_body={
                        'fcm': data2
                    },
                )
                break
            else:
                deliveryBoy_list.remove(del_boy)
                min = 999999
        phones = []
        for ven in vens:
            phones.append(str(ven.phone_no))

        #otp = int(random() * 100000)
        Deliverying_Boys_subs.objects.create(
            phone_no=del_boy,
            sorder_id=sorder_id,
            #otp=otp
        )
        response = beams_client.publish_to_users(
            user_ids=phones,
            publish_body={
                'fcm': data2
            },
        )
        return JsonResponse(data2)


def save_address(request):
    if request.method == "POST":
        address_id = uuid.uuid4()
        print(address_id)
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body['phone_no'])
        Addresses.objects.create(
            address_id=address_id,
            address=body['address'],
            pincode=body['pincode'],
            phone_no=RegUser.objects.get(phone_no=body['phone_no']),
            latitude=body['latitude'],
            longitude=body['longitude'],
            category=body['category'],
            city=body['city']
        )
        return JsonResponse({"success":"true"})




# class save_address(APIView):
#     def post(self, request):
#         response = JsonResponse({'Error': 'True'})
#         add_serializer = RegAddresses(data=request.data)
#         if add_serializer.is_valid():
#             add_serializer.save()
#             return JsonResponse(add_serializer.data)
#         return JsonResponse(add_serializer.errors)
#
#
# class get_address(APIView):
#     def post(self, request):
#         address = (list(Addresses.objects.filter(
#             phone_no=request.POST['phone_no']).values()))
#         return JsonResponse(address, safe=False)


def get_products(request):
    # body=request.body.decode('utf-8')
    # print(json.loads(body)['city'])

    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        mlong = float(body['longitude'])
        mlat = float(body['latitude'])
        mcity = body['city']
        print(mcity)

        cells = Cells.objects.filter(city__iexact=mcity)
        # print(vendors)
        #vendors = Vendors.objects.filter(city__iexact = mcity)
        # print(vendors)
        # selected_vendors = []
        myProducts = []
        x = 0
        for cell in cells:
            print(type(mlat))
            if geodistance2(mlat, mlong, cell.Cell_lat, cell.Cell_long) < 7:
                x = x | cell.Cell_products

        for z in range(0, 50):
            if x >> z & 1:
                pro_name = CategorizedProducts.objects.get(
                    product_id=z).product_name
                obj = CategorizedProducts.objects.get(
                    product_name=pro_name)
                d = {}
                d["under_category"] = obj.under_category.categoryName
                d["product_name"] = obj.product_name
                d["product_id"] = obj.product_id
                d["product_price"] = obj.product_price
                d["product_rating"] = obj.product_rating
                d["product_descp"] = obj.product_descp
                # y = json.loads(d.replace("\"",''))
                # list1=[]
                myProducts.append((d))
            # myProducts.add(list1)
        myProducts = unique(myProducts)
        print(myProducts)
        dict = {"Prod": (myProducts)}

        return JsonResponse(dict, safe=False)

    else:
        return JsonResponse({'error': 'Not a POST request'})


# def update_order(orderid, vendors, products, d_boys):
#     orders = Orders.objects.filter(order_id=orderid)
#     pl = len(products)
#     for i in range(vl):
#         pll = len(products[i])
#         for j in range(vll):
#             plll = len(products[i][j])
#             for k in pll:
#                 obj = orders.get(product_id=products[i][j][k])
#                 obj.update(vendor_phone=vendors[i][j],
#                            delivery_boy_phone=Delivery_Boys.objects.get(phone_no=d_boys[i][j]))


def vendor_response(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        ar1 = body['items']
        phone = body['vendor_phone']
        order_id = body['order_id']
        items_ordered = 0
        print(ar1)
        orders = Orders.objects.get(order_id=order_id)
        for item in ar1:
            print(item)
            item_num = CategorizedProducts.objects.get(
                product_name=item).product_id
            print(item_num)
            items_ordered = items_ordered | (1 << item_num)
        print("items ordered", items_ordered)
        previous_order_state = orders.pending_order
        print("previous", previous_order_state)
        new_pending_order = items_ordered ^ previous_order_state
        new_pending_order = new_pending_order & previous_order_state
        print("new", new_pending_order)
        orders.pending_order = new_pending_order
        current_order_state = new_pending_order
        products_selected_vendor = Vendors.objects.get(phone_no=phone).items
        orders.save()
        print(products_selected_vendor)
        for x in range(0, 40):
            if products_selected_vendor >> x & 1:
                print('Entering for ', x)
                try:
                    itemin = CategorizedProducts.objects.get(
                        product_id=x).product_name
                    print(itemin)
                    if previous_order_state >> x & 1 and current_order_state >> x & 1 and products_selected_vendor >> x & 1:
                        prev_orders.objects.create(
                            order_id=order_id, vendor_phone=phone, product_id=x, status="R")
                        print("rejecting")
                    if previous_order_state >> x & 1 and current_order_state >> x & 1 == 0 and products_selected_vendor >> x & 1:
                        prev_orders.objects.create(
                            order_id=order_id, vendor_phone=phone, product_id=x, status="A")
                        print("accepting")
                except:
                    print("product not found")
        ven = Vendors.objects.get(phone_no=phone)
        curr_no_orders = ven.current_no_orders
        ven.current_no_orders = curr_no_orders + 1
        total_no_orders = ven.total_no_orders
        ven.total_no_orders = total_no_orders + 1
        ven.save()
        return JsonResponse({'success': 'Accepted'})


def suscription_response(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        ar1 = body['items']
        phone = body['vendor_phone']
        sorder_id = body['sorder_id']
        items_ordered = 0
        orders = Subscribed_Orders.objects.get(sorder_id=sorder_id)
        for item in ar1:
            item_num = CategorizedProducts.objects.get(
                product_name=item).product_id
            items_ordered = items_ordered | (1 << item_num)

        previous_order_state = orders.pending_order
        print(previous_order_state)
        print(items_ordered)
        new_pending_order = items_ordered ^ previous_order_state
        print("mid", new_pending_order)
        new_pending_order = new_pending_order & previous_order_state
        orders.pending_order = new_pending_order
        current_order_state = new_pending_order
        ven = Vendors.objects.get(phone_no=phone)
        products_selected_vendor = ven.items
        orders.save()
        for x in range(0, 40):
            if products_selected_vendor >> x & 1:
                itemin = CategorizedProducts.objects.get(
                    product_id=x).product_name
                if previous_order_state >> x & 1 and current_order_state >> x & 1 and products_selected_vendor >> x & 1:
                    prev_orders.objects.create(
                        order_id=sorder_id, vendor_phone=phone, product_id=x, status="R")
                if previous_order_state >> x & 1 and current_order_state >> x & 1 == 0 and products_selected_vendor >> x & 1:
                    Subscribed_Order_Items.objects.create(
                        sorder_id=sorder_id, vendor_phone=ven, product_id=x)
                    prev_orders.objects.create(
                        order_id=sorder_id, vendor_phone=phone, product_id=x, status="A")
        print("pending vr = ", new_pending_order)
        return JsonResponse({'success': 'Accepted'})


def deliver_response(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        phone = body['phone_no']
        order_id = body['order_id']
        accepted = int(body['accepted'])
        print(accepted)
        deli = Delivery_Boys.objects.get(phone_no=phone)
        if accepted == 1:
            DeliveryBoyOrders.objects.create(
                del_boy_no = phone,
                order_id = order_id,
                accepted = True
            )
            deli.accepted_or_not = True
            deli.save()
            print(deli.accepted_or_not)
            return JsonResponse({'success': 'Accepted'})
        else:
            deli.accepted_or_not = False
            deli.save()
            return JsonResponse({'success': 'not_accepted'})


def get_completed_sorder_history(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        objs = Subscribed_Orders.objects.filter(
            customer_phone=RegUser.objects.get(phone_no=body['cust_phone']), status='E')
        cust_sorders = list(objs)
        no_sorders = len(cust_sorders)
        obj_list = []
        print(cust_sorders)
        for i in range(no_sorders):
            print(i, cust_sorders[i].sorder_id)
            d = {}
            ord = Subscribed_Order_Items.objects.filter(
                sorder_id=cust_sorders[i].sorder_id)
            print(ord)
            del_boy_subs = Deliverying_Boys_subs.objects.filter(sorder_id=cust_sorders[i].sorder_id).order_by('order_date',
                                                                                                           'order_time')
            delivery_dates = []
            delivery_times = []
            for boy in del_boy_subs:
                delivery_dates.append(boy.order_date)
                delivery_times.append(boy.order_time)
            d["sorder_id"] = cust_sorders[i].sorder_id
            # print(d["sorder_id"])
            d["cust_delivery_time"] = cust_sorders[i].delivery_time
            d["cust_delivery_dates"] = cust_sorders[i].delivery_dates
            d["order_date"] = cust_sorders[i].order_date
            d["order_time"] = cust_sorders[i].order_time
            d["end_date"] = cust_sorders[i].end_date
            d["delivery_dates"] = delivery_dates
            d["delivery_time"] = delivery_times
            print(d)
            items = []
            for ob in ord:
                obj = CategorizedProducts.objects.get(
                    product_id=ob.product_id)
                if len(ord) == 1:
                    imageurl = CategorizedProducts.objects.get(
                        product_id=0).product_imagepath.url
                else:
                    imageurl = obj.product_imagepath.url
                prod = {
                    'prod_id': obj.product_id,
                    'prod_name': obj.product_name,
                    'category_name': obj.under_category.categoryName,
                    'category_id': obj.under_category.categoryId,
                    'prod_price': obj.product_price,
                    'prod_rating': obj.product_rating,
                    'prod_desc': obj.product_descp,
                    # 'prod_img': obj.product_imagepath,
                    'prod_img': imageurl,
                    'check': False
                }
                items.append(prod)
            d["items"] = items
            print(d)
            obj_list.append(d)
        data = {
            'no_orders': no_sorders,
            'orders': obj_list
        }
        return JsonResponse(data)


def get_active_sorder_history(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        objs = Subscribed_Orders.objects.filter(
            customer_phone=RegUser.objects.get(phone_no=body['cust_phone']), status='A')
        cust_sorders = list(objs)
        no_sorders = len(cust_sorders)
        obj_list = []
        print(cust_sorders)
        for i in range(no_sorders):
            print(i, cust_sorders[i].sorder_id)
            d = {}
            ord = Subscribed_Order_Items.objects.filter(
                sorder_id=cust_sorders[i].sorder_id)
            print(ord)
            del_boy_subs = Deliverying_Boys_subs.objects.filter(sorder_id=cust_sorders[i].sorder_id).order_by('order_date', 'order_time')
            delivery_dates = []
            delivery_times = []
            for boy in del_boy_subs:
                delivery_dates.append(boy.order_date)
                delivery_times.append(boy.order_time)
            d["sorder_id"] = cust_sorders[i].sorder_id
            #print(d["sorder_id"])
            d["cust_delivery_time"] = cust_sorders[i].delivery_time
            d["cust_delivery_dates"] = cust_sorders[i].delivery_dates
            d["order_date"] = cust_sorders[i].order_date
            d["order_time"] = cust_sorders[i].order_time
            d["end_date"] = cust_sorders[i].end_date
            d["delivery_dates"] = delivery_dates
            d["delivery_time"] = delivery_times
            print(d)
            items = []
            for ob in ord:
                obj = CategorizedProducts.objects.get(
                    product_id=ob.product_id)
                if len(ord) == 1:
                    imageurl = CategorizedProducts.objects.get(
                        product_id=0).product_imagepath.url
                else:
                    imageurl = obj.product_imagepath.url
                prod = {
                    'prod_id': obj.product_id,
                    'prod_name': obj.product_name,
                    'category_name': obj.under_category.categoryName,
                    'category_id': obj.under_category.categoryId,
                    'prod_price': obj.product_price,
                    'prod_rating': obj.product_rating,
                    'prod_desc': obj.product_descp,
                    # 'prod_img': obj.product_imagepath,
                    'prod_img': imageurl,
                    'check': False
                }
                items.append(prod)
            d["items"] = items
            print(d)
            obj_list.append(d)
        data = {
            'no_orders': no_sorders,
            'orders': obj_list
        }
        return JsonResponse(data)


def send_saved_address(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        phone_no = body['phone_no']
        addresses = Addresses.objects.filter(phone_no=phone_no)
        final = []
        for address in addresses:
            d ={}
            d['address'] = address.address
            d['pincode'] = address.pincode
            d['city'] = address.city
            d['latitude'] = address.latitude
            d['category'] = address.category
            d['longitude'] = address.longitude
            final.append(d)
        return JsonResponse({
            'address': final
        })


def update_subscribed_delivery_time(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        sorder_id = body['sorder_id']
        sorder = Subscribed_Orders.objects.get(sorder_id=sorder_id)
        sorder.delivery_time = body['delivery_time']
        sorder.save()
        return JsonResponse({
            'success': 'True'
        })


def get_customer_details(request):
    if request.method == 'GET':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        phone_no = body['phone_no']
        user = RegUser.objects.get(phone_no=phone_no)
        data = {
            'name': str(user.first_name+" "+ user.last_name),
            'phone_no': phone_no,
            'email': user.email
        }
        return JsonResponse(data)