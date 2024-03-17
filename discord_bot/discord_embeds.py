import random

import discord
from discord import Embed

import index
from helpers import calculations
from helpers import last_run as lr

max_string_length = 2000
version = index.version
last_run = lr.get_last_run_time_stamp().strftime("%d.%m.%y %H:%M:%S")

base_embed = {
    "title": "base_embed title",
    "type": "rich",
    "description": "base_embed description",
    "url": "https://poe.ninja/",
    "color": int(discord.Color.blue()),
    "footer": {
        "text": f"Alle Werte werden anhand der aktuellen poe.ninja Preise berechnet.\n"
        f"Letzte Aktualisierung der Daten: {last_run}. Poeflipper v{version}"
    },
    "thumbnail": {
        "url": "https://upload.wikimedia.org/wikipedia/en/0/08/Path_of_Exile_Logo.png?20171206230851"
    },
}


def split_string_longer_than_limit(text, limit):
    if len(text) <= limit:
        return [text]

    chunks = []
    current_chunk = ""
    for line in text.split("\n"):
        if len(current_chunk) + len(line) <= limit:
            current_chunk += line + "\n"
        else:
            chunks.append(current_chunk.strip())
            current_chunk = line + "\n"

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def process_chunks(
    input_string, ctx, chunk_size=max_string_length, card_type="Divination Card"
):
    embeds = []
    chunks = "\n".join(input_string).split("\n")
    current_chunk = ""

    for chunk in chunks:
        title = card_type
        if len(current_chunk) + len(chunk) + 1 <= chunk_size:
            current_chunk += chunk + "\n"
        else:
            embed = base_embed
            embed["title"] = title
            embed["description"] = current_chunk[:-1]

            embed = Embed.from_dict(embed)

            embed.add_field(name="Profit pro Karte >= 50", value="__***Beispiel***__")
            embed.add_field(name="Profit pro Karte >= 25", value="**Beispiel**")
            embeds.append(embed)

            current_chunk = chunk + "\n"

    if current_chunk:
        embed = base_embed
        embed["title"] = title
        embed["description"] = current_chunk[:-1]

        embed = Embed.from_dict(embed)

        embed.add_field(name="Profit pro Karte >= 50", value="__***Beispiel***__")
        embed.add_field(name="Profit pro Karte >= 25", value="**Beispiel**")

        embeds.append(embed)
    return embeds


def generate_price_change_embeds(data):
    embeds = []

    for key, values in data.items():
        description_string = ""
        if len(values):
            for item in values:
                if item["total_change"] >= 200:
                    item_string = f'> {item["name"]} > {item["value"]}c > __***{item["total_change"]}***__%\n'
                elif item["total_change"] >= 100:
                    item_string = f'> {item["name"]} > {item["value"]}c > **{item["total_change"]}**%\n'
                elif item["total_change"] >= 50:
                    item_string = f'> {item["name"]} > {item["value"]}c > __{item["total_change"]}__%\n'
                elif item["total_change"] <= -50:
                    item_string = f'> ~~{item["name"]} > {item["value"]}c > {item["total_change"]}~~%\n'
                else:
                    item_string = f'> {item["name"]} > {item["value"]}c > {item["total_change"]}%\n'

                description_string += item_string

            if len(description_string) >= 4096:
                limited_strings = split_string_longer_than_limit(
                    description_string, 4096
                )

                for limited_description in limited_strings:
                    embed = base_embed
                    embed["title"] = key
                    embed["description"] = limited_description

                    embed = Embed.from_dict(embed)

                    embed.add_field(name="Änderung >= 200%", value="__***Beispiel***__")
                    embed.add_field(name="Änderung >= 100%", value="**Beispiel**")
                    embed.add_field(name="Änderung >= 50%", value="__Beispiel__")

                    embeds.append(embed)
            else:
                embed = base_embed
                embed["title"] = key
                embed["description"] = description_string

                embed = Embed.from_dict(embed)

                embed.add_field(name="Änderung >= 200%", value="__***Beispiel***__")
                embed.add_field(name="Änderung >= 100%", value="**Beispiel**")
                embed.add_field(name="Änderung >= 50%", value="__Beispiel__")

                embeds.append(embed)

    return embeds


