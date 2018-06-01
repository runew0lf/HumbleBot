import config
import feedparser
import yaml
import asyncio
from discord.ext import commands
from .utils import checks


class Humble:
    def __init__(self, client):
        self.client = client
        client.loop.create_task(self.tick())

    async def check(self):
        if config.RSSYAML is None:
            config.RSSYAML = {}
            return
        for server in config.RSSYAML:
            if self.client.get_channel(config.RSSYAML[server]['DISCORD_ALERT_CHANNEL']) is not None:
                d = await self.client.loop.run_in_executor(None, feedparser.parse, "http://blog.humblebundle.com/rss")
                if len(d.entries) != 0:
                    if config.RSSYAML[server]['ENTRY_ID'] != d.entries[0]['id']:
                        config.RSSYAML[server]['ENTRY_ID'] = d.entries[0]['id']
                        rss_text = f"▫️{d.entries[0]['title']} - \n" \
                                   f"{d.entries[0]['link']}"
                        await self.client.get_channel(config.RSSYAML[server]['DISCORD_ALERT_CHANNEL']).send(rss_text)
                        with open("rss.yml", 'w') as file_rss:
                            yaml.dump(config.RSSYAML, file_rss, default_flow_style=False)

    async def tick(self):
        await self.client.wait_until_ready()
        while not self.client.is_closed():
            await self.check()
            await asyncio.sleep(120)

    @commands.command(name='humblehere')
    @checks.is_admin()
    async def humble_here(self, ctx):
        """
        Selects the current channel to receive humble bundle updates
        """
        newrss = {'DISCORD_ALERT_CHANNEL': ctx.message.channel.id, 'ENTRY_ID': ''}
        config.RSSYAML[ctx.guild.id] = newrss
        await ctx.send("You will now receive humble notifications here!")
        with open("rss.yml", 'w') as file_rss:
            yaml.dump(config.RSSYAML, file_rss, default_flow_style=False)
        await self.check()


def setup(client):
    client.add_cog(Humble(client))
