import logging
from cachetools import TTLCache
from fetchers import exchange_rate_fetcher

class CacheData:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__initialized = False
        return cls._instance
    
    def __init__(self, maxsize, ttl):
        if self.__initialized:
            return
        self.__initialized = True
        
        self._logger = logging.getLogger(__name__)
        self._cache = TTLCache(maxsize=maxsize, ttl=ttl)
        
        self._logger.info('Singlton instance of CacheData created')
        
    @property
    def cache(self):
        return self._cache
        
    async def get_exchange_rates_by_city_code(self, city_code):
        if city_code not in self._cache:
            rates = await exchange_rate_fetcher.fetch_exchange_rates(city_code)
            self._cache[city_code] = rates
        else:
            self._logger.info(f"Using cached data for city: {city_code}")

        return self.cache[city_code]
    
cache_data = CacheData(155, 300)
