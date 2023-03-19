import json
import asyncio
import aiofiles
import logging
import psutil
from pathlib import Path
from utils import generate_server_usage_text

class UsageData:
    _STATS_FILE = 'logs/bot_usage_stats.json'
    
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
        self._bot_usage_stats = {}
        
        self._load_statistics()
        self._logger.info('Singlton instance of UsageData created')
        
    @property
    def bot_usage_stats(self):
        return self._bot_usage_stats
            
    def _load_statistics(self):
        try:
            if Path(self._STATS_FILE).is_file():
                with open(self._STATS_FILE, 'r', encoding='utf-8') as f:
                    self._bot_usage_stats = json.load(f)
        except Exception as e:
            self._logger.error(f"Error loading statistics: {e}")
                
    async def _save_statistics(self):
        try:
            async with aiofiles.open(self._STATS_FILE, 'w', encoding='utf-8') as f:
                await f.write(json.dumps(self._bot_usage_stats, ensure_ascii=False, indent=4))
        except Exception as e:
            self._logger.error(f"Error saving statistics: {e}")
            
    async def periodic_save_statistics_task(self):
        while True:
            await asyncio.sleep(60)
            self._logger.info("Saving bot usage statistics")
            try:
                await self._save_statistics()
            except Exception as e:
                self._logger.error(f"Error during periodic save: {e}")
                
    def generate_statistics_text(self):
        text = generate_server_usage_text()
        text += "Bot Usage Statistics:\n"
        for date, stats in self.bot_usage_stats.items():
            text += f"  {date}:\n"
            text += f"      Total requests: {stats['total_requests']}\n"
            text += "      Users:\n"
            for user_id, user_data in stats["users"].items():
                text += f"            {user_data['full_name']}:\n"
                text += f"                Last used at: {user_data['last_used_at']}\n"
                text += f"                Requests count: {user_data['requests_count']}\n"
        return text

usage_data = UsageData()
