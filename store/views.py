from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from .models import Cart
from .serializers import CartSerializer
from rest_framework.authentication import TokenAuthentication

class AddToCartView(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)
    serializer_class = CartSerializer

    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')
        user = request.user

        if not product_id or not quantity:
            return Response({'message': 'Product ID and Quantity are required.'}, status=HTTP_400_BAD_REQUEST)

        try:
            cart_item = Cart.objects.get(user=user, product_id=product_id)
            cart_item.quantity += int(quantity)
            cart_item.save()
            return Response(CartSerializer(cart_item).data)
        except Cart.DoesNotExist:
            cart_item = Cart.objects.create(user=user, product_id=product_id, quantity=int(quantity))
            return Response(CartSerializer(cart_item).data, status=HTTP_201_CREATED)
        
        
        


class ViewCartView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)