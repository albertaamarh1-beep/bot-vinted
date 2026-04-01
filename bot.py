import discord
import asyncio
import requests
import os

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = 1488540243266375877  # ton salon

intents = discord.Intents.default()
bot = discord.Client(intents=intents)

async def vinted_loop():
    await bot.wait_until_ready()
    print("BOUCLE LANCÉE")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "fr-FR,fr;q=0.9",
        "Referer": "https://www.vinted.fr/",
        "Origin": "https://www.vinted.fr",
        "Connection": "keep-alive"
    }

    while not bot.is_closed():
        try:
            url = "https://www.vinted.fr/api/v2/catalog/items?search_text=iphone&order=newest_first"

            r = requests.get(url, headers=headers, timeout=10)

            print("STATUS:", r.status_code)

            if r.status_code == 200:
                data = r.json()
                items = data.get("items", [])

                if items:
                    item = items[0]
                    title = item.get("title")
                    price = item.get("price", {}).get("amount")
                    link = item.get("url")

                    channel = bot.get_channel(CHANNEL_ID)
                    if channel:
                        await channel.send(
                            f"📱 {title}\n💰 {price}€\n🔗 {link}"
                        )

        except Exception as e:
            print("ERREUR:", e)

        await asyncio.sleep(30)

@bot.event
async def on_ready():
    print(f"CONNECTÉ EN TANT QUE {bot.user}")
    bot.loop.create_task(vinted_loop())

print("DÉMARRAGE DU BOT")

bot.run(TOKEN)
