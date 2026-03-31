import discord
from discord.ext import commands
import os
import asyncio
import threading
import requests
from flask import Flask

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

sent_items = set()

async def auto_vinted():
    await bot.wait_until_ready()
    channel = bot.get_channel(1488540243266375877)

    while True:
        try:
            url = "https://www.vinted.fr/api/v2/catalog/items"
            params = {
                "search_text": "iPhone 11 12 13 14 15",
                "price_from": 50,
                "price_to": 250,
                "order": "newest_first",
                "per_page": 5
            }

            response = requests.get(url, params=params)
            data = response.json()
            items = data.get("items", [])

            for item in items:
                item_id = item["id"]

                if item_id not in sent_items:
                    sent_items.add(item_id)

                    title = item["title"]
                    price = item["price"]
                    url_item = item["url"]

                    message = f"📱 **{title}**\n💰 {price}€\n🔗 {url_item}"
                    await channel.send(message)

        except Exception as e:
            print("Erreur Vinted:", e)

        await asyncio.sleep(20)

@bot.event
async def on_ready():
    print(f"Bot connecté en tant que {bot.user}")
    bot.loop.create_task(auto_vinted())

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running"

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run).start()

bot.run(TOKEN)
