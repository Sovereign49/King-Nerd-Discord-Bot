"""
TITLE: King Nerd Bot Main File
AUTHOR: SOVEREIGN SHAHID
DATE: 2022-09-24
"""
import discord
from discord import Option, Bot, ApplicationContext, Intents, Embed
from dotenv import load_dotenv
import random
import json
import os
import datetime

load_dotenv()

# --- VARIABLES --- #

with open("yo_mama_jokes.json") as f:
    jokes = json.load(f)

with open("pickup_lines.json") as f:
    pickup_lines = json.load(f)

intents = Intents.default()
intents.message_content = True

bot = Bot(intents=intents)

mommy_enable = True
mommy_count = 0
mommy_max = 3


# --- BOT STUFF --- #


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")


@bot.listen()
async def on_message(message):
    global jokes, mommy_count, mommy_max
    if message.author == bot.user:
        return
    mom_words = ["mom", "mum", "ma ", "mama", "mother"]

    if mommy_enable:
        for mom in mom_words:
            if mom in message.content.lower():
                if mommy_count == 0:
                    await message.channel.send(jokes[random.randrange(len(jokes))])
                else:
                    pass
                mommy_count += 1
        if "ma" == message.content.lower() and mommy_count == 0:
            await message.channel.send(jokes[random.randrange(len(jokes))])

        if mommy_count >= mommy_max:
            mommy_count = 0


@bot.slash_command(
    description="Repeats What you say", )
async def echo(ctx: ApplicationContext, phrase: Option(str, "Enter Phrase")):
    await ctx.respond(f"{phrase}")


@bot.slash_command(
    description="Anonymous Confessions", )
async def confession(ctx: ApplicationContext,
                     confession: Option(str, "Enter Confession")):
    global bot
    confession_embed = Embed(title="Confession", description=confession)
    confession_channel = bot.get_channel(1044695496310132836)
    log_channel = bot.get_channel(1049512969022734437)
    log_embed = Embed(title="Confession log",
                      description=f"{ctx.user} sent the following confession")
    log_embed.add_field(name="Timestamp", value=datetime.datetime.now())
    log_embed.add_field(name="Confession", value=confession)
    await log_channel.send(embed=log_embed)
    await confession_channel.send(embed=confession_embed)
    await ctx.send_response(content="Confession was sent sucessfully",
                            ephemeral=True)


@bot.slash_command(
    description="Generates pickup lines for you so you can get bitches")
async def pickup_line_generator(ctx: ApplicationContext,
                                ping: Option(str,
                                             "Ping the person of your dreams",
                                             required=False)):
    global pickup_lines

    if not ping:
        res = f"{pickup_lines[random.randrange(len(pickup_lines))]}"
    else:
        res = f"{ping}: {pickup_lines[random.randrange(len(pickup_lines))]}"
    await ctx.send_response(res)


@bot.slash_command(
    description=
    "Command for yo mama jokes so you dont have to spam mommy every time")
async def yo_mama_generator(ctx: ApplicationContext):
    global jokes

    res = f"{jokes[random.randrange(len(jokes))]}"
    await ctx.send_response(res)


@bot.slash_command(
    description="For mods to disable yo mama jokes if the time isnt apropriate")
async def yo_mama_enable(ctx: ApplicationContext):
    global mommy_enable

    if ctx.guild.roles[-5] <= ctx.user.roles[-1]:
        if mommy_enable:
            mommy_enable = False
        else:
            mommy_enable = True
        res = f"{mommy_enable}: is what the jokes are set to"
    else:
        res = "You aren't allowed to do that"
    await ctx.send_response(content=res, ephemeral=True)


bot.run(os.getenv("BOT_TOKEN"))
