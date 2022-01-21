from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from .serializers import (
    CartSerializer,
    CartItemSerializer,
    CreateCartItemSerializer,
    UpdateCartItemSerializer,
)
from .models import Cart, CartItem


class CartViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Cart.objects.prefetch_related('cart_items__product').all()
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    def get_queryset(self):
        return CartItem.objects.select_related('product').filter(cart_id=self.kwargs['cart_pk'])

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}
    
    def get_serializer_class(self):
        if self.request.method == "GET":
            return CartItemSerializer
        elif self.request.method == "PATCH":
            return UpdateCartItemSerializer
        return CreateCartItemSerializer
