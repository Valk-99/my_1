from django.contrib.sites.models import Site
from django.contrib.auth.models import AbstractUser
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django.db.models.signals import post_save
from django.utils.html import strip_tags


class Profile(AbstractUser):
    how_old = models.IntegerField(null=True)

    class Meta(AbstractUser.Meta):
        pass

    def __str__(self):
        return f'{self.username}'


class Seller(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE,)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_slug', kwargs={'category_slug': self.slug})


class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tag_slug', kwargs={'tag_slug': self.slug})


class Product(models.Model):
    STATUS_CHOICES = [
        ('d', 'Draft'),
        ('p', 'Published'),
        ('w', 'Withdrawn'),
    ]
    """ it is my model of Products"""
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='category')
    tags = models.ManyToManyField(Tag, blank=True)
    # tags_array = ArrayField(models.CharField(max_length=200),default=' ', blank=True)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique=True)
    description = models.TextField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    image = models.ImageField(upload_to='media/%Y/%m/%d', blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True, null=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'pk': self.pk})

    def send_email(self):
        from .tasks import send_email_task_product
        send_email_task_product.delay(
            self.title, self.slug,
            self.description, self.price
        )


@receiver(post_save, sender=Product)
def create_product(sender, created, instance, **kwargs):
    sub = Subscriber.objects.values_list('user__email', flat=True)
    domain = Site.objects.get_current().domain
    url = 'http://{domain}'.format(domain=domain)
    subject, from_email, to = 'Subject', 'from@xxx.com', sub
    if created and instance.is_active == True:
        html_content = render_to_string('main/add_product_mail.html',
                                        {'varname': 'Новый продукт на сайте',
                                         'url': url})
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(
            subject,
            text_content,
            from_email,
            [to],
        )
        msg.send()


class Subscriber(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.user


class ProductViews(models.Model):
    title = models.CharField(max_length=200)
    views = models.IntegerField()

    def __str__(self):
        return self.title

    class Meta:
        managed = False
        db_table = "main_product"


class Comment(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='comments')
    username = models.CharField(max_length=100)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.username)
