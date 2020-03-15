import json

import discord
from discord.ext import commands
import asyncio
import aiosqlite


class PermissionsUser:
    def __init__(self, member, guild):
        self.member: discord.Member = member
        self.guild: discord.Guild = guild

    async def is_in_database(self):
        main = await aiosqlite.connect('main.db')
        cursor = await main.execute(f"SELECT * FROM my_user WHERE client_id = '{self.member.id}' and guild_id = '{self.guild.id}'")
        result = cursor.fetchone()
        if result is None:
            return False
        else:
            return True

    async def add_to_database(self):
        main = await aiosqlite.connect('main.db')
        cursor = await main.execute(f"INSERT INTO my_user (guild_id, client_id) VALUES ('{self.guild.id}', '{self.member.id}'")
        await main.commit()
        await cursor.close()
        await main.close()

    async def get_member_id(self):
        return self.member.id

    async def get_member_name(self):
        return self.member.name

    async def get_guild(self):
        return self.guild

    async def get_member(self):
        return self.member

    async def get_guild_id(self):
        return self.guild.id

    async def get_guild_name(self):
        return self.guild.name

    async def get_member_avatar_url(self):
        return self.member.avatar_url

    async def get_guild_icon_url(self):
        return self.guild.icon_url

    async def get_user_permissions(self):
        async with open(str(self.guild.id) + '.json', 'r') as f:
            data = json.load(f)

        permissions_list = data["permissions"]
        user_list = permissions_list[str(self.member.id)]
        user_permissions = user_list["self_permissions"]

        return user_permissions

    async def get_user_group(self):
        async with open(str(self.guild.id) + '.json', 'r') as f:
            data = json.load(f)

        permissions_list = data["permissions"]
        user_list = permissions_list[str(self.member.id)]
        user_group = user_list["group"]

        return user_group

    async def add_user_permission(self, permission: str):
        async with open(str(self.guild.id) + '.json', 'r') as f:
            data = json.load(f)

        users_permissions = await self.get_user_permissions()

        users_permissions = users_permissions + '^^^' + permission.lower()

        data["permissions"][str(self.member.id)]["self_permissions"] = users_permissions

        async with open(str(self.guild.id) + '.json', 'w') as f:
            json.dump(data, f)



