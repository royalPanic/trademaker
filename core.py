# Import Stack

import discord
from discord.ext import commands
import jthon
from pathlib import Path
import os
from discord.ext.commands import has_permissions
from discord.utils import get
import discord.abc

class CustomHelpCommand(commands.MinimalHelpCommand): #this special class overwrites the default help command that ships with discord.py with a much better one
    async def send_pages(self):
        destination = self.get_destination()
        e = discord.Embed(color=discord.Color(0x57F287), description='')
        for page in self.paginator.pages:
            e.description += page
        await destination.send(embed=e)

# Variable Defs
help_command = commands.DefaultHelpCommand(no_category = 'Other Commands')
config = jthon.load('config')
token = str(config.get("token")) #pulls the bot token from the hidden config file
bot = commands.Bot( #the actual bot initialization arguments
    command_prefix = commands.when_mentioned_or('^'),
    description = "A simple bot designed to let users trade goods or services with others.",
    help_command = CustomHelpCommand()
)

# Function Defs
def automatic_cog_load(): #this function looks in the bot directory for the "cogs" folder, and then attempts to load all the modules within as bot cogs
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')

#Bot Events
@bot.event
async def on_ready():
    print("TradeMaker is operational!")

@bot.event
async def on_command_error(ctx, error): #this is a general catch-all event that tosses non-standard errors back to the user who used a command
    e = discord.Embed(colour=discord.Colour(0xED4245), description=f"{error}")
    await ctx.send(embed=e)

#Bot Commands (these commands are run from the core, as opposed to all the others which have their own cogs)
@commands.is_owner()
@bot.command()
async def shutdown(ctx):
    """Allows the owner of the bot to shut down the bot from within Discord."""
    e = discord.Embed(colour=discord.Colour(0x57F287), description="Command Received, Shutting down TradeMaker!")
    await ctx.send(embed=e)
    exit()

#main run code
automatic_cog_load()

bot.run(token)