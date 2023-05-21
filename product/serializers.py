from rest_framework import serializers
from .models import Product,Category,Subcategory


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields='__all__'
        
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields='__all__'
        
class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Subcategory
        fields='__all__'