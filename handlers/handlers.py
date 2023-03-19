import os
import logging
from aiogram import types
from storage import *
from utils import generate_regions_markup, generate_cities_markup, generate_common_markup

logger = logging.getLogger(__name__)

async def handle_start_help(message: types.Message):
    user_id = message.from_user.id
    markup = generate_regions_markup(user_id, locations_data.regions_with_cities)
    await message.answer("Выберите область:", reply_markup=markup)

async def handle_region_choice(call: types.CallbackQuery):
    user_id = call.from_user.id
    region_name = call.data.split(':')[1]
    try:
        selected_region = next(
            region for region in locations_data.regions_with_cities if region["region_name"] == region_name)
    except StopIteration:
        logger.warning(f"Region {region_name} not found")
        return

    cities = selected_region["cities"]
    markup = generate_cities_markup(user_id, cities)
    await call.message.edit_text("Выберите город, для которого хотите узнать доступные курсы валют:", reply_markup=markup)

async def handle_city_choice(call: types.CallbackQuery):
    user_id = call.from_user.id
    city_name = call.data.split(':')[1]
    city_code = locations_data.city_name_to_code[city_name]

    rates = await cache_data.get_exchange_rates_by_city_code(city_code)
    text = ''

    text += f"Курсы валют в городе {city_name}:\n"
    for rate in rates:
        text += f"{rate['bank_name']}:\n"
        text += f"USD: Покупка: {rate['usd_purchase']} | Продажа: {rate['usd_sale']}\n"
        text += f"EUR: Покупка: {rate['eur_purchase']} | Продажа: {rate['eur_sale']}\n"
        text += f"RUB: Покупка: {rate['rub_purchase']} | Продажа: {rate['rub_sale']}\n\n"

    markup = generate_common_markup(user_id)
    await call.message.edit_text(text, parse_mode=types.ParseMode.MARKDOWN, reply_markup=markup)

async def handle_return_to_regions(call: types.CallbackQuery):
    user_id = call.from_user.id
    markup = generate_regions_markup(user_id, locations_data.regions_with_cities)
    await call.message.edit_text("Выберите область:", reply_markup=markup)

async def handle_admin_button(call: types.CallbackQuery):
    if call.from_user.id in (int(x) for x in os.getenv('ADMINS').split(',')):
        stats_text = usage_data.generate_statistics_text()
        await call.message.answer(stats_text, parse_mode=types.ParseMode.MARKDOWN)
    else:
        await call.answer("You are not authorized to click this button.", show_alert=True)

async def handle_unknown(message: types.Message):
    user_id = message.from_user.id
    markup = generate_regions_markup(user_id, locations_data.regions_with_cities)
    await message.answer("Выберите область:", reply_markup=markup)
