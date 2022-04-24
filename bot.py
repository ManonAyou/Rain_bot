import os
import discord
import cheer_up
from thank_you import thanks, thank_you
from greeting import greetings, greeting
from cheer_up import sad_words, cheer_up
from happiness import happy_words, happy_for_you
from goodbye import bye_words, good_bye
from thought import small_talk
import daily_recommandation
import random
from discord.ext import commands

from dotenv import load_dotenv

load_dotenv()

token = os.getenv("TOKEN")  # token récupéré depuis le fichier .env, format TOKEN="mon_token_discord"

bot = commands.Bot(command_prefix='--')
client = discord.Client()
intents = discord.Intents.default()
intents.members = True


# creation de regles
# --rules = rules #rules


# détecter quand le bot est prêt
@bot.event
async def on_ready():
    print("I'm ready")
    await bot.change_presence(status=discord.Status.idle,
                              activity=discord.Game("Call me Emperor")
                              )


# creation de la commande --commands qui affiche les commandes du bot
@bot.command()
async def commands(ctx):
    await ctx.send("commands list coming soon !")


# creation de la commande Bienvenue @pseudo
@bot.command()
async def welcome(ctx, member: discord.Member):
    name = member.mention
    await ctx.send(f"Welcome {name}!")


@bot.command()
async def test(ctx):
    await ctx.send("Everything looks fine... I'm ready!")


# verification erreur
@welcome.error
async def on_command_error(ctx, error):
    # detection de l'erreur
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("La commande --welcome doit être suivi de @pseudo")
        return


# Erase messages
@bot.command(name="clear")
async def delete(ctx, number_of_messages: int):
    messages = await ctx.channel.history(limit=number_of_messages + 1).flatten()

    for m in messages:
        await m.delete()
    await ctx.send("*huff huff...*\nOkay, all done ! I cleared the chat for you !")


# Bot chat
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


print("Lancement du bot...")

# connection au serveur
bot.run(token)
