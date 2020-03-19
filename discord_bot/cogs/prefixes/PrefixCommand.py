import discord
from discord.ext import commands
import asyncio
import json


class PrefixManager(commands.Cog):
    def __init__(self, bot):
        self.bot: discord.Client = bot

    @commands.command()
    async def setprefix(self, ctx, prefix):
        async with open('prefixes.json', 'r') as f:
            data = json.load(f)

        new_data = {
            f"{ctx.guild.id}": prefix
        }

        data.update(new_data)

        async with open('prefixes.json', 'w') as f:
            json.dump(data, f)

        await ctx.send(f"Du hast den Prefix auf `{prefix}` geändert!")


def setup(bot):
    bot.add_cog(PrefixManager(bot))
