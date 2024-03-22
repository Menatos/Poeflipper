import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

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
timestamp = lr.get_last_run_time_stamp()

# ENV
env_path = join(dirname(__file__), "../.env")
load_dotenv(env_path)

# DISCORD LOGGING HANDLER
logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
logging.getLogger("discord.http").setLevel(logging.INFO)

if os.environ.get("ENVIRONMENT") == "production":
    log_path = "logs/discord.log"
    os.makedirs("logs", exist_ok=True)
else:
    log_path = "../logs/discord.log"
    os.makedirs("../logs", exist_ok=True)

handler = logging.handlers.RotatingFileHandler(
    filename=log_path,
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
)
async def send(ctx):
    await div_embed(ctx=ctx, Currency=True)


@tree.command(
    name="divcards_uniques",
    description="Show all unique divination cards which can be profitably flipped",
)
async def send(ctx):
    await div_embed(ctx=ctx, Unique=True)


@tree.command(
    name="divcards_fragments",
    description="Show all fragment divination cards which can be profitably flipped",
)
async def send(ctx):
    await div_embed(ctx=ctx, Fragment=True)


@tree.command(
    name="divcards_skillgems",
    description="Show all skillgem divination cards which can be profitably flipped",
)
async def send(ctx):
    await div_embed(ctx=ctx, SkillGem=True)


@tree.command(
    name="price_changes",
    description="Show all items which prices have changed more than 30%",
)
async def send(ctx):
    await price_change_embed(ctx=ctx)


@tree.command(
    name="predict_prices",
    description="Try to predict prices based on previous league data",
)
async def send(ctx, item_name: str):
    await prediction_embed(ctx=ctx, item_name=item_name)


@tree.command(
    name="help", description="What does this bot do? How do i use it?"
)
async def send(ctx):
    await help_embed(ctx=ctx)


@tree.command(
    name="refresh_database", description="Refresh poe.ninja data"
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
    await tree.sync()
    print(f"We have logged in as {client.user}")


discord_token = os.environ.get("DISCORD_BOT_TOKEN")
client.run(discord_token, log_handler=handler)
