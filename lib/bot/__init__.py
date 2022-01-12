''' [MASTER BOT HANDLER]
This configuration will keep the bot running.
This is not a self-run, and will do nothing if started from this module.
START = [launcher.py]
COMMANDS = [wakatime <!change!> <WakaTime_Username> <WakaTime_APIKEY>]
'''
import asyncio
import os
from datetime import datetime
from glob import glob

from apscheduler.schedulers.background import BackgroundScheduler
from discord.ext.commands import BadArgument
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound, when_mentioned_or

from ..db import db

OWNER_IDS = [307867475410681857] # Add your ID if you're going to run this bot.
COGS = [path.split("\\")[-1][:-3] for path in glob("lib/cogs/*.py")]


def get_prefix(bot, message):

    prefix = db.field("SELECT Prefix FROM guilds WHERE GuildID = ?", message.guild.id)

    return when_mentioned_or(prefix)(bot, message)


class Ready(object):
    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)

    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f"{cog} cog ready")

    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])


class Bot(BotBase):
    def __init__(self):
        self.ready = False
        self.cogs_ready = Ready()
        self.guild = None
        self.scheduler = BackgroundScheduler(timezone="America/Denver") # OPTIONAL: Change to your timezone
        db.autosave(self.scheduler)
        super().__init__(
            command_prefix=get_prefix, owner_ids=OWNER_IDS, help_command=None
        )

    def setup(self):
        for cog in COGS:
            self.load_extension(f"lib.cogs.{cog}")
            print(f" {cog} cog loaded")
        print("setup complete")

    def run(self, version):
        self.VERSION = version

        print("running setup...")
        self.setup()

        with open("lib/bot/token", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()

        print("running bot...")
        super().run(self.TOKEN, reconnect=True)

    async def on_connect(self):
        print("bot connected")

    async def on_disconnect(self):
        print("bot disconnected")

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error" and "Manage Server permission" not in args[1]:
                await args[0].send(
                    f"Something went wrong. Please ensure your command was correct. If you have further issues, please message <@307867475410681857>.\n||If this issue is realted to the WakaTime command, please make sure you have your APIKEY and Username correct.||"
                ) # Modify as needed
        else:
            pass
        raise

    async def on_command_error(self, ctx, exc):
        if isinstance(exc, CommandNotFound):
            pass
        elif isinstance(exc, BadArgument):
            pass
        else:
            raise exc

    async def on_ready(self):
        if not self.ready:
            self.scheduler.start()

            while not self.cogs_ready.all_ready():
                await asyncio.sleep(0.5)

            self.ready = True
            print("bot ready")
            os.system("cls")
        else:
            print("bot reconnected")

    async def on_message(self, message):
        if not message.author.bot:
            if message.guild:
                await self.process_commands(message)
            else:

                async def wakatime(
                    args: str = None, name: str = None, api_key: str = None
                ):
                    if args == "change" and name and api_key:
                        try:
                            db.execute(
                                "INSERT INTO userDATA  (wakaTime_UID, UserID) VALUES (?, ?)",
                                name,
                                message.author.id,
                            )
                            db.execute(
                                "INSERT INTO userDATA  (LastModified, UserID) VALUES (?, ?)",
                                name,
                                str(datetime.now()),
                            )
                            db.execute(
                                "INSERT INTO userDATA  (APIKEY, UserID) VALUES (?, ?)",
                                str(api_key),
                                message.author.id,
                            )
                            db.commit()
                        except Exception as e:
                            if "UNIQUE constraint failed: userDATA.UserID" in str(e):
                                db.execute(
                                    "UPDATE userDATA SET wakaTime_UID = ? WHERE UserID = ?",
                                    name,
                                    message.author.id,
                                )
                                db.execute(
                                    "UPDATE userDATA SET LastModified = ? WHERE UserID = ?",
                                    str(datetime.now()),
                                    message.author.id,
                                )
                                db.execute(
                                    "UPDATE userDATA SET APIKEY = ? WHERE UserID = ?",
                                    api_key,
                                    message.author.id,
                                )
                                db.commit()
                            else:
                                raise

                    elif args == "change" and not name:
                        await message.channel.send(
                            "Improper usage. Please provide a proper WakaTime name."
                        )
                    elif args == "change" and name and not api_key:
                        await message.channel.send(
                            "Improper usage. Please provide a proper WakaTime APIKEY."
                        )
                    else:
                        await message.channel.send(
                            "You can only change your profile information in DMs! Please refer to one of the servers containing this bot to use that command."
                        )
                    # ARGUMENT PARSER FOR DIRECT MESSAGING.
                    """[DM MANAGER]
                    Manages all incoming DM's.
                    Default prefix = '-'
                    In DM's there is no default prefixing,\
                        so I went ahead and added a defaut PREFIX and PREFIX parser.\
                            Essentially it just removes the PREFIX, and then handles the rest.
                    Commands: {wakatime}    
                    """

                try:
                    PREFIX = "-"
                    args = (message.content).split()

                    # Prefix Handler
                    args[0] = args[0].replace("-", "")

                    # WakaTime Argument Handler
                    if args[0] == f"wakatime":
                        await wakatime(args[1], args[2], args[3])
                    # ADD COMMANDS THROUGH DMS HERE

                    # In Case Of No Commands Found
                    else:
                        await message.channel.send(
                            "Improper usage. Please provide a proper command!"
                        )
                # Simple Exception Handler - Returns Message To DM User
                except Exception as e:
                    await message.channel.send(
                        f"Improper usage. Please provide proper command formatting!"
                    )


bot = Bot()
