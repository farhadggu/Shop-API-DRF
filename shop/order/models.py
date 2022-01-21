from django.db import models
from django.conf import settings
from product.models import Product


class Order(models.Model):
    PAYMENT_STATUS = (
        ('p', 'Pending'),
        ('c', 'Completed'),
        ('f', 'Failed'),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS, default='p')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
    total_price = models.IntegerField()


class PurchaseHistory(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    price = models.IntegerField()
    Authority = models.CharField(max_length=50, null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    Status=models.CharField(max_length=50 , null=True , blank=True)
    RefID = models.CharField(max_length=50 , null=True , blank=True)

    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return '%s' % (self.name)