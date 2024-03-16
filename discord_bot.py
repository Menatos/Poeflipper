import discord
import os
import logging.handlers
import calculations
from dotenv import load_dotenv
from os.path import join, dirname
from discord import app_commands

# Variables
server_id = 696033204179697795
max_string_length = 2000
guild = discord.Object(id=server_id)

# ENV
env_path = join(dirname(__file__), ".env")
load_dotenv(env_path)

# DISCORD LOGGING HANDLER
os.makedirs("logs", exist_ok=True)
logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
logging.getLogger("discord.http").setLevel(logging.INFO)

handler = logging.handlers.RotatingFileHandler(
    filename="logs/discord.log",
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

async def process_chunks(input_string, chunk_size, processing_function):
    chunks = "\n".join(input_string).split("\n")
    current_chunk = ""

    for chunk in chunks:
        if len(current_chunk) + len(chunk) + 1 <= chunk_size:
            current_chunk += chunk + "\n"
        else:
            await processing_function(current_chunk[:-1])  # Remove the trailing "|"
            current_chunk = chunk + "\n"

    if current_chunk:
        await processing_function(
            current_chunk[:-1]
        )  # Process the last chunk without the trailing "|"


@tree.command(
    name="divcards_currency",
    description="Flip currency cards",
    guild=guild
)
async def send(ctx):
    card_data = calculations.calculate_divination_card_difference(
        currency=True
    )
    await process_chunks(card_data, max_string_length, ctx.channel.send)
    await ctx.response.send_message(content='Currency', delete_after=10)
    await ctx.followup.send('Test followup')

@tree.command(
    name="divcards_uniques",
    description="Flip unique cards",
    guild=guild
)
async def send(ctx):
    card_data = calculations.calculate_divination_card_difference(
        unique=True
    )
    await process_chunks(card_data, max_string_length, ctx.channel.send)
    await ctx.response.send_message(content='Uniques', delete_after=10)
    await ctx.followup.send('Test followup')

@tree.command(
    name="divcards_fragments",
    description="Flip fragment cards",
    guild=guild
)
async def send(ctx):
    card_data = calculations.calculate_divination_card_difference(
        fragment=True
    )
    await process_chunks(card_data, max_string_length, ctx.channel.send)
    await ctx.response.send_message(content='Fragment', delete_after=10)
    await ctx.followup.send('Test followup')

@tree.command(
    name="divcards_skillgems",
    description="Flip Skillgem cards",
    guild=guild
)
async def send(ctx):
    card_data = calculations.calculate_divination_card_difference(
        skillGem=True
    )
    await process_chunks(card_data, max_string_length, ctx.channel.send)
    await ctx.response.send_message(content='Skillgems', delete_after=10)
    await ctx.followup.send('Test followup')

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=server_id))
    print(f"We have logged in as {client.user}")


discord_token = os.environ.get("DISCORD_BOT_TOKEN")
client.run(discord_token, log_handler=handler)