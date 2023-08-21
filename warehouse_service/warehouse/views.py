from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .models import *
from .serializers import *

    
@api_view(['GET'])
@permission_classes([AllowAny]) 
def get_item_list(request):
    items = Item.objects.all()
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAdminUser])  
def create_item(request):
    serializer = ItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def stock_levels(request):
    items = Item.objects.all()
    stock_data = [{'item': item.name, 'quantity': item.quantity} for item in items]
    return Response(stock_data)


@api_view(['GET', 'PATCH'])
def item_detail(request, item_id):
    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        return Response({"message": "Item not found."}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ItemSerializer(item)  
        return Response(serializer.data)
    
    elif request.method == 'PATCH':
        new_quantity = request.data.get('quantity')
        if new_quantity is None:
            return Response({"message": "Quantity field is required for updating."}, status=status.HTTP_400_BAD_REQUEST)
        
        if new_quantity < 0:
            return Response({"message": "Quantity cannot be negative."}, status=status.HTTP_400_BAD_REQUEST)
        
        item.quantity = new_quantity
        item.save()
        return Response({"message": "Quantity updated successfully."})
