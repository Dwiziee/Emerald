import os
import discord
import random
import json
botToken = os.environ['TOKEN2']
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
from Music import MusicCommands
from AdminCommands import AdminCommands
from FunCommands import FunCommands
from HelpfulCommands import HelpfulCommands
from EconomyCommands import EconomyCommands
import aiohttp
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions


intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="=")

responses = ('gday', 'sup', 'yoo', 'wasgud')
swears = ('dwiz sucks')
warnings = ('shut up', 'no')
deaths = ('farted too hard', 'fell from a tree',
          'ate a lot of cheese and died', 'got shot by the police',
          'forgot to breathe', 'watched tiktok and died to cringe','poked a stick at a grizzly bear, which then becomes angry and eats his head off.')


@bot.event
async def on_ready():
	print('we have logged in as {0.user}'.format(bot))
	await bot.change_presence(activity=discord.Activity(
	    type=discord.ActivityType.watching, name="Your Messages"))


@bot.event
async def on_message(message):
	if message.author == bot.user:
		return

	if message.content.startswith(swears):
		await message.channel.send(random.choice(warnings))

	if message.content.startswith('=anda cracked'):
		await message.channel.send('ya da he cracked so saad ')

	if message.content.startswith('=should i take medicine'):
		await message.channel.send('ya go take your dhavai or you will die')
	if message.content.startswith('=tell me my marks'):
		await message.channel.send(
		    'okay this is the link to your marks https://www.thisworldthesedays.com/marksdotcom.html'
		)
@bot.command(name="kill", help= "Kills the mentioned user duh",pass_context=True)
async def kill(ctx, user):
	await ctx.send(f"{user} {random.choice(deaths)}")
	await bot.commands(kill)


@bot.command(name="nick", help= "Changes your server nickname to something you provide")
async def nick(ctx, nickn):
  await ctx.author.edit(nick=nickn)
  await ctx.send(f"Nickname changed to {nickn}")


@bot.command(help="idk just test it out :/")
async def ping(ctx):
	await ctx.channel.send("pong")

@bot.command(help="Simple game of rock paper scissors.")
async def rps(ctx):
	rpsGame = ['rock', 'paper', 'scissors']
	await ctx.send(f"Rock, paper, or scissors? Choose wisely...")

	def check(msg):
		return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower(
		) in rpsGame

	user_choice = (await bot.wait_for('message', check=check)).content

	comp_choice = random.choice(rpsGame)
	if user_choice == 'rock':
		if comp_choice == 'rock':
			await ctx.send(
			    f'Well, that was weird. We tied.\nYour choice: {user_choice}\nMy choice: {comp_choice}'
			)
		elif comp_choice == 'paper':
			await ctx.send(
			    f'Nice try, but I won that time!!\nYour choice: {user_choice}\nMy choice: {comp_choice}'
			)
		elif comp_choice == 'scissors':
			await ctx.send(
			    f"Aw, you beat me. It won't happen again!\nYour choice: {user_choice}\nMy choice: {comp_choice}"
			)

	elif user_choice == 'paper':
		if comp_choice == 'rock':
			await ctx.send(
			    f'Dude you are hacking how did you win that? \nYour choice: {user_choice}\nMy choice: {comp_choice}'
			)
		elif comp_choice == 'paper':
			await ctx.send(
			    f'Oh, wacky. We just tied. I call a rematch!!\nYour choice: {user_choice}\nMy choice: {comp_choice}'
			)
		elif comp_choice == 'scissors':
			await ctx.send(
			    f"get rekt i beat you lol \n Your choice: {user_choice}\nMy choice: {comp_choice}"
			)

	elif user_choice == 'scissors':
		if comp_choice == 'rock':
			await ctx.send(
			    f'HAHA!! I JUST CRUSHED YOU!! I rock!!\nYour choice: {user_choice}\nMy choice: {comp_choice}'
			)
		elif comp_choice == 'paper':
			await ctx.send(
			    f'Bruh. >: |\nYour choice: {user_choice}\nMy choice: {comp_choice}'
			)
		elif comp_choice == 'scissors':
			await ctx.send(
			    f"Oh well, we tied.\nYour choice: {user_choice}\nMy choice: {comp_choice}"
			)

@bot.command(name= "choose", help="Chooses one of two things you tell the bot.")
async def choose(ctx, arg1, arg2):
	args = arg1, arg2
	await ctx.send(f"{random.choice(args)}")


snipe_message_content = None
snipe_message_author = None
snipe_message_id = None


@bot.event
async def on_message_delete(message):

	global snipe_message_content
	global snipe_message_author
	global snipe_message_id

	snipe_message_content = message.content
	snipe_message_author = (
	    f"{message.author.name}#{message.author.discriminator}")
	snipe_message_id = message.id
	await asyncio.sleep(60)

	if message.id == snipe_message_id:
		snipe_message_author = None
		snipe_message_content = None
		snipe_message_id = None


@bot.command(name="meme",help= "MEMESS!!",pass_context=True)
async def meme(ctx):
	embed = discord.Embed(title="", description="")

	async with aiohttp.ClientSession() as cs:
		async with cs.get(
		    'https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
			res = await r.json()
			embed.set_image(url=res['data']['children'][random.randint(0, 25)]
			                ['data']['url'])
			await ctx.send(embed=embed)


@bot.command()
async def snipe(message):
	if snipe_message_content == None:
		await message.channel.send("Theres nothing to snipe.")
	else:
		embed = discord.Embed(description=f"{snipe_message_content}")
		embed.set_footer(
		    text=
		    f"Asked by {message.author.name}#{message.author.discriminator}",
		    icon_url=message.author.avatar_url)
		embed.set_author(name=f"<@{snipe_message_author}>")
		await message.channel.send(embed=embed)
		return

counter = 0
async def my_background_task():
	await bot.wait_until_ready()  # ensures cache is loaded

	channel = bot.get_channel(
	    id=871348678227558411)  # replace with target channel id
	while not bot.is_closed():
		counter = 0
		counter += 1
		await channel.send('hi')
		await asyncio.sleep(60)  # or 300 if you wish for it to be 5 minutes

@bot.command(name="setdelay",  help= "Changes the slow mode delay of a channel.", pass_context=True)
@has_permissions(manage_channels=True)
async def setdelay(ctx, seconds: int):
  await ctx.channel.edit(slowmode_delay=seconds)
  await ctx.send(f"Set the slowmode delay in this channel to {seconds} seconds!")
@has_permissions(manage_channels=False)
async def setdelay(ctx, seconds:int):
  text = "Sorry {}, you do not have permissions to do that.".format(ctx.message.author)
  await bot.send(ctx.message.channel, text)

@bot.command()
async def invite(ctx):
  await ctx.send('Use this link to invite me to any server!\n https://discord.com/api/oauth2/authorize?client_id=896989477615063100&permissions=141167689207&scope=bot')

bot.add_cog(EconomyCommands(bot))
bot.add_cog(FunCommands(bot))
bot.add_cog(HelpfulCommands(bot))
bot.add_cog(AdminCommands(bot))
bot.add_cog(MusicCommands(bot))
bot.run(os.getenv('TOKEN2'))
