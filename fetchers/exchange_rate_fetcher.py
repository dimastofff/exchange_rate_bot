import logging
import aiohttp
from lxml import html

class ExchangeRateFetcher:
    _BASE_URL = 'https://myfin.by/currency'
    
    _XPATH_EXCHANGE_RATE_ROWS = '//tr[contains(@class, "c-currency-table__main-row") or contains(@class, "currencies-courses__row-main")]'
    _XPATH_BANK_NAME = './/img/@alt'
    _XPATH_USD_PURCHASE_RATE = './td[2]/span/text()'
    _XPATH_USD_SALE_RATE = './td[3]/span/text()'
    _XPATH_EUR_PURCHASE_RATE = './td[4]/span/text()'
    _XPATH_EUR_SALE_RATE = './td[5]/span/text()'
    _XPATH_RUB_PURCHASE_RATE = './td[6]/span/text()'
    _XPATH_RUB_SALE_RATE = './td[7]/span/text()'
    
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self):
        if self.__initialized:
            return
        self.__initialized = True
        
        self._logger = logging.getLogger(__name__)
        self._logger.info('Singlton instance of ExchangeRateFetcher created')

    async def fetch_exchange_rates(self, city_code):
        url = f"{self._BASE_URL}/{city_code}"
        async with aiohttp.ClientSession() as session:
            self._logger.info(f"Fetching from the website: {url}")
            async with session.get(url) as response:
                status = response.status
                if status != 200:
                    self._logger.error(f"Failed to fetch exchange rates. HTTP status: {status}")
                    return None
                text = await response.text()
        return self._parse_rates(text)
    
    def _parse_rates(self, text):
        tree = html.fromstring(text)
        rows = tree.xpath(self._XPATH_EXCHANGE_RATE_ROWS)
        results = []

        for row in rows:
            results.append({
                'bank_name': self._safe_extract(row.xpath(self._XPATH_BANK_NAME)),
                'usd_purchase': self._safe_extract(row.xpath(self._XPATH_USD_PURCHASE_RATE)),
                'usd_sale': self._safe_extract(row.xpath(self._XPATH_USD_SALE_RATE)),
                'eur_purchase': self._safe_extract(row.xpath(self._XPATH_EUR_PURCHASE_RATE)),
                'eur_sale': self._safe_extract(row.xpath(self._XPATH_EUR_SALE_RATE)),
                'rub_purchase': self._safe_extract(row.xpath(self._XPATH_RUB_PURCHASE_RATE)),
                'rub_sale': self._safe_extract(row.xpath(self._XPATH_RUB_SALE_RATE)),
            })
        return results
    
    @staticmethod
    def _safe_extract(xpath_result):
        return xpath_result[0] if xpath_result else '-'


exchange_rate_fetcher = ExchangeRateFetcher()
