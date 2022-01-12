''' [PREFIX COMMAND COG]
This cog's main command is '-prefix <prefix>'\
    doing so, as an administrative command, will change the prefix\
        This will only work if the user is/has "manage_guild" permissions\
            Otherwise, nothing will change.
    This is unique to your Guild, so you don't have to worry about using someone else's prefix.
COMMANDS = [prefix <prefix> {PERMISSIONS = manage_guild}]
NOTE: I do recommend that you steer clear from editing this command, as I have it lined up to work flawlessly with the DB.
'''

from discord.ext.commands import Cog, CheckFailure, command, has_permissions

from ..db import db


class Misc(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="prefix", description="Change the prefix for the given server.")
    @has_permissions(manage_guild=True)
    async def change_prefix(self, ctx, new: str = None):
        await ctx.message.delete()
        try:
            if len(new) > 5:
                await ctx.send("The prefix can not be longer than 5 chars.")
            else:

                db.execute(
                    "UPDATE guilds SET Prefix = ? WHERE GuildID = ?", new, ctx.guild.id
                )

                await ctx.send(f"Prefix set to: {new}")
        except:
            currentprefix = db.field(
                "SELECT Prefix FROM guilds WHERE GuildID = ?",
                int(ctx.guild.id),
            )
            await ctx.send(f"The prefix on this server is: {currentprefix}")

    @change_prefix.error
    async def change_prefix_error(self, ctx, exc):
        if isinstance(exc, CheckFailure):
            await ctx.send("You need the Manage Server permission to do that.")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("misc")


def setup(bot):
    bot.add_cog(Misc(bot))
