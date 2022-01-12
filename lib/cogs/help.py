"""
!COG IS NOT WORKING! THIS EDITION OF THE COG IS NOT IN FUNCTIONAL FORMAT.
"""

import discord
import random
from discord.ext import commands
from discord.errors import Forbidden
import json
from discord.ui import Button, View

from ..db import db


class MyButton(Button):
    async def callback(self, interaction):
        label = self.label
        await Help.help(interaction, label)


async def send_embed(ctx, embed, buttons):

    try:

        view = View()

        for button_name in buttons:
            button = MyButton(
                label=button_name, style=discord.ButtonStyle.red, emoji="❔"
            )
            view.add_item(button)

        await ctx.send(embed=embed, view=view)

    except Forbidden:
        try:
            await ctx.send(
                "Hey, seems like I can't send embeds. Please check my permissions :)"
            )
        except Forbidden:
            await ctx.author.send(
                f"Hey, seems like I can't send any message in {ctx.channel.name} on {ctx.guild.name}\n"
                f"May you inform the server team about this issue? :slight_smile: ",
                embed=embed,
            )


class Help(commands.Cog):
    """
    Sends this help message
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    # @commands.bot_has_permissions(add_reactions=True,embed_links=True)
    async def help(self, ctx, *input):

        prefix = db.field(
            "SELECT Prefix FROM guilds WHERE GuildID = ?", ctx.guild.id)
        version = "0.0.4"

        owner = "307867475410681857"

        # checks if cog parameter was given
        # if not: sending all modules and commands not associated with a cog
        if not input:
            # checks if owner is on this server - used to 'tag' owner
            try:
                owner = ctx.guild.get_member(owner).mention

            except AttributeError as e:
                owner = owner

            # starting to build embed
            emb = discord.Embed(
                title="Commands and modules",
                color=discord.Color.blue(),
                description=f"Use `{prefix}help <module>` to gain more information about that module "
                f":smiley:\n",
            )

            # iterating trough cogs, gathering descriptions
            cogs_desc = ""
            buttons = []
            for cog in self.bot.cogs:
                cogs_desc = f"`{cog}` {self.bot.cogs[cog].__doc__}\n"
                buttons.append(str(cog))
            # adding 'list' of cogs to embed
            emb.add_field(name="Modules", value=cogs_desc, inline=True)

            # integrating trough uncategorized commands
            commands_desc = ""
            for command in self.bot.walk_commands():
                # if cog not in a cog
                # listing command if cog name is None and command isn't hidden
                if not command.cog_name and not command.hidden:
                    commands_desc = f"{command.name} - {command.help}\n"

            # adding those commands to embed
            if commands_desc:
                emb.add_field(
                    name="Not belonging to a module", value=commands_desc, inline=False
                )

            # setting information about author
            emb.add_field(
                name="About",
                value=f"The Bots is developed by downbadman#0069, based on discord.py.\n\
                                    This version of it is maintained by {owner}",
                inline=False,
            )
            emb.set_footer(text=f"Bot is running {version}")

        # block called when one cog-name is given
        # trying to find matching cog and it's commands
        elif len(input) == 1:

            # iterating trough cogs
            for cog in self.bot.cogs:
                # check if cog is the matching one
                if cog.lower() == input[0].lower():

                    # making title - getting description from doc-string below class
                    emb = discord.Embed(
                        title=f"{cog} - Commands",
                        description=self.bot.cogs[cog].__doc__,
                        color=discord.Color.green(),
                    )

                    # getting commands from cog
                    for command in self.bot.get_cog(cog).get_commands():
                        # if cog is not hidden
                        if not command.hidden:
                            emb.add_field(
                                name=f"`{command.name}`",
                                value=command.help,
                                inline=True,
                            )
                    # found cog - breaking loop
                    break

            # if input not found
            # yes, for-loops have an else statement, it's called when no 'break' was issued
            else:
                emb = discord.Embed(
                    title="What's that?!",
                    description=f"I've never heard from a module called `{input[0]}` before :scream:",
                    color=discord.Color.orange(),
                )

        # too many cogs requested - only one at a time allowed
        elif len(input) > 1:
            emb = discord.Embed(
                title="That's too much.",
                description="Please request only one module at once :sweat_smile:",
                color=discord.Color.orange(),
            )

        else:
            emb = discord.Embed(
                title="It's a magical place.",
                description="I don't know how you got here. But I didn't see this coming at all.\n"
                "Would you please be so kind to report that issue to me on github?\n"
                "https://github.com/nonchris/discord-fury/issues\n"
                "Thank you! ~Nolan",
                color=discord.Color.red(),
            )

        # sending reply embed using our own function defined above
        await send_embed(ctx, emb, buttons)


def setup(bot):
    bot.add_cog(Help(bot))
