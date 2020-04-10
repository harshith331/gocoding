from django.contrib import admin
from .models import *

# Register your models here.
class Order_ItemsAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'product_id', 'quantity')
    list_display_links = ('order_id', 'product_id')
    list_filter = ('product_id',)

class Subscribed_Order_ItemsAdmin(admin.ModelAdmin):
    list_display = ('sorder_id', 'product_id', 'quantity', 'vendor_phone')
    list_display_links = ('sorder_id',)
    list_filter = ('product_id',)

class Deliverying_Boys_subsAdmin(admin.ModelAdmin):
    list_display = ('phone_no', 'sorder_id', 'order_date')
    list_display_links = ('phone_no',)
    list_filter = ('order_date', )

class AddressesAdmin(admin.ModelAdmin):
    list_display = ('phone_no', 'latitude', 'longitude', 'category')
    list_display_links = ('phone_no',)
    list_filter = ('city', 'category')

class OrdersAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'order_date', 'order_time', 'customer_phone')
    list_display_links = ('order_id',)
    list_filter = ('order_date',)

admin.site.register(Orders, OrdersAdmin)
admin.site.register(Order_Items, Order_ItemsAdmin)
admin.site.register(RegUser)
admin.site.register(Category)
admin.site.register(CategorizedProducts)
admin.site.register(Addresses, AddressesAdmin)
admin.site.register(Vendors)
admin.site.register(Cells)
admin.site.register(Serving_Vendors)
admin.site.register(Delivery_Boys)
admin.site.register(Deliverying_Boys)
admin.site.register(Subscribed_Orders)
admin.site.register(Subscribed_Order_Items, Subscribed_Order_ItemsAdmin)
admin.site.register(geohash_distance)
admin.site.register(Deliverying_Boys_subs, Deliverying_Boys_subsAdmin)
admin.site.register(Vendors_subs)


class OrdersAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'product_id', 'customer_phone', 'order_time')
