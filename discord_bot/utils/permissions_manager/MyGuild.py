import json

import discord
from discord.ext import commands
import asyncio
import datetime
import aiosqlite


class MyGuild:
    def __init__(self, guild):
        self.guild: discord.Guild = guild

    async def is_in_database(self):
        main = await aiosqlite.connect('main.db')
        cursor = await main.execute(f"SELECT * FROM my_guild WHERE guild_id = '{self.guild.id}'")
        result = await cursor.fetchone()
        if result is None:
            return False
        else:
            return True

    async def add_to_database(self):
        main = await aiosqlite.connect('main.db')
        cursor = await main.execute(f"INSERT INTO my_guild (guild_id, use_permissions) VALUES ('{self.guild.id}', '{True}')")
        await main.commit()
        await cursor.close()
        await main.close()

    async def get_guild(self):
        return self.guild

    async def get_guild_id(self):
        return self.guild.id

    async def get_guild_icon_url(self):
        return self.guild.icon_url

    async def get_guild_name(self):
        return self.guild.name

    async def has_permissions_activated(self):
        main = await aiosqlite.connect('main.db')
        cursor = await main.execute(f"SELECT use_permissions FROM my_guild WHERE guild_id = '{self.guild.id}'")
        result = await cursor.fetchone()
        if result is not None and int(result) == 1:
            return True
        else:
            return False

    async def get_groups(self):
        async with open(str(self.guild.id) + '.json', 'r') as f:
            data = json.load(f)

        group_list = data['groups']

        return group_list

    async def get_group_permissions(self, group: str):
        group_list = await self.get_groups()
        specified_group = group_list[group]

        group_permissions = specified_group['permissions']

        return group_permissions

    async def add_group_permission(self, group: str, permission: str):
        group_permissions = await self.get_group_permissions(group)

        async with open(str(self.guild.id) + '.json', 'r') as f:
            data = json.load(f)

        group_permissions = group_permissions + permission.lower() + '^^^'

        data['groups'][group]['permissions'] = group_permissions

        async with open(str(self.guild.id) + '.json', 'w') as f:
            json.dump(data, f)

    async def remove_group_permission(self, group: str, permission: str):
        group_permissions = await self.get_group_permissions(group)

        async with open(str(self.guild.id) + '.json', 'r') as f:
            data = json.load(f)

        group_permissions = group_permissions.replace(permission.lower() + '^^^', "")

        data['groups'][group]['permissions'] = group_permissions

        async with open(str(self.guild.id), 'w') as f:
            json.dump(data, f)

    async def group_has_permission(self, group: str, permission: str):
        return permission.lower() in self.get_group_permissions(group)

    async def remove_group(self, group: str):
        all_groups = await self.get_groups()

        del all_groups[group]

        async with open(str(self.guild.id), 'w') as f:
            json.dump(all_groups, f)

    async def add_group(self, group_name: str, inherit_group: str, *args):
        permissions = "^^^".join(args)

        all_groups = await self.get_groups()

        new_data = {
            f"{group_name}": {
                "inherits": inherit_group,
                "permissions": permissions
            }
        }

        all_groups.update(new_data)


        async with open(str(self.guild.id), 'w') as f:
            json.dump(all_groups, f)
