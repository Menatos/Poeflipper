import logging.handlers
import os
from os.path import join, dirname

import discord
from discord import app_commands
from dotenv import load_dotenv

from discord_embeds import prediction_embed, refresh_embed, help_embed, price_change_embed, div_embed
from database.db_provider import create_db_tables, refresh_db_values
from helpers import last_run as lr

# Variables
server_id = 696033204179697795
guild = discord.Object(id=server_id)
timestamp = lr.get_last_run_time_stamp()

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


@tree.command(
    name="divcards_currency",
    description="Show all currency divination cards which can be profitably flipped",
    guild=guild,
)
async def send(ctx):
    await div_embed(ctx=ctx, Currency=True)


@tree.command(
    name="divcards_uniques",
    description="Show all unique divination cards which can be profitably flipped",
    guild=guild,
)
async def send(ctx):
    await div_embed(ctx=ctx, Unique=True)


@tree.command(
    name="divcards_fragments",
    description="Show all fragment divination cards which can be profitably flipped",
    guild=guild,
)
async def send(ctx):
    await div_embed(ctx=ctx, Fragment=True)


@tree.command(
    name="divcards_skillgems",
    description="Show all skillgem divination cards which can be profitably flipped",
    guild=guild,
)
async def send(ctx):
    await div_embed(ctx=ctx, SkillGem=True)


@tree.command(
    name="price_changes",
    description="Show all items which prices have changed more than 30%",
    guild=guild,
)
async def send(ctx):
    await price_change_embed(ctx=ctx)


@tree.command(
    name="predict_prices",
    description="Try to predict prices based on previous league data",
    guild=guild,
)
async def send(ctx, item_name: str):
    await prediction_embed(ctx=ctx, item_name=item_name)


@tree.command(
    name="help", description="What does this bot do? How do i use it?", guild=guild
)
async def send(ctx):
    await help_embed(ctx=ctx)


@tree.command(
    name="refresh_database", description="Refresh poe.ninja data", guild=guild
)
async def send(ctx):

    try:
        await refresh_embed(ctx)
        create_db_tables()
        refresh_db_values()
    except:
        await ctx.response.send_message(
            content="Error refreshing data. Please contact @felgae or @menatos"
        )


@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=server_id))
    print(f"We have logged in as {client.user}")


discord_token = os.environ.get("DISCORD_BOT_TOKEN")
client.run(discord_token, log_handler=handler)
