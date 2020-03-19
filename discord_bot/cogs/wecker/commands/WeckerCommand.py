import discord
from discord.ext import commands, tasks
from MyBot.discord_bot.utils.time_parser import parse

import random
import datetime
import asyncio
import functools
import os
import uuid
import re


async def delete_message(ctx, time: float):
    try:
        await ctx.message.delete(delay=time)
    except discord.Forbidden:
        pass
    return


class WeckerManager(commands.Cog):
    def __init__(self, bot):
        self.bot: discord.Client = bot

        self.check_reminders.start()

    def cog_unload(self):
        self.check_reminders.cancel()

    @tasks.loop(seconds=1)
    async def check_reminders(self):
        async def remove_reminder(reminder):
            self.bot.botdata["reminders"].remove(reminder)
            async with self.bot.pool.acquire() as conn:
                await conn.execute("""
                UPDATE botdata SET reminders = $1::JSON[];""", self.bot.botdata["reminders"])

        for reminder in self.bot.botdata["reminders"]:
            if datetime.datetime.utcnow() >= datetime.datetime.fromtimestamp(reminder["started_at"] + reminder["duration"]):
                try:
                    author = self.bot.get_user(reminder["author"])
                    channel = self.bot.get_channel(reminder["channel"])
                    msg = discord.utils.get(self.bot.cached_messages, id=reminder["msg"])
                    if msg is None:
                        msg = await channel.fetch_message(reminder["msg"])
                except:
                    await remove_reminder(reminder)
                    continue

                formatted_start = datetime.datetime.fromtimestamp(reminder["started_at"]).strftime("%B %-d, %Y at %X UTC")
                embed = discord.Embed(color=self.bot.user.color, title="\U0001f514 ALARM \U0001f514", description=f""
                                                                f"{author.mention}, am __{formatted_start}__ hast du den "
                                                                f"Reminder Command ausgeführt in [dieser Nachricht]({msg.jump_url}), "
                                                                f"sodass ich dich nun daran erinnern kann! \n"
                                                                f"Nun ist der Zeitpunkt gekommen, also hier erinnere ich dich: ```\n"
                                                                f"{reminder['remind_of']}```", timestamp=datetime.datetime.utcnow())
                await author.send(embed=embed)
                await remove_reminder(reminder)

    @check_reminders.before_loop
    async def before_check_reminders(self):
        await self.bot.wait_until_ready()
        await asyncio.sleep(30)

    @commands.command(aliases=["wecker", "alarm"])
    async def remind(self, ctx, time: str, *, remind_of: str=None):
        parsed_time = parse(time)
        if parsed_time is None or remind_of is None:
            raise commands.BadArgument
        if parsed_time < 300 or parsed_time > 15778800:
            await ctx.send("Die Zeit muss über 5 Minuten sein und unter 6 Monaten!", delete_after=7.0)
            return await delete_message(ctx, 7)
        if len(remind_of) > 1800:
            await ctx.send("Der Text muss unter 1800 Zeichen sein!", delete_after=6.0)
            return await delete_message(ctx, 6)

        formatted_dt = datetime.datetime.fromtimestamp(datetime.datetime.utcnow().timestamp() + parsed_time).strftime("%B %-d, %Y at %X UTC")
        await ctx.send(f"Ok {ctx.author.mention}, ich werde dich in **{time}**, am __{formatted_dt}__, für ```\n"
                       f"{remind_of}```anschreiben!")

        new_reminder = {
            "author": ctx.author.id,
            "channel": ctx.message.channel.id,
            "msg": ctx.message.id,
            "started_at": datetime.datetime.utcnow().timestamp(),
            "duration": parsed_time,
            "remind_of": remind_of
        }
        self.bot.botdata["reminders"].append(new_reminder)
        async with self.bot.pool.acquire() as conn:
            await conn.execute("""
            UPDATE botdata SET reminders = $1::JSON[];""", self.bot.botdata["reminders"])


def setup(bot):
    bot.add_cog(WeckerManager(bot))
    print("WeckerManager loaded")
