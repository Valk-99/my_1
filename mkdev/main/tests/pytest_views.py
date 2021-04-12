import pytest
from django.contrib.auth.models import User

from django.urls import reverse
from django.contrib.auth.models import Permission

from main.models import Product, Category,\
    Seller, Tag, Profile


@pytest.mark.django_db
def test_index_view_get(client):
    url = reverse('index')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_product_detail_view_get(client):
    user = User.objects.create_user('john',
                                    'lennon@thebeatles.com',
                                    'johnpassword')
    product = Product.objects.create(
        category=Category.objects.create(name='Apple',
                                         slug='apple'),
        seller=Seller.objects.create(user=user,
                                     name='john'),
        title='iPhone 20',
        slug='iphone-20',
        description="Heeeeeey",
        price=23.00,
        is_active=True,
        views=1, )
    url = reverse('product_detail',
                  kwargs={'pk': product.pk})
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_tag_detail_view_get(client):
    Tag.objects.create(name='pro', slug='pro')
    url = reverse('tag_slug', args=['pro'])
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_profile_create_view_get(client):
    user = User.objects.create_user('john',
                                    'lennon@thebeatles.com',
                                    'johnpassword')
    client.login(username='john', password='johnpassword')
    Profile.objects.create(user_profile=user, how_old=31)
    url = reverse('profile_form')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_profile_create_view_post(client):
    User.objects.create_user('john1',
                             'lennon@thebeatles.com',
                             'johnpassword')
    client.login(username='john', password='johnpassword')
    url = reverse('profile_form')
    response = client.post(url, {'user_profile': 2, 'how_old': 22})
    assert response.status_code == 302


@pytest.mark.django_db
def test_profile_update_view_get(client):
    user = User.objects.create_user('john',
                                    'lennon@thebeatles.com',
                                    'johnpassword')
    client.login(username='john', password='johnpassword')
    profile = Profile.objects.create(user_profile=user, how_old=31)
    url = reverse('profile', kwargs={'pk': profile.pk})
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_profile_update_view_post(client):
    user = User.objects.create_user('john',
                                    'lennon@thebeatles.com',
                                    'johnpassword')
    client.login(username='john', password='johnpassword')
    profile = Profile.objects.create(user_profile=user, how_old=31)
    url = reverse('profile', kwargs={'pk': profile.pk})
    response = client.post(url, {'user_profile': 1, 'how_old': 22})
    assert response.status_code == 302
    profile.refresh_from_db()
    assert (profile.how_old, 22)


@pytest.mark.django_db
def test_create_product_view_get(client):
    user = User.objects.create_user('john',
                                    'lennon@thebeatles.com',
                                    'johnpassword')
    permission = Permission.objects.get(name='Can add product')
    permission1 = Permission.objects.get(name='Can change product')
    user.user_permissions.add(permission1, permission)
    client.login(username='john', password='johnpassword')
    url = reverse('product_create')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_product_create_view_post(client):
    user3 = User.objects.create_user('john3',
                                     'lennon@thebeatles.com',
                                     'johnpassword')
    client.login(username='john', password='johnpassword')
    url = reverse('product_create')
    response = client.post(url, {
            'category': Category.objects.create(name='Apple2', slug='apple2'),
            'seller': Seller.objects.create(user=user3, name='john'),
            'title':  'iPhone 22',
            'slug':  'iphone-22',
            'description': "Heeeeeey",
            'price': 23.00,
            'is_active': True,
            'views': 1,
        })
    assert response.status_code == 302


@pytest.mark.django_db
def test_product_update_view_get(client):
    user = User.objects.create_user('john',
                                    'lennon@thebeatles.com',
                                    'johnpassword')
    permission = Permission.objects.get(name='Can add product')
    permission1 = Permission.objects.get(name='Can change product')
    user.user_permissions.add(permission1, permission)
    product = Product.objects.create(
        category=Category.objects.create(name='Apple', slug='apple'),
        seller=Seller.objects.create(user=user, name='john'),
        title='iPhone 20',
        slug='iphone-20',
        description="Heeeeeey",
        price=23.00,
        is_active=True,
        views=1, )
    client.login(username='john', password='johnpassword')
    url = reverse('product_update', kwargs={'pk': product.id})
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_product_update_view_post(client):
    user4 = User.objects.create_user('john4',
                                     'lennon@thebeatles.com',
                                     'johnpassword')
    client.login(username='john', password='johnpassword')
    product1 = Product.objects.create(
        category=Category.objects.create(name='Apple3', slug='apple3'),
        seller=Seller.objects.create(user=user4, name='john4'),
        title='iPhone 221',
        slug='iphone-202',
        description="Heeeeeey",
        price=23.00,
        is_active=True,
        views=1, )
    url = reverse('product_update', kwargs={'pk': product1.id})
    response = client.post(url, {
            'category': 'Apple3',
            'seller': 'john4',
            'title': 'iPhone 221',
            'slug': 'iphone-202',
            'description': "Heeeeeey",
            'price': 23.00,
            'is_active': True,
            'views': 1,
        })
    assert response.status_code == 302
    product1.refresh_from_db()
    assert (product1.title, 'iPhone 221')
