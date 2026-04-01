import discord
import asyncio
import requests
import os
from bs4 import BeautifulSoup

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = 1488540243266375877

intents = discord.Intents.default()
bot = discord.Client(intents=intents)

sent_links = set()

MODELS = [
    "iphone 11",
    "iphone 12",
    "iphone 13",
    "iphone 14",
    "iphone 15",
    "iphone 16"
]

VARIANTS = ["pro", "pro max", "mini", "plus"]

async def vinted_loop():
    await bot.wait_until_ready()
    print("BOUCLE LANCÉE")

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    while not bot.is_closed():
        try:
            url = "https://www.vinted.fr/catalog?search_text=iphone&order=newest_first"
            r = requests.get(url, headers=headers, timeout=10)
            print("STATUS:", r.status_code)

            if r.status_code == 200:
                soup = BeautifulSoup(r.text, "html.parser")
                items = soup.select("div.feed-grid__item")

                for item in items[:15]:
                    link_tag = item.find("a")
                    price_tag = item.find("p", {"data-testid": "price"})
                    img_tag = item.find("img")

                    if not link_tag or not price_tag or not img_tag:
                        continue

                    link = "https://www.vinted.fr" + link_tag["href"]
                    title = img_tag.get("alt", "").lower()
                    image = img_tag.get("src")

                    price_text = price_tag.text.strip().replace("€", "").replace(",", ".")
                    try:
                        price = float(price_text)
                    except:
                        continue

                    if link in sent_links:
                        continue

                    # Vérifie modèle
                    if not any(model in title for model in MODELS):
                        continue

                    # Autorise variantes
                    if any(v in title for v in VARIANTS) or True:
                        pass

                    if price < 50 or price > 250:
                        continue

                    sent_links.add(link)

                    embed = discord.Embed(
                        title=title.title(),
                        description=f"💰 {price}€",
                        url=link,
                        color=0x2ecc71
                    )

                    embed.set_image(url=image)

                    channel = bot.get_channel(CHANNEL_ID)
                    if channel:
                        await channel.send(embed=embed)

        except Exception as e:
            print("ERREUR:", e)

        await asyncio.sleep(10)

@bot.event
async def on_ready():
    print(f"CONNECTÉ EN TANT QUE {bot.user}")
    bot.loop.create_task(vinted_loop())

print("DÉMARRAGE DU BOT")

bot.run(TOKEN)
