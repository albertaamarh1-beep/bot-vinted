import discord
import asyncio
import requests
import os

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = 1488540243266375877

intents = discord.Intents.default()
bot = discord.Client(intents=intents)

sent_ids = set()

MODELS = [
    "iphone 11",
    "iphone 12",
    "iphone 13",
    "iphone 14",
    "iphone 15",
    "iphone 16",
    "iphone 17"
]

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

async def search_model(model):
    url = (
        "https://www.vinted.fr/api/v2/catalog/items"
        f"?search_text={model.replace(' ', '%20')}"
        "&price_from=50"
        "&price_to=200"
        "&order=newest_first"
    )

    r = requests.get(url, headers=headers)

    print(model, "STATUS:", r.status_code)

    if r.status_code != 200:
        return []

    data = r.json()
    items = data.get("items", [])

    results = []

    for item in items:
        item_id = item.get("id")
        if item_id in sent_ids:
            continue

        title = item.get("title", "")
        price = item.get("price", {}).get("amount")
        link = item.get("url")
        image = item.get("photo", {}).get("url")

        if not title or not price or not link or not image:
            continue

        results.append((item_id, title, price, link, image))

    return results


async def vinted_loop():
    await bot.wait_until_ready()
    print("BOUCLE LANCÉE")

    while not bot.is_closed():
        try:
            for model in MODELS:
                results = await search_model(model)

                for item_id, title, price, link, image in results:
                    sent_ids.add(item_id)

                    embed = discord.Embed(
                        title=title,
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
