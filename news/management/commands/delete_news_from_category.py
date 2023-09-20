from django.core.management.base import BaseCommand, CommandError
from news.models import Post, Category


class Command(BaseCommand):
    help = 'Delete all records from concrete category'  # показывает подсказку при вводе "python manage.py <ваша команда> --help"
    requires_migrations_checks = False  # напоминать ли о миграциях. Если true — то будет напоминание о том, что не сделаны все миграции (если такие есть)

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        answer = input(f'Вы правда хотите удалить все статьи в категории {options["category"]}? yes/no: ')
        if answer != 'yes':
            self.stdout.write(self.style.ERROR('Отменено'))
        try:
            cat = Category.objects.get(category=options['category'])
            Post.objects.filter(category=cat).delete()
            self.stdout.write(self.style.SUCCESS(
            f'Succesfully deleted all news from category {cat}'))
        except Post.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Could not find category'))




