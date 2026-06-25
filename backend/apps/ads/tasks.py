import re

from celery import shared_task
from core.services.email_service import EmailService
from core.services.exchange_rates import ExchangeService

from apps.ads.models import CarAdModel, ForbiddenWordModel
from apps.users.models import UserModel


@shared_task
def validate_ad_description(ad_id):
    ad = CarAdModel.objects.get(id=ad_id)
    bad_words = ForbiddenWordModel.objects.values_list('word', flat=True)

    if not bad_words:
        ad.status = CarAdModel.StatusChoices.ACTIVE
        ad.save()
        return f"Оголошення {ad_id} пройшло перевірку (список заборонених слів порожній)"

    pattern = re.compile(r'\b(' + '|'.join(map(re.escape, bad_words)) + r')\b', re.IGNORECASE)

    if pattern.search(ad.description):
        ad.edit_attempts += 1
        ad.save()

        if ad.edit_attempts >= 3:
            ad.status = CarAdModel.StatusChoices.MANAGER_REVIEW
            ad.save()

            managers = UserModel.objects.filter(role=UserModel.RoleChoices.MANAGER)
            for manager in managers:
                EmailService.manager_alert(manager.email, ad.id)
            return f"Оголошення {ad_id} відправлено на перевірку менеджеру"


        ad.status = CarAdModel.StatusChoices.PENDING_CHECK
        ad.save()
        return f"Оголошення {ad_id} відхилено автоматично. Спроба {ad.edit_attempts} з 3"

    ad.edit_attempts = 0
    ad.status = CarAdModel.StatusChoices.ACTIVE
    ad.save()
    return f"Оголошення {ad.id} пройшло перевірку"


@shared_task
def update_exchange_task():
    result = ExchangeService.update_exchange()
    return result