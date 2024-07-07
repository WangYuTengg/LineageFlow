from django.core.management.base import BaseCommand
from django.db import connection
from django.apps import apps

class Command(BaseCommand):
    help = 'Drops all tables for the specified app'

    def add_arguments(self, parser):
        parser.add_argument('app_label', type=str, help='App label of the application to drop tables')

    def handle(self, *args, **kwargs):
        app_label = kwargs['app_label']
        app_config = apps.get_app_config(app_label)
        
        table_names = [model._meta.db_table for model in app_config.get_models()]
        
        with connection.cursor() as cursor:
            for table_name in table_names:
                self.stdout.write(f'Dropping table {table_name}')
                cursor.execute(f'DROP TABLE IF EXISTS {table_name} CASCADE')
        self.stdout.write(self.style.SUCCESS(f'Successfully dropped all tables for app "{app_label}"'))
