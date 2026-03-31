import discord
from discord.ext import commands
import os
import asyncio
import threading
from flask import Flask

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

async def auto_message():
    await bot.wait_until_ready()
    channel = discord.utils.get(bot.get_all_channels(), name="annonce-Vinted")

    while not bot.is_closed():
        print("La boucle tourne")
        if channel:
            await channel.send("🚀 Test automatique actif")
        else:
            print("Salon non trouvé")
        await asyncio.sleep(60)

@bot.event
async def on_ready():
    print(f"Bot connecté en tant que {bot.user}")
    bot.loop.create_task(auto_message())

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running"

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run).start()

bot.run(TOKEN)
