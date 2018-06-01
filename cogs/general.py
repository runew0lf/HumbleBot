import config
import time
import arrow
import discord
from discord.ext import commands
import platform
import os
import psutil


EMPTY = u'\u200b'

class Other:
    """General"""

    def __init__(self, bot):
        self.bot = bot

    def botuptime(self):
        total_seconds = float(time.time() - config.BOTUPTIME)
        # Helper vars:
        MINUTE = 60
        HOUR = MINUTE * 60
        DAY = HOUR * 24

        # Get the days, hours, etc:
        days = int(total_seconds / DAY)
        hours = int((total_seconds % DAY) / HOUR)
        minutes = int((total_seconds % HOUR) / MINUTE)
        seconds = int(total_seconds % MINUTE)

        # Build up the pretty string
        # (like this: "N days, N hours, N minutes, N seconds")
        string = ""
        if days > 0:
            string += str(days) + " " + (days == 1 and "day" or "days") + ", "
        if len(string) > 0 or hours > 0:
            string += str(hours) + " " + (hours == 1 and "hour" or "hours") + ", "
        if len(string) > 0 or minutes > 0:
            string += str(minutes) + " " + (minutes == 1 and "minute" or "minutes") + ", "
        string += str(seconds) + " " + (seconds == 1 and "second" or "seconds")

        return string

    @commands.command(name='server')
    async def server(self, ctx):
        """
        Displays server info
        Usage: !server
        """
        server = ctx.guild
        embed = discord.Embed(title=server.name, description="", color=ctx.me.color)
        embed.set_thumbnail(url=server.icon_url)

        serverinfo = f"Owner: {server.owner}\n" \
                     f"Created: {arrow.get(server.created_at).humanize()}\n" \
                     f"Members: {server.member_count}\n" \
                     f"Region: {server.region}\n" \
                     f"Features: {', '.join(server.features)}"
        embed.add_field(name="Server Information", value=serverinfo)

        member_list = list(server.members)
        status_list = [member.status.value for member in member_list]

        membersinfo = (f"Online: {status_list.count('online')}\n"
                       f"Idle: {status_list.count('idle')}\n"
                       f"Dnd: {status_list.count('dnd')}\n"
                       f"Offline: {status_list.count('offline')}")

        embed.add_field(name="Channels", value=f"{len(server.channels)}", inline=True)
        embed.add_field(name="Roles", value=f"{len(server.roles)}", inline=True)
        embed.add_field(name="Members", value=membersinfo, inline=True)
        await ctx.send(embed=embed)

    @commands.command(name='info')
    async def info(self, ctx):
        """
        Displays bot information
        """
        process = psutil.Process(os.getpid())
        embed = discord.Embed(color=ctx.me.color, title=f"HumbleBot",
                              description=f"HumbleBot has been up for {self.botuptime()}")
        embed.set_thumbnail(url=ctx.me.avatar_url)
        embed.add_field(name="» Ping", value=f"{round(self.bot.latency*1000)}ms")
        embed.add_field(name="» Servers", value=format(len(self.bot.guilds), ','))
        embed.add_field(name="» Users", value=format(len(list(self.bot.get_all_members())), ','))
        embed.add_field(name="» Channels", value=format(len(list(self.bot.get_all_channels())), ','))
        embed.add_field(name="» Commands", value=str(len(self.bot.commands)))
        embed.add_field(name="» OS", value=platform.system())
        embed.add_field(name="» Python Version", value=platform.python_version())
        embed.add_field(name="» Library", value=f'Discord.py: {discord.__version__}\n')
        embed.add_field(name="» Memory Usage", value=f"{float(process.memory_info().rss) / 1024 / 1024:0.2f} MB")
        embed.add_field(name="» Developer", value="Runew0lf#0001")
        embed.add_field(name="» Links:",
                        value=f"**Invite: [Invite HumbleBot](https://discordapp.com/api/oauth2/authorize?"
                              f"client_id=451727957266923521&permissions=388160&scope=bot)**\n"
                              f"**Official Server: [Click here for support](https://discord.gg/runew0lf)**\n")

        await ctx.send(embed=embed)


# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(Other(bot))
