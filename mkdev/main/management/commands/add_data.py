from django.core.management.base import BaseCommand

from main.factory import CategoryFactory, TagFactory


class Command(BaseCommand):
    help = "create test model"

    def add_arguments(self, parser):
        parser.add_argument('--category',
                            type=str,
                            help='Create category')
        parser.add_argument('--tag',
                            type=str,
                            help='Create tag')

    def handle(self, *args, **options):
        for i in [options['category'], options['tag']]:
            CategoryFactory.create(), TagFactory.create()
            break