def calculate_embeds_length(embeds):
    total_length = 0
    for embed in embeds:
        # Calculate length based on your object's attributes or any relevant criteria
        # For example, if your object has a 'length' attribute:
        total_length += len(embed)
    return total_length


async def send_response(embeds, ctx):
    i = 0
    print(embeds)
    for embed in embeds:
        if i == 0:
            await ctx.response.send_message(embed=embed)
        else:
            await ctx.followup.send(embed=embed)
        i += 1


async def send_followup(embeds, ctx):
    for embed in embeds:
        await ctx.followup.send(embed=embed)


async def limit_embed_size(ctx, embeds):
    total_length = calculate_embeds_length(embeds)
    if total_length <= 5999 and len(embeds) <= 10:
        # If total length is smaller than or equal to 5999, execute the function directly
        await send_response(embeds, ctx)
    else:
        chunk_size = 0
        current_chunk = []
        for embed in embeds:
            current_length = calculate_embeds_length([embed])
            if chunk_size + current_length > 5999 and ctx.response.is_done() is False:
                await send_response(current_chunk, ctx)
                chunk_size = 0
                current_chunk = []
            elif chunk_size + current_length > 5999 and ctx.response.is_done() is True:
                await send_followup(current_chunk, ctx)
                chunk_size = 0
                current_chunk = []
            current_chunk.append(embed)
            chunk_size += current_length
        if current_chunk:
            await send_followup(current_chunk, ctx)


async def div_embed(ctx, **kwargs):
    card_data = calculations.calculate_divination_card_difference(**kwargs)

    for key, value in kwargs.items():
        embeds = process_chunks(card_data, ctx, max_string_length, key)

    await limit_embed_size(ctx, embeds)


async def price_change_embed(ctx):
    price_change_data = calculations.calculate_price_change()

    embeds = generate_price_change_embeds(price_change_data)

    await limit_embed_size(ctx, embeds)


async def refresh_embed(ctx):
    embed = base_embed
    embed["title"] = "Datenbank wird aktualisiert"
    embed["description"] = "Refreshing poe.ninja data... please wait"

    embed = Embed.from_dict(embed)

    await ctx.response.send_message(embed=embed, delete_after=45)


async def help_embed(ctx):
    embed = base_embed
    embed["title"] = "Was kann Poeflipper?"
    embed["description"] = (
        "Es werden grundsätzlich Items ausgefiltert, bei welchen nur wenige Exemplare auf dem Markt sind. Folgende Funktionen sind aktuell verfügbar:"
    )

    embed = Embed.from_dict(embed)

    embed.add_field(
        name="/divcards_currency",
        value="```Der Wert der divinationcard rewards wird mit den Kosten verglichen.```",
        inline=False,
    )
    embed.add_field(
        name="/divcards_uniques",
        value="```Der Wert der divinationcard rewards wird mit den Kosten verglichen. Dabei werden Links oder das Map-Tier berücksichtigt```",
        inline=False,
    )
    embed.add_field(
        name="/divcards_fragments",
        value="```Der Wert der divinationcard rewards wird mit den Kosten verglichen.```",
        inline=False,
    )
    embed.add_field(
        name="/divcards_skillgems",
        value="```Der Wert der divinationcard reward wird mit den Kosten verglichen. Gemlevel, Korruption und Qualität werden berücksichtigt.```",
        inline=False,
    )
    embed.add_field(
        name="/price_changes",
        value="```Für jede Itemkategorie werden die Preisänderungen der letzten 7 Tage angezeigt, wenn sie größer als 30% sind und das Item mehr als 10 Chaos kostet. Besonders starke Veränderungen in beide Richtungen werden markiert.```",
        inline=False,
    )
    embed.add_field(
        name="/refresh_database",
        value="```Lädt die Datenbank mit neuen Daten. Standardmäßig geschieht dies automatisch alle 30 Minuten.```",
        inline=False,
    )

    await ctx.response.send_message(embed=embed)
