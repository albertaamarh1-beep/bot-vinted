import discord
from discord.ext import commands
import asyncio
import requests
import os

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = 1488540243266375877

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

sent_items = set()

async def vinted_loop():
    await bot.wait_until_ready()
    channel = bot.get_channel(CHANNEL_ID)

    print("Boucle démarrée")

    while not bot.is_closed():
        try:
            print("Recherche Vinted...")

            url = "https://www.vinted.fr/api/v2/catalog/items"
            params = {
                "search_text": "iphone",
                "price_from": 50,
                "price_to": 250,
                "order": "newest_first",
                "per_page": 5
            }

            headers = {
                "User-Agent": "Mozilla/5.0"
            }

            response = requests.get(url, params=params, headers=headers)
            print("HTTP", response.status_code)

            if response.status_code == 200:
                data = response.json()
                items = data.get("items", [])

                for item in items:
                    item_id = item["id"]

                    if item_id not in sent_items:
                        title = item["title"]
                        price = item["price"]
                        url_item = item["url"]

                        message = f"📱 **{title}**\n💰 {price}€\n🔗 {url_item}"
                        await channel.send(message)

                        sent_items.add(item_id)

            await asyncio.sleep(20)

        except Exception as e:
            print("ERREUR:", e)
            await asyncio.sleep(20)

@bot.event
async def on_ready():
    print(f"Bot connecté en tant que {bot.user}")
    bot.loop.create_task(vinted_loop())
    print("Task lancée")

bot.run(TOKEN)
