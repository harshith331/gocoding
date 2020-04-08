from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Orders)
admin.site.register(Order_Items)
admin.site.register(RegUser)
admin.site.register(Category)
admin.site.register(CategorizedProducts)
admin.site.register(Addresses)
admin.site.register(Vendors)
admin.site.register(Cells)
admin.site.register(Serving_Vendors)
admin.site.register(Delivery_Boys)
admin.site.register(Deliverying_Boys)
admin.site.register(Subscribed_Orders)
admin.site.register(Subscribed_Order_Items)
admin.site.register(geohash_distance)
admin.site.register(Deliverying_Boys_subs)
admin.site.register(Vendors_subs)


class OrdersAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'product_id', 'customer_phone', 'order_time')
