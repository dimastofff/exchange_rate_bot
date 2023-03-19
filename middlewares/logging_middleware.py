import logging
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types
from datetime import datetime
from utils import desired_timezone

class LoggingMiddleware(BaseMiddleware):
    def __init__(self, bot_usage_stats):
        self._logger = logging.getLogger(__name__)
        self._bot_usage_stats = bot_usage_stats
        super().__init__()
    
    async def on_pre_process_message(self, message: types.Message, data: dict):
        user_id = message.from_user.id
        full_name = message.from_user.full_name
        self._logger.info(f"User {full_name}[{user_id}] sent a message: {message.text}")
        await self._update_statistics(user_id, full_name)

    async def on_pre_process_callback_query(self, call: types.CallbackQuery, data: dict):
        user_id = call.from_user.id
        full_name = call.from_user.full_name
        self._logger.info(f"User {full_name}[{user_id}] triggered a callback query: {call.data}")
        await self._update_statistics(user_id, full_name)
        
    async def _update_statistics(self, user_id, full_name):
        user_id = str(user_id)
        date_key = datetime.now(desired_timezone).strftime('%d-%m-%Y')
        if date_key not in self._bot_usage_stats:
            self._bot_usage_stats[date_key] = {
                "total_requests": 0,
                "users": {}
            }

        self._bot_usage_stats[date_key]["total_requests"] += 1
        user_data = self._bot_usage_stats[date_key]["users"].setdefault(user_id, {
            "last_used_at": "",
            "requests_count": 0
        })

        user_data["full_name"] = full_name
        user_data["last_used_at"] = datetime.now(desired_timezone).strftime('%d-%m-%Y %H:%M:%S')
        user_data["requests_count"] += 1
