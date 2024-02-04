import discord
from discord.ext import tasks, commands
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import requests
from bs4 import BeautifulSoup
import datetime
import pytz
import asyncio
import os
from keepAlive import keep_alive

generated_urls = []

# Configuración del bot Discord
token = "MTE5OTA3ODEzMjM4OTUxNTM3NA.GBFLFO.Se9gouVx-0u523Lb9G9G6r2x_lbE5ABZ-9PYog"
CHANNEL_ID = 1195004269363990578
target_role_id = 1194868944213913681
intents = discord.Intents.default()
intents.voice_states = True
intents.messages = True
intents.message_content = True
prefix = "!"  # prefijo
bot = commands.Bot(command_prefix=prefix, intents=intents)

# Configuración del navegador Selenium
chrome_options = Options()
chrome_options.add_argument('--headless')
mobile_emulation = {
    "deviceMetrics": {"width": 420, "height": 680, "pixelRatio": 2.0},
    "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E304 Safari/602.1",
}
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

driver = webdriver.Chrome(options=chrome_options)
# Función para generar la URL
async def generar_url():
    now = datetime.datetime.now(pytz.timezone('America/Los_Angeles'))

    if 10 <= now.hour < 15:
      now = now.replace(hour=10, minute=0, second=0)
    elif 15 <= now.hour < 20:
      now = now.replace(hour=15, minute=0, second=0)
    else:
      now = now.replace(hour=20, minute=0, second=0)


    formatted_month = now.strftime('%m').lstrip('0')
    formatted_day = now.strftime('%d').lstrip('0')
    formatted_hour = now.strftime('%I%p').lower().lstrip('0')

    url = f'https://www.yews.news/edition/{formatted_month}{formatted_day}-24-{formatted_hour}'
    generated_urls.append(url)


# Función para capturar y enviar capturas de pantalla
async def capture_and_send_screenshot():
    if generated_urls:
        url = generated_urls[-1]  # Tomar la última URL generada
    driver.get(url)
    time.sleep(5)

    screenshot_path = 'screenshot.png'
    driver.save_screenshot(screenshot_path)

    channel = bot.get_channel(CHANNEL_ID)
    role = discord.utils.get(channel.guild.roles, id=target_role_id)

    if channel and role:
        mention = role.mention
        message_content = f"{mention} ¡Nuevas Yews! \n {url}"

        await channel.send(message_content, file=discord.File(screenshot_path))
    else:
        print(f"Canal con ID: {CHANNEL_ID} o el rol con ID: {target_role_id} no fue encontrado.")

@tasks.loop(hours=1)
async def generate_url_task():
    await generar_url()

@tasks.loop(minutes=30)
async def capture_screenshot():
    await capture_and_send_screenshot()

@bot.command(name='today')
async def today(ctx):
    if generated_urls:
        await ctx.send('\n'.join(generated_urls))
    else:
        print("No URLs generated yet.")


@bot.event
async def on_ready():
    print(f'Conectado como {bot.user.name}')

    
    generate_url_task.start()
    capture_screenshot.start()

keep_alive()

bot.run(token)
