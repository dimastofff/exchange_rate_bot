import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor
from middlewares import LoggingMiddleware
from handlers import *
from storage import *

async def on_startup(dp):
    asyncio.create_task(usage_data.periodic_save_statistics_task())

if __name__ == '__main__':
    load_dotenv()
    
    bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
    dp = Dispatcher(bot)
    
    dp.register_message_handler(handle_start_help, commands=['start', 'help'])
    dp.register_message_handler(handle_unknown)
    
    dp.register_callback_query_handler(handle_region_choice, lambda call: call.data.startswith('region:'))
    dp.register_callback_query_handler(handle_city_choice, lambda call: call.data.startswith('city:'))
    dp.register_callback_query_handler(handle_return_to_regions, lambda call: call.data == "return_to_regions")
    dp.register_callback_query_handler(handle_admin_button, lambda call: call.data == "admin")
    
    dp.middleware.setup(LoggingMiddleware(usage_data.bot_usage_stats))
    
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
