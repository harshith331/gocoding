from django.db import models
from django.utils import timezone
import uuid
import json


class RegUser(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_no = models.CharField(primary_key=True, max_length=15)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    customer_fcm_token = models.CharField(max_length=500, default="")


class Category(models.Model):
    categoryId = models.IntegerField(primary_key=True)
    categoryName = models.CharField(max_length=255)
    categoryImagePath = models.CharField(max_length=255)

    def __str__(self):
        return self.categoryName


class CategorizedProducts(models.Model):
    under_category = models.ForeignKey(Category, on_delete=models.PROTECT)
    product_name = models.CharField(unique=True, max_length=255)
    product_id = models.IntegerField(primary_key=True)
    product_price = models.IntegerField()
    product_rating = models.FloatField()
    product_descp = models.CharField(max_length=255)
    product_imagepath = models.ImageField(
        default='default.jpg', upload_to='images/')

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)
    #vendors = models.ManyToManyField(Vendors)

    def __str__(self):
        return str(self.product_id)


class Hotel(models.Model):
    name = models.CharField(max_length=50)
    hotel_Main_Img = models.ImageField(upload_to='images/')


class Addresses(models.Model):
    address_id = models.CharField(primary_key=True, max_length=200)
    # house_no = models.CharField(max_length=10)
    # street = models.CharField(max_length=255)
    # city = models.CharField(max_length=30)
    # landmark = models.CharField(max_length=100)
    address = models.CharField(max_length=350)
    pincode = models.IntegerField()
    phone_no = models.ForeignKey(
        RegUser, to_field='phone_no', on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    category = models.CharField(max_length=100)
    city = models.CharField(max_length=100)


class Cells(models.Model):
    Cell_id = models.CharField(primary_key=True, max_length=15)
    Cell_lat = models.FloatField()
    Cell_long = models.FloatField()
    no_vendor = models.IntegerField()
    Cell_products = models.IntegerField()
    city = models.CharField(unique=False, max_length=255, default="Roorkee")


class Vendors(models.Model):
    name = models.CharField(max_length=255, default="Hemil")
    phone_no = models.CharField(primary_key=True, max_length=255)
    vendor_id = models.CharField(unique=True, max_length=100)
    vendor_lat = models.FloatField()
    vendor_long = models.FloatField()
    address = models.CharField(max_length=500, default="Roorkee")
    city = models.CharField(unique=False, max_length=255)
    cell = models.ForeignKey(
        Cells, on_delete=models.CASCADE, null=True, blank=True)
    geoha = models.CharField(max_length=12)
    STATUS = [
        ('A', 'Active'),
        ('I', 'Inactive'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='I',
    )
    total_no_orders = models.IntegerField(default=0)
    current_no_orders = models.IntegerField(default=0)
    busy = models.CharField(max_length=20, blank=True, null=True)
    items = models.IntegerField(default=0)
    money_earned = models.IntegerField(default=0)
    penalty_money = models.IntegerField(default=0)
    vendor_fcm_token = models.CharField(max_length=500, default="")
    vendor_imagepath = models.ImageField(
           default='toys.png', upload_to='images/')


class Serving_Vendors(models.Model):
    phone_no = models.ForeignKey(
        Vendors, to_field="phone_no", on_delete=models.CASCADE)
    order_id = models.CharField(max_length=500)


class Delivery_Boys(models.Model):
    name = models.CharField(max_length=255)
    phone_no = models.CharField(max_length=255, primary_key=True)
    del_boy_id = models.CharField(max_length=100)
    address = models.CharField(max_length=500)
    STATUS = [
        ('A', 'Active'),
        ('I', 'Inactive'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='I',
    )
    total_no_orders = models.IntegerField()
    current_no_orders = models.IntegerField()
    busy = models.BooleanField(default=False)
    city = models.CharField(unique=False, max_length=255)
    lat = models.FloatField(default=28.33)
    long = models.FloatField(default=77.88)
    accepted_or_not = models.BooleanField(default=False)
    delboy_fcm_token = models.CharField(max_length=500, default="")
    delivery_imagepath = models.ImageField(
         default='toys.png', upload_to='images/')


class Deliverying_Boys(models.Model):
    phone_no = models.ForeignKey(
        Delivery_Boys, to_field='phone_no', on_delete=models.CASCADE)
    order_id = models.CharField(max_length=500)
    vendor_phone = models.ForeignKey(Vendors, on_delete=models.PROTECT)


class Subscribed_Orders(models.Model):
    sorder_id = models.CharField(
        primary_key=False, editable=True, default=uuid.uuid4, max_length=100)
    customer_phone = models.ForeignKey(RegUser, on_delete=models.CASCADE)
    delivery_time = models.CharField(max_length=200, default="11")
    delivery_dates = models.CharField(max_length=200, default="11")
    address = models.CharField(max_length=255)
    STATUS = [
        ('A', 'Active'),
        ('E', 'Expired'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='A')
    cust_lat = models.CharField(max_length=50, blank=True, null=True)
    cust_long = models.CharField(max_length=50, blank=True, null=True)
    far_vendor = models.ForeignKey(
        Vendors, on_delete=models.PROTECT, blank=True, null=True)
    duration = models.CharField(max_length=50, default="1")
    pending_order = models.IntegerField(default=0)
    order_date = models.DateField(auto_now_add=True)
    order_time = models.TimeField(auto_now_add=True)
    COMPLETTION_STATUS = [
        ('C', 'Complete'),
         ('I', 'Incomplete')
     ]
    completion_status = models.CharField(max_length=20, choices=COMPLETTION_STATUS, default='C')
    end_date = models.DateField()


class Deliverying_Boys_subs(models.Model):
    phone_no = models.ForeignKey(
        Delivery_Boys, to_field='phone_no', on_delete=models.CASCADE)
    sorder_id = models.CharField(max_length=500)
    order_date = models.DateField((u"Order date"), auto_now_add=True)
    order_time = models.TimeField((u"Order time"), auto_now_add=True)
    STATUS = [
        ('A', 'Active'),
        ('I', 'Inactive'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='A',
    )
    #otp = models.IntegerField(blank=True, default=0)


class Vendors_subs(models.Model):
    phone_no = models.ForeignKey(
        Vendors, to_field='phone_no', on_delete=models.CASCADE)
    sorder_id = models.CharField(max_length=500)
    order_date = models.DateField((u"Order date"), auto_now_add=True)
    order_time = models.TimeField((u"Order time"), auto_now_add=True)
    VENDOR_STATUS = [
        ('D', 'Delivered'),
        ('N', 'Not Delivered')
    ]
    vendor_status = models.CharField(
        max_length=20, choices=VENDOR_STATUS, default='N')
    DELIVERY_STATUS = [
        ('P', 'Picked'),
        ('N', 'Not Picked')
    ]
    delivery_status = models.CharField(max_length=20, choices=DELIVERY_STATUS, default='N')
    otp = models.IntegerField(blank=True, default=0)



class Subscribed_Order_Items(models.Model):
    sorder_id = models.CharField(
        primary_key=False, editable=True, default=uuid.uuid4, max_length=100)
    vendor_phone = models.ForeignKey(
        Vendors, on_delete=models.PROTECT, blank=True, null=True)
    product_id = models.IntegerField(default=0)
    quantity = models.IntegerField(default=1)


class Orders(models.Model):
    order_id = models.CharField(
        primary_key=False, editable=True, default=uuid.uuid4, max_length=500)
    order_date = models.DateField((u"Order date"), auto_now_add=True)
    order_time = models.TimeField((u"Order time"), auto_now_add=True)
    address = models.CharField(max_length=500)
    customer_phone = models.ForeignKey(
        RegUser, to_field='phone_no', on_delete=models.CASCADE)
    cust_lat = models.CharField(max_length=50, blank=True, null=True)
    cust_long = models.CharField(max_length=50, blank=True, null=True)
    pending_order = models.IntegerField(default=0)
    ORDER_STATUS = (
        ('D', 'Delivered'),
        ('A', 'Active')
    )
    order_status = models.CharField(
        max_length=50, choices=ORDER_STATUS, default='A')
    primary_vendor = models.ForeignKey(
        Vendors, on_delete=models.PROTECT, blank=True, null=True)
    primary_vendor2 = models.CharField(max_length=50, default="123456")
    primary_cell = models.ForeignKey(
        Cells, on_delete=models.PROTECT, blank=True, null=True)
    price = models.IntegerField(default=50)

    def __str__(self):
        return self.order_id


class Order_Items(models.Model):
    order_id = models.CharField(max_length=500)
    product_id = models.IntegerField(default=0)
    quantity = models.IntegerField(default=1)
    delivery_boy_phone = models.ForeignKey(
        Delivery_Boys, on_delete=models.PROTECT, null=True, blank=True)
    deliveryBoy_type = (
        ('P', 'Primary'),
        ('S', 'Secondary')
    )
    delboy_type = models.CharField(
        max_length=50, choices=deliveryBoy_type, default='S')
    vendor_phone = models.CharField(max_length=500, blank=True, null=True)
    otp = models.IntegerField(blank=True, default=0)
    DELIVERY_STATUS = [
        ('P', 'Picked'),
        ('N', 'Not Picked')
    ]
    delivery_status = models.CharField(max_length=20, choices=DELIVERY_STATUS, default='N')


# class iteminfo(models.Model):
#     item_name = models.CharField(max_length=100)
#     item_no = models.IntegerField()


class geohash_distance(models.Model):
    geohash1 = models.CharField(max_length=50)
    geohash2 = models.CharField(max_length=50)
    dist = models.FloatField(default=0)
