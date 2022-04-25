import os
import discord
import random
# import the userful files birthday:
import birthday


from discord.ext import commands
from dotenv import load_dotenv
# import the actions files :
from thank_you import thanks, thank_you
from greeting import greetings, greeting
from cheer_up import sad_words, cheer_up
from happiness import happy_words, happy_for_you
from goodbye import bye_words, good_bye
from thought import small_talk
from daily_recommandation import daily_recommendation


load_dotenv()
token = os.getenv("TOKEN")  # fetch the Token in the .env file, where format is TOKEN="your_discord_token"

bot = commands.Bot(command_prefix='--')
client = discord.Client()
intents = discord.Intents.all()
intents.members = True

cogs = [music]

for i in range(len(cogs)):
    cogs[i].setup(bot)


# print if the bot is online in the Console. Will display a bot activity in your server.
@bot.event
async def on_ready():
    print("Rain is ready")
    await bot.change_presence(status=discord.Status.idle,
                              activity=discord.Game("Call me Emperor")
                              )


# Allow the users to check all the available commands
@bot.command(name="commands", description="Show the bot commands.")
async def commands(ctx):
    await ctx.send("commands list coming soon !")


@bot.command(name="welcome", description="Will display a welcome message to all new server member.")
async def welcome(ctx, member: discord.Member):
    messages = await ctx.channel.history(limit=1).flatten()
    name = member.mention
    for m in messages:
        await m.delete()
    await ctx.send(f"Welcome {name}!")


@bot.command(name="test", description="The bot will answer if its online.")
async def test(ctx):
    await ctx.send("Everything looks fine... I'm ready!")


# Error verification and warn the user about the correct way to use the command
@welcome.error
async def on_command_error(ctx, error):
    # error detection
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Ah, I'm sorry ! The --welcome command must be followed by a @username !")
        return


# Erase messages
@bot.command(name="delete", description="Allow the user to erase the last N messages in the channel")
async def delete(ctx, number_of_messages: int):
    messages = await ctx.channel.history(limit=number_of_messages + 1).flatten()

    for m in messages:
        await m.delete()
    await ctx.send("...\nOkay, all done ! I cleared the chat for you ! *huff*")


@bot.command()
async def smalltalk(ctx):
    rand = random.choice(small_talk)
    await ctx.send(rand)


@bot.command()
async def daily(ctx):
    rand = random.choice(daily_recommendation)
    await ctx.send(rand)


# Bot reactions to usual talk in chat
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.author == bot:
        return

    if any(word in message.content.lower() for word in greeting):
        await message.channel.send(random.choice(greetings))
        return

    if any(word in message.content.lower() for word in thanks):
        await message.channel.send(random.choice(thank_you))
        return

    if any(word in message.content.lower() for word in sad_words):
        await message.channel.send(random.choice(cheer_up))
        return

    if any(word in message.content.lower() for word in happy_words):
        await message.channel.send(random.choice(happy_for_you))
        return
    if any(word in message.content.lower() for word in bye_words):
        await message.channel.send(random.choice(good_bye))
        return

    await bot.process_commands(message)


print("Connecting. Please, wait a moment...")

# connection au serveur
bot.run(token)
