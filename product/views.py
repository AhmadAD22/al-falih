
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from .serializers import ProductSerializer,CategorySerializer,SubcategorySerializer
from .models import Product,Category,Subcategory
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication


# Product viewset

class ProductView(ViewSet):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def list (self,request):
        all_products=Product.objects.all()
        serializer=ProductSerializer(all_products,many=True)
        return Response(serializer.data)
    
    def listByCategory(self,request,*args, **kwargs):
        category_obj = Category.objects.filter(pk=kwargs['category_id']).first()
        if category_obj:
            subcategories_id=[subcategory.id for subcategory in Subcategory.objects.filter(category=category_obj)]
            products=Product.objects.filter(subcategory__id__in=subcategories_id)
            serializer=ProductSerializer(products,many=True)
            return Response(serializer.data)
        else:
            return Response("The Category does exists")
        
    def listBySubcategory(self,request,*args, **kwargs):
        subcategory_obj=Subcategory.objects.filter(pk=kwargs['subcategory_id']).first()
        if subcategory_obj:
            products=Product.objects.filter(subcategory=subcategory_obj)
            serializer=ProductSerializer(products,many=True)
            return Response(serializer.data)
        else:
            return Response("The Subcategory does exists")
        
    def create(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def update(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)
        old_image_path = product.image.path if product.image else None
        serializer = ProductSerializer(product, data=request.data)

        if serializer.is_valid():
            serializer.save()

            # Delete old image file
           # if old_imagepath and the new image file path are different, and the old image file exists, delete the old file.
            if 'image' in request.data:
                new_image_path = serializer.data.get('image')
                if old_image_path and new_image_path and old_image_path != new_image_path:
                    fs = FileSystemStorage(location=settings.MEDIA_ROOT)
                    fs.delete(old_image_path)

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)
        image_path = product.image.path if product.image else None
        product.delete()

        # Delete image file
        if image_path:
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)
            fs.delete(image_path)

        return Response(status=status.HTTP_204_NO_CONTENT)
        
               
        
        
        
        
        
#Categories
class CategoryView(ViewSet):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def list (self,request):
        categoris=Category.objects.all()
        serializer=CategorySerializer(categoris,many=True)
        return Response (serializer.data)
    def create(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def update(self, request, pk=None):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        return Response(status=204)
    
    
#Subcategories 
class SubcategoryView(ViewSet):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def list (self,request):
        subcategories=Subcategory.objects.all()
        serializer=SubcategorySerializer(subcategories,many=True) 
        return Response(serializer.data)
    
    def create(self, request):
        serializer = SubcategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        subcategory = get_object_or_404(Subcategory, pk=pk)
        serializer = SubcategorySerializer(subcategory)
        return Response(serializer.data)

    def update(self, request, pk=None):
        subcategory = get_object_or_404(Subcategory, pk=pk)
        serializer = SubcategorySerializer(subcategory, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        subcategory = get_object_or_404(Subcategory, pk=pk)
        subcategory.delete()
        return Response(status=204)
  