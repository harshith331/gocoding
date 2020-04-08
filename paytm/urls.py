from django.conf.urls import include, url
from paytm import views
from django.urls import path

urlpatterns = [
    # Examples:
    path('paytm/', views.home, name='home'),
    path('paytm/payment/', views.payment, name='payment'),
    path('paytm/response/', views.response, name='response'),
    path('charge/', views.app_charge, name='razor'),
    path('charge-razor/', views.razor_final, name='razor-final'),
]
