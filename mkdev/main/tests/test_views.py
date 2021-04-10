from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import Permission

from main.models import Tag, Product, Category, Seller, Profile


class IndexListTestCase(TestCase):
    """It`s working"""
    def setUp(self):
        self.client = Client()
        self.index_url = reverse('index')

    def test_index_list_view_url_get(self):
        resp = self.client.get(self.index_url)
        self.assertEqual(resp.status_code, 200)


class ProductDetailTestCase(TestCase):
    """It`s working"""
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

        self.product = Product.objects.create(
            category=Category.objects.create(name='Apple', slug='apple'),
            seller=Seller.objects.create(user=self.user, name='john'),
            title='iPhone 20',
            slug='iphone-20',
            description="Heeeeeey",
            price=23.00,
            is_active=True,
            views=1,
        )
        self.product_detail_url = reverse('product_detail', kwargs={'pk': self.product.pk})

    def test_product_detail_view_url_get(self):
        resp = self.client.get(self.product_detail_url)
        self.assertEqual(resp.status_code, 200)


class TagDetailTestCase(TestCase):
    """It`s working"""
    def setUp(self):
        self.client = Client()
        self.tag_detail_url = reverse('tag_slug', args=['pro'])
        self.tag = Tag.objects.create(name='pro', slug='pro')

    def test_tag_detail_view_url_get(self):
        resp = self.client.get(self.tag_detail_url)
        self.assertEqual(resp.status_code, 200)


class ProfileCreateTestCase(TestCase):
    """It`s working"""
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.profile_create_url = reverse('profile_form')

    def test_profile_create_view_url_get(self):
        self.client.login(username='john', password='johnpassword')
        resp = self.client.get(self.profile_create_url)
        self.assertEqual(resp.status_code, 200)

    def test_profile_create_view_url_post(self):
        self.client.login(username='john', password='johnpassword')
        resp = self.client.post(self.profile_create_url, {'user_profile': 1, 'how_old': 22})
        self.assertEqual(resp.status_code, 302)


class ProfileUpdateTestCase(TestCase):
    """It`s working"""
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.profile = Profile.objects.create(user_profile=self.user, how_old=31)
        self.profile_update_url = reverse('profile', kwargs={'pk': self.profile.pk})

    def test_profile_update_view_url_get(self):
        self.client.login(username='john', password='johnpassword')
        resp = self.client.get(self.profile_update_url)
        self.assertEqual(resp.status_code, 200)

    def test_profile_create_view_url_post(self):
        self.client.login(username='john', password='johnpassword')
        resp = self.client.post(self.profile_update_url, {'user_profile': 1, 'how_old': 22})
        self.assertEqual(resp.status_code, 302)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.how_old, 22)


class CreateProductTestCase(TestCase):
    """need to add post test"""
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.permission = Permission.objects.get(name='Can add product')
        self.user.user_permissions.add(self.permission)
        self.create_product_url = reverse('product_create')

    def test_create_product_view_url_get(self):
        self.client.login(username='john', password='johnpassword')
        resp = self.client.get(self.create_product_url)
        self.assertEqual(resp.status_code, 200)

    def test_profile_create_view_url_post(self):
        self.client.login(username='john', password='johnpassword')
        resp = self.client.post(self.create_product_url, {
            'category': 'category',
            'seller': 'Valk',
            'title': 'iPhone 20',
            'slug': 'iphone-20',
            'description': "Heeeeeey",
            'price': 23.00,
            'is_active': True,
            'views': 1,
        })
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'iPhone 20')
        self.assertContains(resp, 'Heeeeeey')


class ProductUpdateTestCase(TestCase):
    """need to add post test"""
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.permission = Permission.objects.get(name='Can change product')
        self.user.user_permissions.add(self.permission)
        category = Category.objects.create(name='Apple', slug='apple')
        seller = Seller.objects.create(user=self.user, name='john')
        self.product = Product.objects.create(
                category=category,
                seller=seller,
                title='iPhone 20',
                slug='iphone-20',
                description="Heeeeeey",
                price=23.00,
                is_active=True,
                views=1,
        )
        self.product_update_url = reverse('product_update', kwargs={'pk': 1})

    def test_product_update_view_url_get(self):
        self.client.login(username='john', password='johnpassword')
        resp = self.client.get(self.product_update_url)
        self.assertEqual(resp.status_code, 200)

    def test_profile_create_view_url_post(self):
        self.client.login(username='john', password='johnpassword')
        resp = self.client.post(self.product_update_url, {
            'category': self.product.category,
            'seller': self.product.seller,
            'title': self.product.title,
            'slug': self.product.slug,
            'description': "Heeeeeey123",
            'price': self.product.price,
            'is_active': self.product.is_active,
            'views': self.product.views,
        })
        self.assertEqual(resp.status_code, 302)
        self.product.refresh_from_db()
        self.assertEqual(self.product.description, 'Heeeeeey123')



