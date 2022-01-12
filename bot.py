import os
import discord
# permet d'appeler le ficher .env, qui contient le token au format TOKEN = "mon_token_ici"
from dotenv import load_dotenv
load_dotenv()
from discord.ext import commands
from discord.utils import get



# creation d'une instance du bot
bot = commands.Bot(command_prefix='--')

# token récupéré depuis le fichier .env
token = os.getenv("TOKEN")

#creation de regles
#--rules = rules #rules


# détecter quand le bot est prêt
## decorateur qui permet de déclencher un nouvel événement
## la fonction est asynchrone pour que les tâches ne se bloquent pas jusqu'à la fin de l'exécution des autres.
@bot.event
async def on_ready():
    print("I'm ready")
    await bot.change_presence(status=discord.Status.idle,
                              activity = discord.Game("On live"))

#creation de la commande !regles
@bot.command()
async def rules(ctx):
    await ctx.send("Rule 1 : be nice\nRule 2: be police\nRule 3: brush your teeth 3 times a day !")

#creation de la commande Bienvenue @pseudo
@bot.command()
async def welcome(ctx, member: discord.Member):
    name = member.mention
    await ctx.send(f"Welcome {name}!")

#verification erreur
@welcome.error
async def on_command_error(ctx, error):
    #detection de l'erreur
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("La commande --welcome doit être suivi de @pseudo")

# détecter quand quelqu'un ajoute un emoji sur un message
@bot.event
async def on_raw_reaction_add(payload):


    emoji = payload.emoji.name
    channel = payload.channel_id
    message = payload.message_id




    #verifier que l'emoji ajouté est "candy"
    if channel == 815604351733202994 and message == 930602661391257611 and emoji == "🍬" :
        print("OK!")



@bot.event
async def on_raw_reaction_remove(payload):

    emoji = payload.emoji.name
    channel = payload.channel_id
    message = payload.message_id


    #verifier que l'emoji ajouté est "candy"
    if channel == 815604351733202994 and message == 930602661391257611 and emoji == "🍬" :
        print("Supprimé!")


print("Lancement du bot...")





# connection au serveur
bot.run(token)

