from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('items/', get_item_list, name='get-item-list'),
    path('items/create/', create_item, name='create-item'),
    path('stocks/', stock_levels, name='stock-levels'),
    path('items/<uuid:item_id>/', item_detail, name='item-detail'),

]
