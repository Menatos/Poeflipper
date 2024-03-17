import discord
import os
import logging.handlers
from dotenv import load_dotenv
from os.path import join, dirname
from discord import app_commands

import discord_embeds

# Variables
server_id = 696033204179697795
guild = discord.Object(id=server_id)

# ENV
env_path = join(dirname(__file__), "../.env")
load_dotenv(env_path)

# DISCORD LOGGING HANDLER
os.makedirs("../logs", exist_ok=True)
logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
logging.getLogger("discord.http").setLevel(logging.INFO)

handler = logging.handlers.RotatingFileHandler(
    filename="../logs/discord.log",
    encoding="utf-8",
    maxBytes=32 * 1024 * 1024,  # 32 MiB
    backupCount=5,  # Rotate through 5 files
)
dt_fmt = "%Y-%m-%d %H:%M:%S"
formatter = logging.Formatter(
    "[{asctime}] [{levelname:<8}] {name}: {message}", dt_fmt, style="{"
)
handler.setFormatter(formatter)
logger.addHandler(handler)

# BOT
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@tree.command(name="divcards_currency", description="Flip currency cards", guild=guild)
async def send(ctx):
    await discord_embeds.div_embed(ctx=ctx, Currency=True)


@tree.command(name="divcards_uniques", description="Flip unique cards", guild=guild)
async def send(ctx):
    await discord_embeds.div_embed(ctx=ctx, Unique=True)


@tree.command(name="divcards_fragments", description="Flip fragment cards", guild=guild)
async def send(ctx):
    await discord_embeds.div_embed(ctx=ctx, Fragment=True)


@tree.command(name="divcards_skillgems", description="Flip skillgem cards", guild=guild)
async def send(ctx):
    await discord_embeds.div_embed(ctx=ctx, SkillGem=True)

@tree.command(name="price_changes", description="Show all items which prices have changed more than 30%", guild=guild)
async def send(ctx):
    await discord_embeds.price_change_embed(ctx=ctx)


@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=server_id))
    print(f"We have logged in as {client.user}")


discord_token = os.environ.get("DISCORD_BOT_TOKEN")
client.run(discord_token, log_handler=handler)
