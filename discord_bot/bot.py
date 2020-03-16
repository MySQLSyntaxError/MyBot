import discord
import os
from discord.ext import commands
import asyncio
import datetime
import sqlite3
import json


async def get_prefix(bot, message):
    async with open('prefixes.json', 'r') as f:
        data = json.load(f)

    if data[str(message.guild.id)] is not None:
        return data[str(message.guild.id)]
    else:
        return '!'


bot = commands.Bot(command_prefix=get_prefix, case_insensitive=True)
bot.remove_command('help')


@bot.event
async def on_ready():
    print("Logged in as User: " + bot.user.name)
    bot.load_extension('cogs.custom_command_handler.commands.CreateCustomCommand')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"on {len(bot.guilds)} Servers"))


@bot.event 
async def on_guild_join(guild):
    async with open('prefixes.json', 'r') as f:
        data = json.load(f)

    new_data = {
        str(guild.id): "!"
    }

    data.update(new_data)

    async with open('prefixes.json', 'w') as f:
        json.dump(data, f)


@bot.event 
async def on_guild_remove(guild):
    async with open('prefixes.json', 'r') as f:
        data = json.load(f)

    del data[str(guild.id)]

    async with open('prefixes.json', 'w') as f:
        json.dump(data, f)
        

bot.run('')
