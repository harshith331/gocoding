from django.contrib import admin
from .models import *

class prev_ordersAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'product_id', 'order_status', 'status')
    list_display_links = ('order_id', )
    list_editable = ('product_id', 'order_status', 'status')

admin.site.register(prev_orders, prev_ordersAdmin)
