from django.urls import path

from . import views

urlpatterns = [
    path('check/', views.check_vendor, name='check'),
    path('save_products/', views.save_vendor_products, name='saveproducts'),
    path('activate/', views.activate, name='activate'),
    path('history/', views.order_history, name='history'),
    path('ongoing/', views.order_ongoing_alt, name='ongoing'),
    # path('send/', views.pusher_check),
    path('get_products/', views.send_all_products, name='getproducts'),
    path('prepared/', views.order_prepared, name='prepared'),
    path('get_prev_products/', views.send_prev_products, name='prevproducts'),
    # path('pusher_auth/', views.pusher_authentication, name='pusherauth'),
    # path('delivery_details/', views.delivery_details, name='deliverydetails'),
    path('dispatch/', views.order_dispatched, name='order_dispatched'),
    path('vendorregister/', views.vendor_register, name='vendor_register'),
    path('send_order_id/', views.send_order_id, name='send_order_id'),
    path('send_order_items/', views.send_order_items, name='send_order_items'),
    path('send_sorder_items/', views.send_subscribed_order_items, name='send_sorder_items'),
    path('product_register/', views.product_register, name='product_register'),
    #path('get_upcoming_subs_order/', views.get_upcoming_subs_order, name='get_upcoming_subs_order'),
]
