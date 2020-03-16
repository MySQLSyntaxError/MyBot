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
        await ctx.message.delete()

        GUILD_PREFIX = get_prefix(self.bot, ctx.mesage)

        embed = discord.Embed(color=self.bot.user.color, title=f"Custom Commands Help", description="Reagiere mit den Pfeilen\n\n"
                                                                                                     "`Seite 1/`")

        max_pages = 3

        current_page = 1

        message = await ctx.send(embed=embed)

        to_react = ["⏪", "⏩", "❌"]

        for react in to_react:
            await message.add_reaction(react)

        def check_react(reaction, user):
            if reaction.message_id != message.id:
                return False
            if user != ctx.message.author:
                return False
            if str(reaction.emoji) not in to_react:
                return False
            return True

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=900.0, check=check_react)
        except asyncio.TimeoutError:
            await message.clear_reactions()

            embed = discord.Embed(color=self.bot.user.color, title="Custom Commands Hilfe abgelaufen")
            embed.timestamp = datetime.datetime.utcnow()

            await message.edit(embed=embed)
        if user != ctx.message.author:
            pass
        elif '⏪' in str(reaction.emoji):
            if current_page == 1:
                current_page = max_pages
                embed = discord.Embed(color=self.bot.user.color, title=f"Custom Commands Hilfe Seite `{current_page}/{max_pages}`",
                                       description=f"```\n"
                                                   f"- {GUILD_PREFIX}custom embed <NAME> <TRUE|FALSE> | "
                                                   f"\"TRUE\" aktiviert das Embed, \"FALSE\" deaktiviert das Embed!\n"
                                                   f"- {GUILD_PREFIX}custom embed <NAME> title <TITEL...> | "
                                                   f"Setzt den Embed Title, \"none\" für keinen Title!\n"
                                                   f"- {GUILD_PREFIX}custom embed <NAME> desc <DESC...> | "
                                                   f"Setzt die Embed Description, \"none\" für keine Description!\n"
                                                   f"- {GUILD_PREFIX}custom embed <NAME> timestamp <TRUE|FALSE> | "
                                                   f"\"TRUE\" lässt im Footer des Embeds die Uhrzeit anzeigen, \"FALSE\" deaktiviert dies!\n"
                                                   f"- {GUILD_PREFIX}custom embed <NAME> thumbnail <TRUE|FALSE> | \"TRUE\" aktiviert "
                                                   f"das Thumbnail bei dem Embed, \"FALSE\" deaktiviert es!```")
                embed.timestamp = datetime.datetime.utcnow()

                await message.edit(embed=embed)
            elif current_page == max_pages:
                current_page = 1

                embed = discord.Embed(color=self.bot.user.color, title=f"Custom Commands Hilfe Seite `{current_page}/{max_pages}`",
                                       description=f"Das ist die Hilfe von den Custom Commands, durch reagieren mit unteren Reaktionen,"
                                                   f"kannst du die Seiten ändern. \nFalls du fertig bist, kannst du auf das ❌ Emote reagieren.\n"
                                                   f"Damit stoppst du die Hilfe, ansonsten kannst du auch 15 Minuten warten, dann wird die Hilfe automatisch ungültig.")
                embed.timestamp = datetime.datetime.utcnow()

                await message.edit(embed=embed)

            else:
                current_page += 1

                if current_page == 2:
                    embed = discord.Embed(color=self.bot.user.color, title=f"Custom Commands Hilfe Seite `{current_page}/{max_pages}`",
                                           description=f"```\n"
                                                       f"- {GUILD_PREFIX}custom list | Zeigt alle Custom "
                                                       f"Commands an!\n"
                                                       f"- {GUILD_PREFIX}custom create <NAME> <PARAMETER...> |"
                                                       f"Erstellt einen Custom Command und leitet den User "
                                                       f"zu dem Setup weiter!\n"
                                                       f"- {GUILD_PREFIX}custom set <NAME> response <ANTWORT...> | "
                                                       f"Setzt die Antwort des Commands neu!\n"
                                                       f"- {GUILD_PREFIX}custom add <NAME> parameter <PARAMETER...> | "
                                                       f"Fügt mehr Paramater hinzu!\n"
                                                       f"- {GUILD_PREFIX}custom remove <NAME> parameter <PARAMETER...> | "
                                                       f"Entfernt Parameter!```")
                    embed.timestamp = datetime.datetime.utcnow()

                    await message.edit(embed=embed)

        #embed = discord.Embed(color=self.bot.user.color, title=f"Custom Commands", description=f"```\n"
        #                                                                                       f"- {GUILD_PREFIX}list | Zeigt alle Custom "
        #                                                                                       f"Commands an!\n"
        #                                                                                       f"- {GUILD_PREFIX}create <NAME> <PARAMETER...> |"
        #                                                                                       f"Erstellt einen Custom Command und leitet den User "
        #                                                                                       f"zu dem Setup weiter!\n"
        #                                                                                       f"- {GUILD_PREFIX}set <NAME> response <ANTWORT...> | "
        #                                                                                       f"Setzt die Antwort des Commands neu!\n"
        #                                                                                       f"- {GUILD_PREFIX}add <NAME> parameter <PARAMETER...> | "
        #                                                                                       f"Fügt mehr Paramater hinzu!\n"
        #                                                                                       f"- {GUILD_PREFIX}remove <NAME> parameter <PARAMETER...> | "
        #                                                                                       f"Entfernt Parameter!\n"
        #                                                                                       f"- {GUILD_PREFIX}embed <NAME> <TRUE|FALSE> | "
        #                                                                                       f"\"TRUE\" aktiviert das Embed, \"FALSE\" deaktiviert das Embed!\n"
        #                                                                                       f"- {GUILD_PREFIX}embed <NAME> title <TITEL...> | "
        #                                                                                       f"Setzt den Embed Title, \"none\" für keinen Title!\n"
        #                                                                                       f"- {GUILD_PREFIX}embed <NAME> desc <DESC...> | "
        #                                                                                       f"Setzt die Embed Description, \"none\" für keine Description!\n"
        #                                                                                       f"- {GUILD_PREFIX}embed <NAME> timestamp <TRUE|FALSE> | "
        #                                                                                       f"\"TRUE\" lässt im Footer des Embeds die Uhrzeit anzeigen, \"FALSE\" deaktiviert dies!\n"
        #                                                                                       f"- {GUILD_PREFIX}embed <NAME> thumbnail <TRUE|FALSE> |```")


def setup(bot):
    bot.add_cog(CreateCustomCommand(bot))
    print("CreateCustomCommand loaded")
