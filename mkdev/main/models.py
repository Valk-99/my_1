from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.db.models.signals import post_save

class Profile(models.Model):
    user_profile = models.OneToOneField(User, on_delete=models.CASCADE)
    how_old = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.user_profile} has {self.how_old}'

    def get_absolute_url(self):
        return reverse('profile', kwargs={'pk': self.pk})


class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tag_slug', kwargs={'tag_slug': self.slug})


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    tags = models.ManyToManyField(Tag)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique=True)
    description = models.TextField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'pk': self.pk})

    def good_add(self):
        post_save.connect(send_mail(), sender=self, weak=False)


class Customer(models.Model):
    name = models.CharField(max_length=150,null=True)
    email = models.CharField(max_length=50,null=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.PositiveIntegerField()
    date_order = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Номер заказа: {self.id}'