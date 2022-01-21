from django.shortcuts import render
from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from .serializers import (
    CategorySerializer,
    CreateCategorySerializer,
    ProductSerializer,
    CreateProductSerializer,
    CommentSerializer,
    CreateCommentSerializer
)
from .models import Category, Product, Comment


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CategorySerializer
        return CreateCategorySerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == "GET":
            return ProductSerializer
        return CreateProductSerializer


class CommentViewSet(ModelViewSet):
    def get_queryset(self):
        return Comment.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'user_id': self.request.user.id, 'product_id': self.kwargs['product_pk']}
    
    def get_serializer_class(self):
        if self.request.method == "GET":
            return CommentSerializer
        return CreateCommentSerializer