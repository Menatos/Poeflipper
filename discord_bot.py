import discord
import os
import logging.handlers
import calculations
from dotenv import load_dotenv
from os.path import join, dirname

# ENV
env_path = join(dirname(__file__), '.env')
load_dotenv(env_path)

# DISCORD LOGGING HANDLER
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
logging.getLogger('discord.http').setLevel(logging.INFO)

handler = logging.handlers.RotatingFileHandler(
    filename='logs/discord.log',
    encoding='utf-8',
    maxBytes=32 * 1024 * 1024,  # 32 MiB
    backupCount=5,  # Rotate through 5 files
)
dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
handler.setFormatter(formatter)
logger.addHandler(handler)

# BOT
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

commands = {
    '$divinationcards_currency',
    '$divinationcards_uniques',
    '$divinationcards_fragments',
    '$divinationcards_skillgems',
}


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
        await processing_function(current_chunk[:-1])  # Process the last chunk without the trailing "|"

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    max_string_length = 2000

    if message.author == client.user:
        return

    if message.content.startswith('$divinationcards_currency'):
        card_data = await calculations.calculate_divination_card_difference(currency=True)
        await process_chunks(card_data, max_string_length, message.channel.send)
    if message.content.startswith('$divinationcards_uniques'):
        card_data = await calculations.calculate_divination_card_difference(unique=True)
        await process_chunks(card_data, max_string_length, message.channel.send)
    if message.content.startswith('$divinationcards_fragments'):
        card_data = await calculations.calculate_divination_card_difference(fragment=True)
        await process_chunks(card_data, max_string_length, message.channel.send)
    if message.content.startswith('$divinationcards_skillGems'):
        card_data = await calculations.calculate_divination_card_difference(skillGem=False)
        await process_chunks(card_data, max_string_length, message.channel.send)


discord_token = os.environ.get('DISCORD_BOT_TOKEN')
client.run(discord_token, log_handler=handler)
