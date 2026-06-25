from django.core.management.base import BaseCommand
from core.services.exchange_rates import ExchangeService

class Command(BaseCommand):
    help = 'Первинне завантаження та синхронізація курсів валют з API при старті системи'

    def handle(self, *args, **options):
        self.stdout.write('Запуск синхронізації курсів валют з ПриватБанком...')
        try:
            result = ExchangeService.update_exchange()
            self.stdout.write(
                self.style.SUCCESS(f'Синхронізацію успішно завершено. Результат: {result}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Не вдалося оновити курси при старті (можливо, API недоступне): {e}')
            )