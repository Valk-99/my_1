from factory.django import DjangoModelFactory
import factory

from main.models import Category, Tag


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = 'Phones'
    slug = factory.Faker('slug')


class TagFactory(DjangoModelFactory):
    class Meta:
        model = Tag

    name = 'Sport'
    slug = factory.Faker('slug')