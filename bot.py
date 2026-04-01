import discord
import asyncio
import requests
import os
from flask import Flask
from threading import Thread

TOKEN = os.getenv("TOKEN")

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is alive"

def run_web():
    app.run(host="0.0.0.0", port=10000)

intents = discord.Intents.default()
bot = discord.Client(intents=intents)

async def vinted_loop():
    await bot.wait_until_ready()
    print("BOUCLE DÉMARRÉE")

    while not bot.is_closed():
        print("JE TOURNE")

        try:
            url = "https://www.vinted.fr/api/v2/catalog/items?search_text=nike"
            headers = {"User-Agent": "Mozilla/5.0"}
            r = requests.get(url, headers=headers)
            print("STATUS:", r.status_code)
        except Exception as e:
            print("ERREUR:", e)

        await asyncio.sleep(20)

@bot.event
async def on_ready():
    print(f"CONNECTÉ : {bot.user}")

bot.loop.create_task(vinted_loop())

Thread(target=run_web).start()

print("SCRIPT LANCÉ")

bot.run(TOKEN)
