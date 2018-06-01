import asyncio
import random
from os import listdir
from os.path import isfile, join
from os import environ

import discord
from discord.ext import commands

import config
import traceback
import discord.ext.commands.view


def get_prefix(client, message):
    """A callable Prefix for our bot. This could be edited to allow per server prefixes."""

    # Notice how you can use spaces in prefixes. Try to keep them simple though.
    if "PYCHARM_HOSTED" in environ:
        prefixes = ['?']
    else:
        prefixes = ['!']

    # Check to see if we are outside of a guild. e.g DM's etc.
    if not message.guild:
        # Only allow ? to be used in DMs
        return '!'

    # If we are in a guild, we allow for the user to mention us or use any of the prefixes in our list.
    return commands.when_mentioned_or(*prefixes)(client, message)


# Below cogs represents our folder our cogs are in. Following is the file name. So 'meme.py' in cogs, would be cogs.meme
# Think of it like a dot path import
# This is the directory all are located in.
cogs_dir = "cogs"

bot = commands.Bot(command_prefix=get_prefix, description='Serving the community')

# Here we load our extensions(cogs) that are located in the cogs directory. Any file in here attempts to load.
if __name__ == '__main__':
    for extension in [f.replace('.py', '') for f in listdir(cogs_dir) if isfile(join(cogs_dir, f))]:
        try:
            bot.load_extension(cogs_dir + "." + extension)
        except (discord.ClientException, ModuleNotFoundError):
            print(f'Failed to load extension {extension}.')
            traceback.print_exc()


async def tick():
    await bot.wait_until_ready()
    while not bot.is_closed():
        await asyncio.sleep(120)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing,
                                                            name=random.choice(config.status)))


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing,
                                                        name=random.choice(config.status)))
    print(f'Logged in as: {bot.user.name} - {bot.user.id}')
    print(f'Version: {discord.__version__}\n')


@bot.event
async def on_message(message):
    if message.author.bot:
        return
    await bot.process_commands(message)


@bot.event
async def on_message_edit(before, after):
    if after.author.bot:
        return
    await bot.process_commands(after)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Missing argument: Try {ctx.prefix}help {ctx.command}")

bot.loop.create_task(tick())
bot.run(config.BOT_TOKEN, bot=True, reconnect=True)
