import discord
from discord.ext import commands
import asyncio
import datetime
from MyBot.discord_bot.utils.custom_commands import MyCommand
from MyBot.discord_bot.bot import get_prefix


class CreateCustomCommand(commands.Cog):
    def __init__(self, bot):
        self.bot: discord.Client = bot

    @commands.group()
    async def custom(self, ctx):
        GUILD_PREFIX = get_prefix(self.bot, ctx.mesage)

        embed = discord.Embed(color=self.bot.user.color, title=f"Custom Commands Help", description="Reagiere mit den Pfeilen")

        embed = discord.Embed(color=self.bot.user.color, title=f"Custom Commands", description=f"```\n"
                                                                                               f"- {GUILD_PREFIX}list | Zeigt alle Custom "
                                                                                               f"Commands an!\n"
                                                                                               f"- {GUILD_PREFIX}create <NAME> <PARAMETER...> |"
                                                                                               f"Erstellt einen Custom Command und leitet den User "
                                                                                               f"zu dem Setup weiter!\n"
                                                                                               f"- {GUILD_PREFIX}set <NAME> response <ANTWORT...> | "
                                                                                               f"Setzt die Antwort des Commands neu!\n"
                                                                                               f"- {GUILD_PREFIX}add <NAME> parameter <PARAMETER...> | "
                                                                                               f"Fügt mehr Paramater hinzu!\n"
                                                                                               f"- {GUILD_PREFIX}remove <NAME> parameter <PARAMETER...> | "
                                                                                               f"Entfernt Parameter!\n"
                                                                                               f"- {GUILD_PREFIX}embed <NAME> <TRUE|FALSE> | "
                                                                                               f"\"TRUE\" aktiviert das Embed, \"FALSE\" deaktiviert das Embed!\n"
                                                                                               f"- {GUILD_PREFIX}embed <NAME> title <TITEL...> | "
                                                                                               f"Setzt den Embed Title, \"none\" für keinen Title!\n"
                                                                                               f"- {GUILD_PREFIX}embed <NAME> desc <DESC...> | "
                                                                                               f"Setzt die Embed Description, \"none\" für keine Description!\n"
                                                                                               f"- {GUILD_PREFIX}embed <NAME> timestamp <TRUE|FALSE> | "
                                                                                               f"\"TRUE\" lässt im Footer des Embeds die Uhrzeit anzeigen, \"FALSE\" deaktiviert dies!\n"
                                                                                               f"- {GUILD_PREFIX}embed <NAME> thumbnail <TRUE|FALSE> |```")




def setup(bot):
    bot.add_cog(CreateCustomCommand(bot))
    print("CreateCustomCommand loaded")
