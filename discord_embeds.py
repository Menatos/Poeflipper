# build dynamic embed list
import discord

import calculations

max_string_length = 2000


def process_chunks(input_string, ctx, chunk_size=max_string_length, card_type="Divination Card"):
    embeds = []
    chunks = "\n".join(input_string).split("\n")
    current_chunk = ""
    current_chunk_number = 1

    for chunk in chunks:
        title = card_type + " " + str(current_chunk_number)
        if len(current_chunk) + len(chunk) + 1 <= chunk_size:
            current_chunk += chunk + "\n"
        else:
            embed = discord.Embed(title=title,
                                  description=current_chunk[:-1],
                                  color=discord.Color.blue(),
                                  url="https://upload.wikimedia.org/wikipedia/en/0/08/Path_of_Exile_Logo.png?20171206230851"
                                  )
            embed.set_thumbnail(url="images/poe_logo.png")
            embed.set_footer(text="Alle Werte werden anhand der aktuellen poe.ninja Preise berechnet.")
            embeds.append(embed)
            current_chunk_number += 1

            current_chunk = chunk + "\n"

    if current_chunk:
        embed = discord.Embed(title=title,
                              description=current_chunk[:-1],
                              color=discord.Color.blue(),
                              url="https://poe.ninja/"
                              )
        embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/en/0/08/Path_of_Exile_Logo.png?20171206230851")
        embed.set_footer(text="Alle Werte werden anhand der aktuellen poe.ninja Preise berechnet.")
        embeds.append(embed)
        current_chunk_number += 1
    return embeds


def calculate_embeds_length(embeds):
    total_length = 0
    for embed in embeds:
        # Calculate length based on your object's attributes or any relevant criteria
        # For example, if your object has a 'length' attribute:
        total_length += len(embed)
    return total_length


async def send_response(embeds, ctx):
    await ctx.response.send_message(embeds=embeds)


async def send_followup(embeds, ctx):
    await ctx.followup.send(embeds=embeds)


async def div_embed(ctx, **kwargs):
    card_data = calculations.calculate_divination_card_difference(**kwargs)

    for key, value in kwargs.items():
        embeds = process_chunks(card_data, ctx, max_string_length, key)

    total_length = calculate_embeds_length(embeds)
    if total_length <= 5999:
        # If total length is smaller than or equal to 5999, execute the function directly
        await send_response(embeds, ctx)
    else:
        # Split the embeds list into chunks of size <= 5999
        chunk_size = 0
        current_chunk = []
        for embed in embeds:
            current_length = calculate_embeds_length([embed])
            if chunk_size + current_length > 5999:
                await send_response(current_chunk, ctx)
                chunk_size = 0
                current_chunk = []
            current_chunk.append(embed)
            chunk_size += current_length
        if current_chunk:
            await send_followup(current_chunk, ctx)
