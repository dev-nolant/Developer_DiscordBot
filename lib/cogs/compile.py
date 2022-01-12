''' [DNT]
DO NOT TOUCH.
'''
from discord.ext.commands import Cog, command
from discord.ext import commands



class compile(commands.Cog, name="compile", description="Compile help"):
    """Compile Template"""

    def __init__(self, bot):
        self.bot = bot

    @command(name="compile", description="Compile code")
    async def compile(self):
        ListOfCogs = self.bot.cogs
        print(len(ListOfCogs))
        for NameOfCog in ListOfCogs.items():
            print(NameOfCog)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("compile")


def setup(bot):
    bot.add_cog(compile(bot))
