from django.urls import path

from . import views

urlpatterns = [

    # path('confirm_order/', views.order_confirm, name='confirmorder'),
    path('vendor_details/', views.vendor_details, name='vendor_details'),
    path('cust_details/', views.cust_details, name='cust_details'),
    path('del_details/', views.del_boy_details, name='del_details'),
    # path('confirm_order/', views.order_confirm, name='confirm_order'),
    path('reached_vendor/', views.reached_vendor, name='reached_vendor'),
    path('pickedup/', views.order_pickedup, name='pickedup'),
    path('reached_customer/', views.reached_customer, name='reached_customer'),
    # path('reached_checkpoint/', views.reached_checkpoint,
    #      name='reached_checkpoint'),
    path('delivered/', views.order_delivered, name='delivered'),
    path('check/', views.check_delivery_boy, name='check'),
    path('activate/', views.activate_delboy, name='activate'),
    path('pusher/beams-auth/', views.beams_auth, name='beams'),
    path('deliveryregister/', views.delivery_register, name='delivery_register'),
    path('deliveryorderhistory/', views.get_deliver_order_history,
         name='get_deliver_order_history'),
    path('getproductdetails/', views.get_product_details,
         name='get_product_details'),
    path('reached_checkpoint/', views.secondary_reached_checkpoint, name='reached_checkpoint'),
    path('get_customer_details/', views.get_customer_details, name='get_customer_details'),
    path('get_checkpoint_details/', views.get_checkpoint_details, name='get_checkpoint_details'),
    path('test_notification/', views.test_notification, name='test_notificaiton'),

]
