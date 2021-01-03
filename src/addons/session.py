from resources.structures.Bloxlink import Bloxlink # pylint: disable=import-error
from resources.constants import ARROW, LIMITS, INVISIBLE_COLOR, EMBED_COLOR, RED_COLOR, YELLOW_COLOR, GREEN_COLOR # pylint: disable=import-error
from discord import Embed
from discord.errors import Forbidden, NotFound
import asyncio
from datetime import datetime, timezone

sessions = []

@Bloxlink.command
class SessionCommand(Bloxlink.Module):
    """announces a session"""

    def __init__(self):
        self.permissions = Bloxlink.Permissions().build("BLOXLINK_MODERATOR")
        self.aliases = ["training", "sessions"]
        self.arguments = [
            {
                "prompt": "Would you like to **create** a session, or "
                          "**change** the status of your current one?",
                "name": "subcommand_choice",
                "type": "choice",
                "choices": ("create", "update")
            }
        ]

    async def __main__(self, CommandArgs):
        choice = CommandArgs.parsed_args["subcommand_choice"]

        if choice == "create":
            await self.create(CommandArgs)
        elif choice == "update":
            await self.update(CommandArgs)

    async def getSession(self, message_id):
        filtered_sessions = []

        for x in sessions:
            if x["message_id"] == int(message_id):
                filtered_sessions.append(x)
        
        return filtered_sessions[0]

    @Bloxlink.subcommand()
    async def create(self, CommandArgs):
        parsed_args = await CommandArgs.prompt([
            {
                "prompt": "What is the name of this session?",
                "name": "title",
                "embed_title": "Session Name"
            },
            {
                "prompt": "What is the description of this session?",
                "name": "description",
                "embed_title": "Session Description"
            },
            {
                "prompt": "Who is hosting this session?",
                "name": "host",
                "type": "user",
                "embed_title": "Session Host",
                "footer": "Say **me** if you are the host of the session.",
                "exceptions": ["me"]
            },
            {
                "prompt": "Who is co-hosting this session?",
                "name": "co_host",
                "embed_title": "Session Co-Host",
                "type": "user",
                "footer": "Say **skip** if there isn't a co-host, or **me** if you are the co-host of the session.",
                "exceptions": ["skip"]
            },
            {
                "prompt": "When is the session?",
                "name": "dateAndTime",
                "embed_title": "Session Date & Time"
            },
            {
                "prompt": "What channel should this session be posted in?",
                "name": "channel",
                "embed_title": "Session Channel",
                "type": "channel"
            }
        ])

        response = CommandArgs.response
        title = parsed_args["title"]
        description = parsed_args["description"]
        host = parsed_args["host"]
        co_host = parsed_args["co_host"]
        date_and_time = parsed_args["dateAndTime"]
        channel = parsed_args["channel"]

        embed = Embed(title=title)
        embed.description = description

        embed.add_field(name="Date & Time", value=date_and_time, inline=False)

        if host == "me":
            embed.add_field(name="Host", value=f"<@{CommandArgs.message.author.id}>", inline=True)
        else:
            embed.add_field(name="Host", value=f"<@{host.id}>", inline=True)

        if co_host == "me":
            embed.add_field(name="Co-Host", value=f"<@{CommandArgs.message.author.id}>", inline=True)
        elif co_host != "skip" and co_host != "me":
            embed.add_field(name="Co-Host", value=f"<@{co_host.id}>", inline=True)

        embed.set_footer(text="Powered by Bloxlink", icon_url=Bloxlink.user.avatar_url)
        embed.colour = GREEN_COLOR

        await response.success(f"Your session has been posted in <#{channel.id}>!")
        try:
            message = await channel.send(embed=embed)
        except (Forbidden, NotFound):
            return await response.error("Failed to send a message to the specified channel.")
            pass
        else:
            embed.description = description
            embed.set_footer(text=f"ID: {message.id} • Powered by Bloxlink", icon_url=Bloxlink.user.avatar_url)
            try:
                await message.edit(embed=embed)
            except (Forbidden, NotFound):
                return await response.error("Failed to edit the session message.")
            else:
                sessions.append({
                    "title": embed.title,
                    "guild_id": CommandArgs.message.guild.id,
                    "channel_id": channel.id,
                    "host": host,
                    "co_host": co_host,
                    "embed": embed,
                    "message": message,
                    "message_id": message.id,
                    "status": "upcoming"
                })


    @Bloxlink.subcommand()
    async def update(self, CommandArgs):
        parsed_args = await CommandArgs.prompt([
            {
                "prompt": "What is the ID in the footer of the session?",
                "name": "message_id",
                "embed_title": "Session ID"
            },
            {
                "prompt": "Would you like to mark the session as **in progress**, or "
                          "**ended**?",
                "name": "status_choice",
                "type": "choice",
                "choices": ("in progress", "ended")
            }
        ])

        response = CommandArgs.response
        message_id = parsed_args["message_id"]
        status_choice = parsed_args["status_choice"]

        try:
            session = await self.getSession(message_id)
        except IndexError:
            return await response.error("The provided Session ID does not belong to any sessions or is already ended.")
        else:
            sessionIndex = sessions.index(session)

            if session["host"] != "me" and CommandArgs.message.author.id != session["host"].id:
                return await response.error("Only the session host or co-host can edit this session.")
            if session["co_host"] != "me" and session["co_host"] != "skip" and CommandArgs.message.author.id != session["co_host"].id:
                return await response.error("Only the session host or co-host can edit this session.")

            embed = session["embed"]
            if status_choice == "in progress":
                if session["status"] != "in progress":
                    embed.title = "``[In Progress]`` {sessionTitle}".format(sessionTitle=session["title"])
                    embed.colour = YELLOW_COLOR
                    try:
                        await session["message"].edit(embed=embed)
                    except (Forbidden, NotFound):
                        return await response.error("Failed to edit the session message.")
                    else:
                        sessions[sessionIndex]["status"] = "in progress"
                        session["embed"] = embed
                        await response.success("Successfully updated the session!")
                else:
                    await response.error("The provided session has already been marked as in progress!")
            elif status_choice == "ended":
                embed.title = "``[Ended]`` {sessionTitle}".format(sessionTitle=session["title"])
                embed.colour = RED_COLOR
                try:
                    await session["message"].edit(embed=embed)
                except (Forbidden, NotFound):
                    return await response.error("Failed to edit the session message.")
                else:
                    sessions.pop(sessionIndex)
                    await response.success("Successfully updated the session!")
