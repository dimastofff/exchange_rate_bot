
import json
import logging
from pathlib import Path

class LocationsData:
    _REGIONS_WITH_CITIES_FILE = 'init_data/regions_with_cities.json'
    
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
        self._regions_with_cities = []
        self._city_name_to_code = {}
        
        self._load_regions_with_cities()
        self._create_city_to_code_dictionary()
        self._logger.info('Singlton instance of LocationsData created')
        
    @property
    def regions_with_cities(self):
        return self._regions_with_cities

    @property
    def city_name_to_code(self):
        return self._city_name_to_code
            
    def _load_regions_with_cities(self):
        try:
            if Path(self._REGIONS_WITH_CITIES_FILE).is_file():
                with open(self._REGIONS_WITH_CITIES_FILE, 'r', encoding='utf-8') as f:
                    self._regions_with_cities = json.load(f)
        except Exception as e:
            self._logger.error(f"Error loading cities: {e}")
            
    def _create_city_to_code_dictionary(self):
        self._city_name_to_code = {}
        for region in self.regions_with_cities:
            for city in region["cities"]:
                self._city_name_to_code[city["name"]] = city["code"]

locations_data = LocationsData()
