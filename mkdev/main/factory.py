from factory.django import DjangoModelFactory
import factory

from main.models import Category, Tag


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker('name')
    slug = factory.Faker('slug')


class TagFactory(DjangoModelFactory):
    class Meta:
        model = Tag

    name = factory.Faker('name')
    slug = factory.Faker('slug')