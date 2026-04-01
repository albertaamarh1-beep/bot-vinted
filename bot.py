import discord
import requests
import asyncio
import os
from flask import Flask
from threading import Thread

TOKEN = os.getenv("TOKEN")

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running"

def run_web():
    app.run(host="0.0.0.0", port=10000)

Thread(target=run_web).start()

intents = discord.Intents.default()
bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print("BOT CONNECTÉ")

    while True:
        print("JE TOURNE")

        try:
            url = "https://www.vinted.fr/api/v2/catalog/items?search_text=nike"
            headers = {"User-Agent": "Mozilla/5.0"}
            r = requests.get(url, headers=headers)
            print("STATUS:", r.status_code)
        except Exception as e:
            print("ERREUR:", e)

        await asyncio.sleep(20)

print("SCRIPT LANCÉ")

bot.run(TOKEN)
