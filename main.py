import discord
import requests
from datetime import datetime
import os

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)

def get_next_version():
    now = datetime.now()
    year = now.year + (now.month // 12)
    month = now.month % 12 + 1
    return f"{year}{month:02d}"  # e.g., 202506

def generate_urls(version):
    base = f"https://game-lgtmtmg.line-scdn.net/COMMON/G{version}/images/"
    paths = [
        "event_banner/info_main_en.png",
        "event/main_header_en.png",
        "event_banner/info_score_en.png",
        "event_banner/heartsale_en.png",
        "event_banner/itemsale_en.png",
        "event_banner/info_bnr_boxbonus_en.png",
        "event_banner/index_doubleup_2_en.png",
        "box/box01_l_en.png",
        "box/box02_l_en.png",
        "box/box03_z_en.png",
        "box/list_01_l_en.png",
        "box/list_02_l_en.png",
        "box/list_03_l_en.png",
        "box/list_04_l_en.png",
        "box/list_05_l_en.png",
        "select/select01_head_en.png",       
        "select/select01_list_en.png",
        "select/select02_head_en.png",
        "select/select02_list_en.png",
        "select/select03_head_en.png",
        "select/select03_list_en.png",
        "select/select03_head_en.png",
        "pick/pick01_img_en.png",
        "pick/pick01_limit_en.png",
        "pick/pick02_img_en.png",
        "pick/pick02_limit_en.png",
        "boxbonus/boxbonus_en.png",
        "event/score_header_en.png",
        "raffle/raffle_header_en.png",
        "event/sticker_header_en.png",
        "event/scratch_header_en.png",
        "bingo/bingo_header_en.png",
    ]
    return [base + path for path in paths]

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user.name}")
    await send_images()
    await client.close()  # ⛔ 這是關鍵：執行完後結束 bot.run()

async def send_images():
    version = get_next_version()
    thread_name = f"{version}"
    urls = generate_urls(version)

    channel = client.get_channel(CHANNEL_ID)

    if channel is None:
        print("❌ Channel not found. Check CHANNEL_ID.")
        return

    existing_threads = list(channel.threads)

    # 加入 archived threads
    archived_threads = []
    async for thread in channel.archived_threads(limit=50):
        archived_threads.append(thread)

    existing_threads += archived_threads

    for t in existing_threads:
        if t.name == thread_name:
            print(f"🛑 Thread '{thread_name}' already exists (even archived). Skipping creation.")
            return

    valid_urls = [url for url in urls if requests.get(url).status_code == 200]

    if not valid_urls:
        print("ℹ️ No valid image URLs found.")
        return

    thread = await channel.create_thread(name=thread_name, type=discord.ChannelType.public_thread)

    for i in range(0, len(valid_urls), 10):
        embeds = []
        for url in valid_urls[i:i+10]:
            embed = discord.Embed()
            embed.set_image(url=url)
            embeds.append(embed)
        await thread.send(embeds=embeds)

client.run(TOKEN)
