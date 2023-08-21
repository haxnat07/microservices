from rest_framework import serializers
from .models import *


class ItemImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemImage
        fields = ('image',)

class ItemSerializer(serializers.ModelSerializer):
    images = ItemImageSerializer(many=True, read_only=True)

    class Meta:
        model = Item
        fields = ('id', 'name', 'price', 'quantity', 'images')

    def create(self, validated_data):
        images_data = self.context['request'].FILES.getlist('images')
        item = Item.objects.create(**validated_data)
        for image_data in images_data:
            ItemImage.objects.create(item=item, image=image_data)
        return item