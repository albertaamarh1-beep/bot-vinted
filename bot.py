import discord
import asyncio
import requests
import os
from bs4 import BeautifulSoup

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = 1488540243266375877  # ton salon

intents = discord.Intents.default()
bot = discord.Client(intents=intents)

async def vinted_loop():
    await bot.wait_until_ready()
    print("BOUCLE LANCÉE")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    while not bot.is_closed():
        try:
            url = "https://www.vinted.fr/catalog?search_text=iphone"

            r = requests.get(url, headers=headers, timeout=10)
            print("STATUS:", r.status_code)

            if r.status_code == 200:
                soup = BeautifulSoup(r.text, "html.parser")

                items = soup.select("a.new-item-box__overlay")

                if items:
                    first = items[0]
                    link = "https://www.vinted.fr" + first["href"]

                    channel = bot.get_channel(CHANNEL_ID)
                    if channel:
                        await channel.send(f"📱 Nouvelle annonce :\n🔗 {link}")

        except Exception as e:
            print("ERREUR:", e)

        await asyncio.sleep(30)

@bot.event
async def on_ready():
    print(f"CONNECTÉ EN TANT QUE {bot.user}")
    bot.loop.create_task(vinted_loop())

print("DÉMARRAGE DU BOT")

bot.run(TOKEN)
