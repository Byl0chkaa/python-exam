from django.core.management.base import BaseCommand
from apps.ads.models import ForbiddenWordModel


class Command(BaseCommand):
    help = 'Автоматично наповнює базу даних базовим списком заборонених слів'

    def handle(self, *args, **options):
        words_to_seed = [
            'шахрай', 'обман', 'капєц', 'купуйте прямо зараз',
            'терміново без перевірки', 'махінація', 'бабло'
        ]

        self.stdout.write('Початок наповнення бази даних забороненими словами...')

        count_created = 0
        for word_text in words_to_seed:
            obj, created = ForbiddenWordModel.objects.get_or_create(word=word_text.lower())
            if created:
                count_created += 1

        self.stdout.write(
            self.style.SUCCESS(f'Успішно завершено! Додано нових слів: {count_created}.')
        )