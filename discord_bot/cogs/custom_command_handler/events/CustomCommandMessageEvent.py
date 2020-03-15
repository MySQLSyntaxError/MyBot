import discord
from discord.ext import commands
import asyncio
import datetime
from MyBot.discord_bot.utils.custom_commands import MyCommand
from MyBot.discord_bot.bot import get_prefix


class CustomCommandMessageEvent(commands.Cog):
    def __init__(self, bot):
        self.bot: discord.Client = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        GUILD_PREFIX = get_prefix(self.bot, message)

        my_command = MyCommand.MyCommand(message.guild)

        message_content_lower = message.content.lower()

        if not message_content_lower.startswith(GUILD_PREFIX):
            message_content_lower = GUILD_PREFIX + message_content_lower

        for custom_command in my_command.get_custom_commands():
            if message_content_lower == custom_command:
                command_parameters = my_command.get_custom_command_parameter(custom_command)
                command_response = my_command.get_custom_command_response(custom_command)

                await message.delete()

                await message.channel.send(command_response)


def setup(bot):
    bot.add_cog(CustomCommandMessageEvent(bot))
    print("CustomCommandMessageEvent loaded")
