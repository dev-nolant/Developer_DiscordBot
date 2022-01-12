''' [WAKATIME COMMANDS]
Handler for the WakaTime command.
This command will gather and output coding information gathered by WAKATIME in the past \
    And then output it to Discord.
COMMANDS = [wakatime <check/NONE> \CHECK = user]
'''
from datetime import datetime

import discord
import requests
from discord.ext import commands
from discord.ext.commands import Cog

from ..db import db


async def wakatimestats(ctx, name: str = None):
    if name is None:
        wakaTime_UID = db.field(
            "SELECT wakaTime_UID FROM userDATA WHERE UserID = ?",
            int(ctx.message.author.id),
        )
        waka_key = db.field(
            "SELECT APIKEY FROM userDATA WHERE UserID = ?",
            int(ctx.message.author.id),
        )
        await ctx.message.delete()
        await ctx.send(
            f"Please please wait! Gathering the WakaTime statistics for you :)",
            delete_after=0,
        )
        try:
            data = requests.get(
                f"https://wakatime.com/api/v1/users/{wakaTime_UID}?api_key={waka_key}"
            ).json()
            # print(data)
            bio = data["data"]["bio"]
            id = data["data"]["id"]
            website = data["data"]["human_readable_website"]
            profile_url = data["data"]["profile_url"]

            data = requests.get(
                f"https://wakatime.com/api/v1/users/{wakaTime_UID}/stats/last_7_days?api_key={waka_key}"
            ).json()
            total_time_week = data["data"]["categories"][0]["text"]
            data = requests.get(
                f"https://wakatime.com/api/v1/users/{wakaTime_UID}/all_time_since_today?api_key={waka_key}"
            ).json()

            total_time = data["data"]["text"]
            time = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
            embed = discord.Embed(
                title=f"{wakaTime_UID}'s WakaTime Statistics",
                url=f"{profile_url}",
                description=f"Generated WakaTime statistics for {wakaTime_UID}",
                color=0x06D5FE,
            )
            embed.set_author(
                name="Mira Bot",
                url="https://github.com/dev-nolant",
                icon_url="https://image.freepik.com/free-vector/cute-corgi-dog-floating-with-doughnut-swimming-tires-cartoon-vector-icon-illustration-animal-holiday-icon-concept-isolated-premium-vector-flat-cartoon-style_138676-3513.jpg",
            )
            embed.add_field(name="Biography", value=f"{bio}", inline=False)
            embed.add_field(name="User Website",
                            value=f"{website}", inline=False)
            embed.add_field(
                name="Total Time Coded  This Week",
                value=f"{total_time_week}",
                inline=False,
            )
            embed.add_field(
                name="Total Time Coded", value=f"{total_time}", inline=False
            )
            embed.add_field(name="User ID", value=f"{id}", inline=False)
            embed.set_footer(
                text=f"Genertated at {time} for @{ctx.message.author}")
            await ctx.send(embed=embed)
        except Exception as e:
            raise e
    else:
        print("Outside")
        name = name.replace("<", "")
        name = name.replace(">", "")
        name = name.replace("@", "")
        name = name.replace("!", "")
        wakaTime_UID = db.field(
            "SELECT wakaTime_UID FROM userDATA WHERE UserID = ?", int(name)
        )
        waka_key = db.field(
            "SELECT APIKEY FROM userDATA WHERE wakaTime_UID = ?",
            str(wakaTime_UID),
        )
        if f"Your wakaTime ID is: {wakaTime_UID}." == "Your wakaTime ID is: None.":
            ctx.send("No WakaTime username has been set for them :(")
        else:
            await ctx.message.delete()
            await ctx.send(
                f"Please please wait! Gathering the Wakatime statistics for you :)",
                delete_after=3,
            )
            try:
                data = requests.get(
                    f"https://wakatime.com/api/v1/users/{wakaTime_UID}?api_key={waka_key}"
                ).json()

                bio = data["data"]["bio"]
                id = data["data"]["id"]
                website = data["data"]["human_readable_website"]
                profile_url = data["data"]["profile_url"]

                data = requests.get(
                    f"https://wakatime.com/api/v1/users/dev_nolant/stats/last_7_days?api_key={waka_key}"
                ).json()
                total_time_week = data["data"]["categories"][0]["text"]
                data = requests.get(
                    f"https://wakatime.com/api/v1/users/dev_nolant/all_time_since_today?api_key={waka_key}"
                ).json()

                total_time = data["data"]["text"]
                time = (datetime.now()).strftime("%Y-%m-%d %H:%M")
                embed = discord.Embed(
                    title=f"{wakaTime_UID}'s WakaTime Statistics",
                    url=f"{profile_url}",
                    description=f"Generated WakaTime statistics for {wakaTime_UID}",
                    color=0x06D5FE,
                )
                embed.set_author(
                    name="Mira Bot",
                    url="https://github.com/dev-nolant",
                    icon_url="https://image.freepik.com/free-vector/cute-corgi-dog-floating-with-doughnut-swimming-tires-cartoon-vector-icon-illustration-animal-holiday-icon-concept-isolated-premium-vector-flat-cartoon-style_138676-3513.jpg",
                )
                embed.add_field(name="Biography", value=f"{bio}", inline=False)
                embed.add_field(name="User Website",
                                value=f"{website}", inline=False)
                embed.add_field(
                    name="Total Time Coded  This Week",
                    value=f"{total_time_week}",
                    inline=False,
                )
                embed.add_field(
                    name="Total Time Coded", value=f"{total_time}", inline=False
                )
                embed.add_field(name="User ID", value=f"{id}", inline=False)
                embed.set_footer(
                    text=f"Genertated at {time} by @{ctx.message.author}")
                await ctx.send(embed=embed)
            except Exception as e:
                raise e


