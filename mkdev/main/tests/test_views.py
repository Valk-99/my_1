from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import Permission

from main.models import Tag, Product, Category, Seller, Profile


class ViewGetPostTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.permission = Permission.objects.get(name='Can add product')
        self.permission1 = Permission.objects.get(name='Can change product')
        self.user.user_permissions.add(self.permission1, self.permission)
        self.tag = Tag.objects.create(name='pro', slug='pro')
        self.profile = Profile.objects.create(user_profile=self.user, how_old=31)
        self.product = Product.objects.create(
            category=Category.objects.create(name='Apple', slug='apple'),
            seller=Seller.objects.create(user=self.user, name='john'),
            title='iPhone 20',
            slug='iphone-20',
            description="Heeeeeey",
            price=23.00,
            is_active=True,
            views=1,)

        self.index_url = reverse('index')
        self.product_detail_url = reverse('product_detail', kwargs={'pk': self.product.pk})
        self.tag_detail_url = reverse('tag_slug', args=['pro'])
        self.profile_create_url = reverse('profile_form')
        self.profile_update_url = reverse('profile', kwargs={'pk': self.profile.pk})
        self.create_product_url = reverse('product_create')
        self.product_update_url = reverse('product_update', kwargs={'pk': self.product.id})

    def test_index_list_view_url_get(self):
        resp = self.client.get(self.index_url)
        self.assertEqual(resp.status_code, 200)

    def test_product_detail_view_url_get(self):
        resp = self.client.get(self.product_detail_url)
        self.assertEqual(resp.status_code, 200)

    def test_tag_detail_view_url_get(self):
        resp = self.client.get(self.tag_detail_url)
        self.assertEqual(resp.status_code, 200)

    def test_profile_create_view_url_get(self):
        self.client.login(username='john', password='johnpassword')
        resp = self.client.get(self.profile_create_url)
        self.assertEqual(resp.status_code, 200)

    def test_profile_create_view_url_post(self):
        self.client.login(username='john', password='johnpassword')
        self.user2 = User.objects.create_user('john1', 'lennon@thebeatles.com', 'johnpassword')
        resp = self.client.post(self.profile_create_url, {'user_profile': 2, 'how_old': 22})
        self.assertEqual(resp.status_code, 302)

    def test_profile_update_view_url_get(self):
        self.client.login(username='john', password='johnpassword')
        resp = self.client.get(self.profile_update_url)
        self.assertEqual(resp.status_code, 200)

    def test_profile_update_view_url_post(self):
        self.client.login(username='john', password='johnpassword')
        resp = self.client.post(self.profile_update_url, {'user_profile': 1, 'how_old': 22})
        self.assertEqual(resp.status_code, 302)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.how_old, 22)

    def test_create_product_view_url_get(self):
        self.client.login(username='john', password='johnpassword')
        self.user.user_permissions.add(self.permission)
        resp = self.client.get(self.create_product_url)
        self.assertEqual(resp.status_code, 200)

    def test_product_create_view_url_post(self):
        self.client.login(username='john', password='johnpassword')
        self.user3 = User.objects.create_user('john3', 'lennon@thebeatles.com', 'johnpassword')
        resp = self.client.post(self.create_product_url, {
            'category': Category.objects.create(name='Apple2', slug='apple2'),
            'seller': Seller.objects.create(user=self.user3, name='john'),
            'title':  'iPhone 22',
            'slug':  'iphone-22',
            'description': "Heeeeeey",
            'price': 23.00,
            'is_active': True,
            'views': 1,
        })
        self.assertEqual(resp.status_code, 302)

    def test_product_update_view_url_get(self):
        self.client.login(username='john', password='johnpassword')
        self.user.user_permissions.add(self.permission1)
        resp = self.client.get(self.product_update_url)
        self.assertEqual(resp.status_code, 200)

    def test_product_update_view_url_post(self):
        self.client.login(username='john', password='johnpassword')
        resp = self.client.post(self.product_update_url, {
            'category': 'Apple2',
            'seller': 'john2',
            'title': 'iPhone 220',
            'slug': 'iphone-22',
            'description': "Heeeeeey",
            'price': 23.00,
            'is_active': True,
            'views': 1,
        })
        self.assertEqual(resp.status_code, 302)
        self.product.refresh_from_db()
        self.assertEqual(self.product.title, 'iPhone 220')




