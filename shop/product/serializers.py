from rest_framework import serializers
from account.models import User
from .models import Category, Product, Comment


class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'slug']


class CategorySerializer(serializers.ModelSerializer):
    parent = ParentSerializer()
    class Meta:
        model = Category
        fields = ['id', 'parent', 'title', 'slug']


class CreateCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['parent', 'title', 'slug']


class SimpleUser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class SimpleComment(serializers.ModelSerializer):
    user = SimpleUser()
    class Meta:
        model = Comment
        fields = ['id', 'user', 'comment']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    comment_product = SimpleComment(many=True)
    class Meta:
        model = Product
        fields = ['id', 'category', 'title', 'slug', 'desc', 'quantity', 'price', 'discount', 'total_price', 'comment_product']


class SimpleProduct(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'total_price']


class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'category', 'title', 'slug', 'desc', 'quantity', 'price', 'discount', 'total_price']


class CommentSerializer(serializers.ModelSerializer):
    user = SimpleUser()
    product = SimpleProduct()
    class Meta:
        model = Comment
        fields = ['id', 'user', 'product', 'comment']


class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['comment']

    def create(self, validated_data):
        user_id = self.context['user_id']
        product_id = self.context['product_id']
        return Comment.objects.create(user_id=user_id, product_id=product_id, **validated_data)