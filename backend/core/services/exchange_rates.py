from decimal import Decimal

import requests
from apps.ads.models import CarAdModel, ExchangeRatesModel


class ExchangeService:
    @staticmethod
    def update_exchange():
        response = requests.get('https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11')
        data = response.json()

        for item in data:
            if item['ccy'] in ['USD', 'EUR']:
                ExchangeRatesModel.objects.update_or_create(
                    currency=item['ccy'],
                    defaults={'rate_to_uah': item['sale']}
                )

        rates = {r.currency: Decimal(str(r.rate_to_uah)) for r in ExchangeRatesModel.objects.all()}

        if 'USD' not in rates or 'EUR' not in rates:
            return "Немає курсів для оновлення"

        rate_usd = rates['USD']
        rate_eur = rates['EUR']
        ads_to_update = []

        for ad in CarAdModel.objects.all():
            if ad.original_currency == 'USD':
                ad.price_usd = ad.original_price
                ad.price_uah = ad.original_price * rate_usd
                ad.price_eur = ad.price_uah / rate_eur
                ad.exchange_rate_used = rate_usd
            elif ad.original_currency == 'EUR':
                ad.price_eur = ad.original_price
                ad.price_uah = ad.original_price * rate_eur
                ad.price_usd = ad.price_uah / rate_usd
                ad.exchange_rate_used = rate_eur
            else:
                ad.price_uah = ad.original_price
                ad.price_usd = ad.original_price / rate_usd
                ad.price_eur = ad.original_price / rate_eur
                ad.exchange_rate_used = rate_usd

            ads_to_update.append(ad)

        CarAdModel.objects.bulk_update(ads_to_update, ['price_usd', 'price_eur', 'price_uah', 'exchange_rate_used'])
        return "Курси успішно оновлено!"