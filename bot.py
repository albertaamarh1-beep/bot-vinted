import discord
import requests
import asyncio
import os
from flask import Flask
from threading import Thread

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = 1488540243266375877

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running"

def run_web():
    app.run(host="0.0.0.0", port=10000)

def keep_alive():
    Thread(target=run_web).start()

intents = discord.Intents.default()
bot = discord.Client(intents=intents)

async def vinted_loop():
    print(">>> BOUCLE DÉMARRÉE <<<")
    await bot.wait_until_ready()

    while True:
        print(">>> RECHERCHE VINTED <<<")
        try:
            url = "https://www.vinted.fr/api/v2/catalog/items?search_text=nike"
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers)
            print("HTTP STATUS:", response.status_code)
        except Exception as e:
            print("ERREUR:", e)

        await asyncio.sleep(20)

@bot.event
async def on_ready():
    print(">>> BOT CONNECTÉ <<<")
    bot.loop.create_task(vinted_loop())

print(">>> SCRIPT DÉMARRÉ <<<")

keep_alive()
bot.run(TOKEN)
