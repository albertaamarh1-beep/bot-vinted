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

    while not bot.is_closed():
        try:
            url = "https://www.vinted.fr/api/v2/catalog/items?search_text=iphone"
            headers = {"User-Agent": "Mozilla/5.0"}
            r = requests.get(url, headers=headers)

            print("STATUS:", r.status_code)

            if r.status_code == 200:
                data = r.json()
                items = data.get("items", [])

                if items:
                    item = items[0]
                    title = item["title"]
                    price = item["price"]["amount"]
                    link = item["url"]

                    channel = bot.get_channel(CHANNEL_ID)
                    if channel:
                        await channel.send(
                            f"📱 {title}\n💰 {price}€\n🔗 {link}"
                        )

        except Exception as e:
            print("ERREUR:", e)

        await asyncio.sleep(20)

@bot.event
async def on_ready():
    print(f"CONNECTÉ EN TANT QUE {bot.user}")
    bot.loop.create_task(vinted_loop())

print("DÉMARRAGE DU BOT")

bot.run(TOKEN)
