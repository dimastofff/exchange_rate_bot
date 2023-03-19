import os
from aiogram import types

def generate_regions_markup(user_id, regions_with_cities):
    markup = types.InlineKeyboardMarkup(row_width=3)
    buttons = [
        types.InlineKeyboardButton(
            region["region_name"], callback_data=f"region:{region['region_name']}")
        for region in regions_with_cities
    ]
    markup.add(*buttons)
    markup.add(*__generate_admin_panel_button(user_id))

    return markup

def generate_cities_markup(user_id, cities):
    markup = types.InlineKeyboardMarkup(row_width=3)
    city_buttons = [
        types.InlineKeyboardButton(
            city["name"], callback_data=f"city:{city['name']}")
        for city in cities
    ]
    markup.add(*city_buttons)
    markup.add(*__generate_return_to_region_button())
    markup.add(*__generate_admin_panel_button(user_id))

    return markup

def generate_common_markup(user_id):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*__generate_return_to_region_button())
    markup.add(*__generate_admin_panel_button(user_id))
    
    return markup

def __generate_admin_panel_button(user_id):
    if user_id in (int(x) for x in os.getenv('ADMINS').split(',')):
        return [types.InlineKeyboardButton("[ADMIN PANEL]", callback_data="admin")]
    return []

def __generate_return_to_region_button():
    return [types.InlineKeyboardButton("<<< Области >>>", callback_data="return_to_regions")]
