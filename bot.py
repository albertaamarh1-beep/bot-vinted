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

VALID_MODELS = [
    "iphone 11",
    "iphone 12",
    "iphone 13",
    "iphone 14",
    "iphone 15",
    "iphone 16",
    "iphone 17"
]

async def vinted_loop():
    await bot.wait_until_ready()
    print("BOUCLE LANCÉE")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    while not bot.is_closed():
        try:
            url = "https://www.vinted.fr/catalog?search_text=iphone&order=newest_first"
            r = requests.get(url, headers=headers, timeout=10)
            print("STATUS:", r.status_code)

            if r.status_code == 200:
                soup = BeautifulSoup(r.text, "html.parser")
                items = soup.select("div.feed-grid__item")

                for item in items[:40]:
                    link_tag = item.find("a", href=True)
                    price_tag = item.find("p", {"data-testid": "price"})
                    img_tag = item.find("img")

                    if not link_tag or not price_tag or not img_tag:
                        continue

                    # ----- Lien sécurisé -----
                    href = link_tag["href"]
                    if href.startswith("http"):
                        link = href
                    else:
                        link = "https://www.vinted.fr" + href

                    if link in sent_links:
                        continue

                    # ----- Titre -----
                    title = img_tag.get("alt", "").lower()

                    if not any(model in title for model in VALID_MODELS):
                        continue

                    # ----- Image fix -----
                    image = (
                        img_tag.get("src")
                        or img_tag.get("data-src")
                        or img_tag.get("data-original")
                    )

                    if image and image.startswith("//"):
                        image = "https:" + image

                    if not image:
                        continue

                    # ----- Prix -----
                    price_text = (
                        price_tag.text
                        .strip()
                        .replace("€", "")
                        .replace(",", ".")
                    )

                    try:
                        price = float(price_text)
                    except:
                        continue

                    if price < 50 or price > 200:
                        continue

                    # ----- Ajout anti-duplicate -----
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
