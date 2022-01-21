from django.db import models
from django.conf import settings


class Category(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.title
    

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    desc = models.TextField()
    quantity = models.IntegerField()
    price = models.IntegerField()
    discount = models.IntegerField()
    total_price = models.IntegerField(default=0, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        total = (self.price * self.discount) / 100
        self.total_price = int(self.price - total)
        return super().save(*args, **kwargs)



class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comment_product')
    comment = models.TextField()

    def __str__(self):
        return f'{self.user.username}-{self.comment}'
    