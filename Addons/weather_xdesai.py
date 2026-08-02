"""Zelretch Addon: Advanced Weather

Provides detailed weather data with optional API configuration.

Category: Information
Maintainer: Siam Chowdhury
GitHub: https://github.com/ChowdhurySiam
Telegram: @Ch0wdhury_Siam
"""

ZELRETCH_MODULE_INFO = {'title': 'Advanced Weather', 'icon': '⛅', 'category': 'Information', 'description': 'Provides detailed weather data with optional API configuration.', 'developer': 'Siam Chowdhury', 'github': 'https://github.com/ChowdhurySiam', 'telegram': 'https://t.me/Ch0wdhury_Siam'}



import os
from pyrogram import Client
from command import zel_command, zel_sudo, who_message, get_text
from requirements_installer import install_library
install_library("requests -U")
import requests

def load_config():
    api_key = os.environ.get("OPENWEATHER_API_KEY", "").strip()
    if not api_key:
        try:
            with open("userdata/weather_setting", "r", encoding="utf-8") as f:
                api_key = f.read().strip()
        except FileNotFoundError:
            api_key = ""
    return {"api_key": api_key}

def save_config(api_key):
    with open("userdata/weather_setting", "w", encoding="utf-8") as f:
        f.write(api_key)

LANGUAGES = {'en': {'weather_info': '<emoji id=5884330496619450755>☁️</emoji> <b>Weather in {city}, '
                        '{country}:</b>\n'
                        '<emoji id=5199707727475007907>🌡️</emoji> <b>Temperature: {temperature}°C '
                        '(feels like {feels_like}°C)</b>\n'
                        '<emoji id=6050944866580435869>💧</emoji> <b>Humidity: {humidity}%</b>\n'
                        '<emoji id=5415843564280107382>🌀</emoji> <b>Wind speed: {wind_speed} '
                        'm/s</b>\n'
                        '<emoji id=5417937876232983047>⛅️</emoji> <b>Sky: {description}</b>',
        'error': '<b>Error:</b> <code>{e}</code>',
        'api_error': '<b>City not found: {city}\nAPI response:</b> <code>{data}</code>',
        'invalid_args': '<emoji id=5019523782004441717>❌</emoji> <b>Specify the city.</b>',
        'config_saved': '✅ <b>API key saved:</b> <code>{api_key}</code>',
        'current_config': '🔑 <b>Current API key:</b> <code>{api_key}</code>',
        'help_text': '🌤️ <b>Weather Module</b>\n'
                     '\n'
                     '<code>weather [city]</code> - Check weather in specified city\n'
                     '<code>weather_config [api_key]</code> - Set OpenWeatherMap API key\n'
                     '\n'
                     'API key can be obtained from: https://openweathermap.org/api'}}

filename = os.path.basename(__file__)
Module_Name = "Weather"

@Client.on_message(zel_command("weather", Module_Name, filename, "[city]") & zel_sudo())
async def weather_handler(client, message):
    message = await who_message(client, message)
    
    args = message.text.split()
    if len(args) < 2:
        text = get_text(Module_Name, "invalid_args", LANGUAGES=LANGUAGES)
        return await message.edit(text)
    
    city = " ".join(args[1:])
    config = load_config()
    api_key = config["api_key"]
    if not api_key:
        return await message.edit(
            "<b>OpenWeather API key is not configured.</b>\n"
            "Use <code>.weather_config YOUR_KEY</code> or set "
            "<code>OPENWEATHER_API_KEY</code>."
        )

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=en"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if data.get("cod") != 200:
            text = get_text(Module_Name, "api_error", LANGUAGES=LANGUAGES, city=city, data=str(data))
            return await message.edit(text)

        country = data["sys"]["country"]
        weather_data = data["main"]
        temperature = weather_data["temp"]
        feels_like = weather_data["feels_like"]
        wind_speed = data["wind"]["speed"]
        humidity = weather_data["humidity"]
        description = data["weather"][0]["description"].capitalize()
        
        text = get_text(Module_Name, "weather_info", LANGUAGES=LANGUAGES,
                       city=city.capitalize(),
                       country=country,
                       description=description,
                       temperature=temperature,
                       feels_like=feels_like,
                       humidity=humidity,
                       wind_speed=wind_speed)
        
        await message.edit(text)
        
    except Exception as e:
        text = get_text(Module_Name, "error", LANGUAGES=LANGUAGES, e=str(e))
        await message.edit(text)

@Client.on_message(zel_command("weather_config", Module_Name, filename, "[api_key]") & zel_sudo())
async def weather_config_handler(client, message):
    message = await who_message(client, message)
    
    args = message.text.split()
    if len(args) < 2:
        config = load_config()
        configured = bool(config["api_key"])
        return await message.edit(
            "✅ <b>OpenWeather API key is configured.</b>"
            if configured
            else "⚠️ <b>OpenWeather API key is not configured.</b>"
        )
    
    api_key = args[1]
    save_config(api_key)
    
    text = get_text(Module_Name, "config_saved", LANGUAGES=LANGUAGES, api_key=api_key)
    await message.edit(text)

@Client.on_message(zel_command("weather_help", Module_Name, filename) & zel_sudo())
async def weather_help_handler(client, message):
    message = await who_message(client, message)
    
    text = get_text(Module_Name, "help_text", LANGUAGES=LANGUAGES)
    await message.edit(text)
