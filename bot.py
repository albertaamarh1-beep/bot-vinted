import discord
import requests
import asyncio
import os
from flask import Flask
from threading import Thread

TOKEN = os.getenv("DISCORD_TOKEN")

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running"

def run_web():
    app.run(host="0.0.0.0", port=10000)

def keep_alive():
    t = Thread(target=run_web)
    t.start()

intents = discord.Intents.default()
bot = discord.Client(intents=intents)

CHANNEL_ID = 1488540243266375877

async def vinted_loop():
    print("Boucle démarrée")

    await bot.wait_until_ready()

    while not bot.is_closed():
        print("Recherche Vinted...")

        try:
            url = "https://www.vinted.fr/api/v2/catalog/items?search_text=nike"
            headers = {
                "User-Agent": "Mozilla/5.0"
            }

            response = requests.get(url, headers=headers)
            print("HTTP", response.status_code)

            if response.status_code == 200:
                data = response.json()
                items = data.get("items", [])

                if items:
                    item = items[0]
                    title = item["title"]
                    price = item["price"]["amount"]
                    link = item["url"]

                    channel = bot.get_channel(CHANNEL_ID)
                    if channel:
                        await channel.send(f"🔥 {title}\n💰 {price}€\n🔗 {link}")

        except Exception as e:
            print("ERREUR :", e)

        await asyncio.sleep(20)

@bot.event
async def on_ready():
    print(f"Bot connecté en tant que {bot.user}")
    asyncio.create_task(vinted_loop())

print("Script démarré")

keep_alive()
bot.run(TOKEN)
