from rest_framework import serializers
from cart.models import CartItem, Cart
from .models import Order, OrderItem, PurchaseHistory
from product.serializers import SimpleProduct


class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProduct()
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'total_price']


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'payment_status', 'order_items']


class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError('No carts with the given id exists')
        if CartItem.objects.filter(cart_id=cart_id).count() == 0:
            raise serializers.ValidationError('The Cart is Empty.')
        return cart_id

    def save(self, *args, **kwargs):
        user = self.context['user']
        cart_id = self.validated_data['cart_id']
        order = Order.objects.create(user_id=user.id)

        cart_items = CartItem.objects.select_related('product').filter(cart_id=cart_id)
        order_items = [
            OrderItem(
                order=order,
                product=item.product,
                total_price = item.product.total_price,
                quantity = item.quantity
            ) for item in cart_items
        ]
        OrderItem.objects.bulk_create(order_items)

        Cart.objects.filter(pk=cart_id).delete()

        name = user.first_name
        email = user.email
        price = sum([item.total_price for item in OrderItem.objects.only('total_price').filter(order_id=order.id)])
        PurchaseHistory.objects.create(name=name, email=email, price=price)

        return order


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['payment_status']


class SendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseHistory
        fields = ['id', 'name', 'email', 'price']
        read_only_fields = ['name', 'email', 'price']
        


class VerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseHistory
        fields = ['price', 'user']