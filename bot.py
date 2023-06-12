from discord.ext import commands
import discord
import os
import json
import hashlib
import requests
import time
from discord_webhook import DiscordWebhook, DiscordEmbed

from foring import color
from boosting import *
from auto import *

if os.name == 'nt':
    import ctypes

config = json.load(open("config.json", encoding="utf-8"))


def clear():  # clears the terminal
    os.system('cls' if os.name == 'nt' else 'clear')


if os.name == "nt":
    ctypes.windll.kernel32.SetConsoleTitleW(f"Boost Bot")


activity = discord.Activity(
    type=discord.ActivityType.watching, name=config["bot_status"])
bot = commands.Bot(command_prefix=">", intents=discord.Intents.all(), activity=activity)


@bot.event
async def on_ready():
    print(f"{bot.user} is online!")


@bot.slash_command(guild_ids=[config["guildID"]], name="ping", description="Check the bot's latency.")
async def ping(ctx):
    await ctx.respond(embed=discord.Embed(title="**Pong!**", description=f"{round(bot.latency * 1000)} ms", color=0x4598d2))


@bot.slash_command(guild_ids=[config["guildID"]], name="restock", description="Allows one to restock 1 month or 3 month nitro tokens.")
async def restock(ctx, code: discord.Option(str, "Paste.ee link", required=True),
                  type: discord.Option(int, "Type of tokens you are restocking, 3 months or 1 month", required=True)):
    if ctx.author.id not in config["ownerID"] and ctx.author.id not in config['adminID']:
        return await ctx.respond(
            embed=discord.Embed(title="**Missing Permission**", description="You must be an owner or an administrator to use this command!", color=0xc80000))
    if type != 1 and type != 3 and type != 0:
        return await ctx.respond(
            embed=discord.Embed(title="**Invalid Input**", description="Type can either be 3 (months), 1 (month) or empty", color=0xc80000))
    if type == 1:
        file = "input/1m_tokens.txt"
    elif type == 3:
        file = "input/3m_tokens.txt"

    code = code.replace("https://paste.ee/p/", "")
    temp_stock = requests.get(f"https://paste.ee/d/{code}",
                              headers={"User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36"}).text
    fingerprint_modification()

    f = open(file, "a", encoding="utf-8")
    f.write(f"{temp_stock}\n")
    f.close()
    lst = temp_stock.split("\n")
    return await ctx.respond(
        embed=discord.Embed(title="**Success**", description=f"Successfully added {len(lst)} tokens to {file}", color=0x4598d2))


@bot.slash_command(guild_ids=[config["guildID"]], name="addowner", description="Adds an owner.")
async def addowner(ctx, member: discord.Option(discord.Member, "Member who has add to be added as an owner.", required=True)):
    if ctx.author.id not in config["ownerID"]:
        return await ctx.respond(
            embed=discord.Embed(title
