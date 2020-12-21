from resources.structures.Bloxlink import Bloxlink # pylint: disable=import-error
from resources.constants import ARROW, LIMITS, INVISIBLE_COLOR, EMBED_COLOR # pylint: disable=import-error
from discord import Embed


@Bloxlink.command
class SessionCommand(Bloxlink.Module):
    """announces a session"""

    def __init__(self):
        self.permissions = Bloxlink.Permissions().build("BLOXLINK_MODERATOR")
        self.aliases = ["training"]
        self.dm_allowed = False
        self.category = "Miscellaneous"
        self.free_to_use = True
        self.arguments = [
            {
                "prompt": "What is the name of this session?",
                "name": "title",
                "embed_title": "Session Name",
                "embed_color": INVISIBLE_COLOR
            },
            {
                "prompt": "What is the description of this session?",
                "name": "description",
                "embed_title": "Session Description",
                "embed_color": INVISIBLE_COLOR
            },
            {
                "prompt": "Who is hosting this session?",
                "name": "host",
                "embed_title": "Session Host",
                "embed_color": INVISIBLE_COLOR
            },
            {
                "prompt": "Who is co-hosting this session?",
                "name": "co_host",
                "embed_title": "Session Co-Host",
                "embed_color": INVISIBLE_COLOR,
                "footer": "Say **skip** if there isn't a co-host.",
                "exceptions": ["skip"]
            },
            {
                "prompt": "When is the session?",
                "name": "dateAndTime",
                "embed_title": "Session Date & Time",
                "embed_color": INVISIBLE_COLOR
            },
            {
                "prompt": "What channel should this session be posted in?",
                "name": "channel",
                "embed_title": "Session Channel",
                "embed_color": INVISIBLE_COLOR,
                "type": "channel"
            }
        ]

    @Bloxlink.flags
    async def __main__(self, CommandArgs):
        response = CommandArgs.response
        prefix = CommandArgs.prefix

        title = CommandArgs.parsed_args["title"]
        description = CommandArgs.parsed_args["description"]
        host = CommandArgs.parsed_args["host"]
        co_host = CommandArgs.parsed_args["co_host"]
        date_and_time = CommandArgs.parsed_args["dateAndTime"]
        channel = CommandArgs.parsed_args["channel"]

        embed = Embed(title=f"{title}")
        embed.description = f"{description}"

        embed.add_field(name="Date & Time", value=f"{date_and_time}", inline=False)

        embed.add_field(name="Host", value=f"{host}", inline=True)
        if co_host != "skip":
            embed.add_field(name="Co-Host", value=f"{co_host}", inline=True)

        embed.set_footer(text="Powered by Bloxlink", icon_url=Bloxlink.user.avatar_url)
        embed.colour = EMBED_COLOR

        await response.success(f"Your session has been posted in <#{channel.id}>!")
        await channel.send(embed=embed)


class SessionAddon:
    """provides commands for posting sessions"""

    def __init__(self):
        self.commands = [SessionCommand]

    def load_commands(self):
        return self.commands

    def __str__(self):
        return f"**{self.__class__.__name__.replace('Addon', '').lower()}** {ARROW} {self.__doc__}"