class wakaTime(commands.Cog, name="wakatime", description="Hello"):
    """Link or Grab information and assign WakaTime ID to your Discord profile!\n`change` - Change the WakaTime ID assigned to your Discord Account.\n`check` - Get stats of the WakaTime ID assigned to the Discord Account mentioned."""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(
        name="wakatime",
        help="To see data of the WakaTime ID assigned to your Discord Account.",
        hidden=True,
    )
    async def wakatime(self, ctx, args: str = None, name: str = None):
        if args == "change":
            await ctx.send("Please DM me this command to change your user and APIKEY.")
        elif args == "check":
            if name:
                name = name.replace("<", "")
                name = name.replace(">", "")
                name = name.replace("@", "")
                name = name.replace("!", "")
                wakaTime_UID = db.field(
                    "SELECT wakaTime_UID FROM userDATA WHERE UserID = ?",
                    int(name),
                )
                if (
                    f"Your wakaTime ID is: {wakaTime_UID}."
                    == "Your wakaTime ID is: None."
                ):
                    await ctx.send("No WakaTime username has been set for them :(")
                else:
                    await ctx.send(f"The WakaTime ID for <@{name}> is: {wakaTime_UID}")
            else:
                wakaTime_UID = db.field(
                    "SELECT wakaTime_UID FROM userDATA WHERE UserID = ?",
                    int(ctx.message.author.id),
                )
                if (
                    f"Your wakaTime ID is: {wakaTime_UID}."
                    == "Your wakaTime ID is: None."
                ):
                    await ctx.send("No WakaTime username has been set for you :(")
                else:
                    await ctx.send(
                        f"The WakaTime ID for <@{ctx.message.author.id}> is: {wakaTime_UID}"
                    )

        else:
            if args:
                args = args.replace("<", "")
                args = args.replace(">", "")
                args = args.replace("@", "")
                args = args.replace("!", "")
                wakaTime_UID = db.field(
                    "SELECT wakaTime_UID FROM userDATA WHERE UserID = ?",
                    int(args),
                )
                if (
                    f"Your wakaTime ID is: {wakaTime_UID}."
                    == "Your wakaTime ID is: None."
                ):
                    await ctx.send("No WakaTime username has been set for them :(")
                else:
                    await wakatimestats(ctx, args)
            else:
                wakaTime_UID = db.field(
                    "SELECT wakaTime_UID FROM userDATA WHERE UserID = ?",
                    int(ctx.message.author.id),
                )
                if (
                    f"Your wakaTime ID is: {wakaTime_UID}."
                    == "Your wakaTime ID is: None."
                ):
                    await ctx.send("No WakaTime username has been set for you :(")
                else:
                    await wakatimestats(ctx)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("wakatime")


def setup(bot):
    bot.add_cog(wakaTime(bot))
