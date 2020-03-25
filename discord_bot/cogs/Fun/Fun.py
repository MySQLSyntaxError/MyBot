import discord
from discord.ext import commands
import random
from random import randint

EMBEDCOLOR = 0x15f906
eightball = ["Ja", "Nein", "Vielleicht", "Sehr wahrscheinlich", "Sehr unwahrscheinlich", "Bestimmt"]
flip = ["Zahl", "Kopf"]
ssp = ["Schere", "Stein", "Papier"]

class Fun(commands.Cog, name="Fun"):

    def __init__(self, bot):
        self.bot: discord.Client = bot

    @commands.command(name="eightball", aliases=["8ball"])
    async def eightball(self, ctx,*,Frage):
        embed = discord.Embed(title=f"8ball", color=EMBEDCOLOR)
        embed.set_author(name=ctx.author.name, icon_url=f"{ctx.author.avatar_url}")
        embed.add_field(name=f"Deine Frage: {Frage}", value=f"Antwort: {random.choice(eightball)}")
        await ctx.send(embed=embed)

    @commands.command()
    async def flip(self, ctx,):
        embed = discord.Embed(title=f"{random.choice(flip)}", color=EMBEDCOLOR)
        embed.set_author(name=ctx.author.name, icon_url=f"{ctx.author.avatar_url}")
        await ctx.send(embed=embed)

    @commands.command()
    async def roll(self, ctx, number:int):
        x = randint(1,6)
        if x == number:
            embed = discord.Embed(title=None,description=f"Du hast gewonnen!\r\nDu hast eine {number} gewählt und der Bot hat eine {x} gewürfelt.",color=EMBEDCOLOR)
            embed.set_author(name=ctx.author.name, icon_url=f"{ctx.author.avatar_url}")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=None,description=f"Du hast verloren...\r\nDu hast eine {number} gewählt und der Bot hat eine {x} gewürfelt.",color=EMBEDCOLOR)
            embed.set_author(name=ctx.author.name, icon_url=f"{ctx.author.avatar_url}")
            await ctx.channel.send(embed=embed)

    @commands.command()
    async def ssp(self, ctx, Wahl: str):
        Bot = random.choice(ssp)
        if Bot == "Schere" and Wahl == "Papier":
            antwort = "Du hast verloren..."
        if Bot == "Schere" and Wahl == "Stein":
            antwort = "Du hast gewonnen!"
        if Bot == "Schere" and Wahl == "Schere":
            antwort = "Ihr habt unentschieden gespielt."

        if Bot == "Stein" and Wahl == "Papier":
            antwort = "Du hast gewonnen!"
        if Bot == "Stein" and Wahl == "Stein":
            antwort = "Ihr habt unentschieden gespielt."
        if Bot == "Stein" and Wahl == "Schere":
            antwort = "Du hast verloren..."

        if Bot == "Papier" and Wahl == "Papier":
            antwort = "Ihr habt unentschieden gespielt."
        if Bot == "Papier" and Wahl == "Stein":
            antwort = "Du hast verloren..."
        if Bot == "Papier" and Wahl == "Schere":
            antwort = "Du hast gewonnen!"

        embed = discord.Embed(title="Schere Stein Papier", color=EMBEDCOLOR, inline=False)
        embed.add_field(name=f"{antwort}", value=f"Du hast {Wahl} und der Bot {Bot} genommen!", inline=False)
        embed.set_author(name=ctx.author.name, icon_url=f"{ctx.author.avatar_url}")
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Fun(client))
    print("Fun wurde geladen.")