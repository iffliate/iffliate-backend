"""
command for the application to bulk create roles
"""
from django.core.management import BaseCommand
from product import models


class Command(BaseCommand):
    """
    Django command to initialise admin
    """

    def handle(self, *args, **options):
        if models.Category.objects.count() != 7:
            self.stdout.write('Creating Categories for the  application')
            for name in ['Grocery','Bakery','MakeUP','Bags','Clothing','Funiture','Book']:
                models.Category.objects.create(
                    name=name)
            self.stdout.write('Create  Categories Successfully')
            