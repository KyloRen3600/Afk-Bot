import json
with open("config.json") as f:
	data = json.load(f)
	TOKEN = data["DISCORD_TOKEN"]
	PREFIX = data["DISCORD_PREFIX"]
	SERVER = data["MINECRAFT_SERVER"]
	PORT = data["MINECRAFT_PORT"]
	LOGIN_COMMANDS = data["MINECRAFT_LOGIN_COMMANDS"]

import discord
from discord.ext import commands

from log import log
from connect import minecraft_connect, minecraft_disconnect

prefix = PREFIX
discord_bot = commands.Bot(command_prefix=prefix)


def build_embed(user, title,color):
	embed = discord.Embed(title="[{0}]".format(title), url="https://github.com/KyloRen3600/Afk-Bot",color=color)
	embed.set_author(name=user.name, icon_url=user.avatar_url)
	embed.set_thumbnail(url="https://raw.githubusercontent.com/KyloRen3600/Afk-Bot/master/assets/afk.jpg")
	embed.set_footer(text="Développé par KyloRen3600")
	return embed

def get_help_embed(author):
	embed = build_embed(author,  "AFK Bot", 0xffff00)
	embed.add_field(name="Aide:",value="\"{0}connect <bot>\" -> Connecter le bot\n\"{0}disconect <bot>\" -> Déconnecter le bot".format(prefix))
	return embed

def get_discord_presence():
	return "!aide", discord.Status.online


@discord_bot.command()
async def connect(ctx, username):
	result = minecraft_connect(username, SERVER, PORT, LOGIN_COMMANDS)
	if result == True:
		embed = build_embed(ctx.author, "AFK Bot", 0x00ff00)
		embed.add_field(name="[Connexion]", value="Connexion de {0} au serveur {1}:{2} en cours...".format(username, SERVER, PORT))
	else:
		embed = build_embed(ctx.author, "AFK Bot", 0xff0000)
		embed.add_field(name="[Erreur]", value="Le bot est déjà lancé.")
	await ctx.send(embed=embed)


@discord_bot.command()
async def disconnect(ctx, username):
	result = minecraft_disconnect(username)
	if result == True:
		embed = build_embed(ctx.author, "AFK Bot", 0x00ff00)
		embed.add_field(name="[Déconnexion]", value="Déconnexion de {0} en cours...".format(username))
	else:
		embed = build_embed(ctx.author, "AFK Bot", 0xff0000)
		embed.add_field(name="[Erreur]", value="Le bot n'est pas lancé.")
	await ctx.send(embed=embed)


@connect.error
async def connect_error(ctx, error):
	embed = build_embed(ctx.author, "AFK Bot", 0xff0000)
	embed.add_field(name="[Erreur]", value="Veuillez préciser un bot.")
	await ctx.send(embed=embed)\

@disconnect.error
async def disconnect_error(ctx, error):
	embed = build_embed(ctx.author, "AFK Bot", 0xff0000)
	embed.add_field(name="[Erreur]", value="Veuillez préciser un bot.")
	await ctx.send(embed=embed)

@discord_bot.command()
async def aide(ctx):
	await ctx.send(embed=get_help_embed(ctx.author))

@discord_bot.listen()
async def on_ready():
	log("INFO", "Discord Bot connected.")
	await discord_bot.change_presence(activity=discord.Streaming(name=get_discord_presence()[0], url="https://www.twitch.tv/AFK"), status=get_discord_presence()[1])

log("INFO", "AFK Bot created by KyloRen3600.")
log("INFO", "Git repo: https://github.com/KyloRen3600/Afk-Bot")
log("INFO", "Connecting to Discord Bot...")
discord_bot.run(TOKEN)
