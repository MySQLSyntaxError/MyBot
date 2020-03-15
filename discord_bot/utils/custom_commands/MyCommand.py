import json

import discord
from discord.ext import commands
import asyncio
import datetime
import aiosqlite


class MyCommand:
    def __init__(self, guild):
        self.guild: discord.Guild = guild

    async def get_custom_commands(self):
        async with open(str(self.guild.id) + '.json', 'r') as f:
            data = json.load(f)

        return data['custom_commands']

    async def add_custom_command(self, command: str, parameter: str, *args):
        response = " ".join(args)

        all_commands = await self.get_custom_commands()

        new_data = {
            f"{command.lower()}": {
                'parameters': parameter,
                'response': response
            }
        }

        all_commands.update(new_data)

        async with open(str(self.guild.id) + '.json', 'w') as f:
            json.dump(all_commands, f)

    async def remove_custom_command(self, command: str):
        all_commands = await self.get_custom_commands()

        del all_commands[command.lower()]

        async with open(str(self.guild.id) + '.json', 'w') as f:
            json.dump(all_commands, f)

    async def custom_command_exists(self, command: str):
        return command.lower() in self.get_custom_commands()

    async def get_custom_command(self, command: str):
        return self.get_custom_commands()[command.lower()]

    async def get_custom_command_parameter(self, command: str):
        return self.get_custom_command(command.lower())['parameters']

    async def get_custom_command_response(self, command: str):
        return self.get_custom_command(command.lower())['response']

    async def add_custom_command_parameter(self, command: str, new_parameter: str):
        all_commands = await self.get_custom_commands()

        custom_command = all_commands[command.lower()]

        current_parameters = custom_command['parameters']

        current_response = await self.get_custom_command_response(command)

        new_data = {
            f"{command.lower()}": {
                "parameters": current_parameters + new_parameter.lower() + "^^^",
                "response": current_response
            }
        }

        all_commands.update(new_data)

        async with open(str(self.guild.id) + '.json', 'w') as f:
            json.dump(all_commands, f)

    async def set_custom_command_response(self, command: str, *args):
        response = " ".join(args)
        all_commands = await self.get_custom_commands()

        current_parameters = await self.get_custom_command_parameter(command)

        new_data = {
            f"{command.lower()}": {
                "parameters": current_parameters,
                "response": response
            }
        }

        all_commands.update(new_data)

        async with open(str(self.guild.id) + '.json', 'w') as f:
            json.dump(all_commands, f)

