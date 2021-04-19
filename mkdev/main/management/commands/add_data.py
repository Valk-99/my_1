from django.core.management.base import BaseCommand

from main.factory import CategoryFactory, TagFactory


class Command(BaseCommand):
    help = "create test model"

    def add_arguments(self, parser):
        CategoryFactory()
        TagFactory()

    def handle(self, *args, **kwargs):
        pass