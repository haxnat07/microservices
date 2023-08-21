from django.urls import path
from .views import *

urlpatterns = [
    path('orders/', order_list, name='order_list'),
    #path('orders/all/', get_all_orders, name='get-all-orders'),
]