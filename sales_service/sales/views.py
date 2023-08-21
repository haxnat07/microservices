from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from .models import Order
from .serializers import OrderSerializer
from django.views.decorators.csrf import csrf_exempt
import requests 

@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def order_list(request):
    if request.method == 'GET':
        user_orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(user_orders, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            item_id = serializer.validated_data['item_id'] 
            quantity = serializer.validated_data['quantity']
            
            try:
                response = requests.get(f'http://127.0.0.1:8001/items/{item_id}/')
                if response.status_code == 200:
                    item_data = response.json()
                    if item_data['quantity'] >= quantity:
                        serializer.save(user=request.user)
                        
                        update_data = {'quantity': item_data['quantity'] - quantity}
                        requests.patch(f'http://127.0.0.1:8001/items/{item_id}/', json=update_data)
                        
                        return Response(serializer.data, status=201)
                    else:
                        return Response({"message": "Out of stock."}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"message": "Item not found."}, status=status.HTTP_400_BAD_REQUEST)
            except requests.exceptions.RequestException as e:
                return Response({"message": "Error communicating with warehouse microservice."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        return Response(serializer.errors, status=400)
