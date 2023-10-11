from openpyxl import load_workbook
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from stuff.models import Category

class Command(BaseCommand):
    help = 'Populate the database with initial data'

    def handle(self, *args, **options):
        
        #Read from excel
        workbook = load_workbook(filename='administratorship/management/commands/categories.xlsx')
        sheet = workbook.active

        #fill database
        for row in sheet.iter_rows(min_row=2, values_only=True):
            name = row[0]
            is_sub = row[1]
            slug = row[2]
            subcategory_name = row[3] if len(row) > 3 else None

            data = {
                'name': name,
                'slug': slug,
                'is_sub': is_sub,
                'sub_category': Category.objects.get(name=subcategory_name) if subcategory_name else None
            }
            Category.objects.create(**data)

        self.stdout.write(self.style.SUCCESS('Database populated successfully.'))