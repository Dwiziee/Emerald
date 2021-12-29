import discord
import json
import os
from discord.ext import commands
from discord.ext.commands import Bot
from discord import Member
import random

class EconomyCommands(commands.Cog):
  def __init__(self, client):
    self.client = client
  @commands.command()
  async def start(self,ctx):
    with open("users.json", "r") as f:
        data = json.load(f)
    if str(ctx.author.id) in data:
      await ctx.reply("You already have an account.")
    else:
      data[str(ctx.author.id)] = {}
      data[str(ctx.author.id)]["Coins"] = 100
      with open("users.json","w") as f:
        json.dump(data,f, indent = 4)
      await ctx.reply("You have been added to the database.")

  @commands.command()
  async def bal(self,ctx,*balguy:discord.Member):
    if not balguy:
      balguy = ctx.message.author
    with open("users.json","r") as f:
      data = json.load(f)
    wallet_amt = data[str(balguy.id)]["Coins"]
    balembed = discord.Embed(title = f"{balguy}'s balance", color = discord.Color.blue())
    balembed.add_field(name = "Account balance", value = wallet_amt)
    await ctx.send(embed= balembed)
  
  @commands.command()
  async def beg(self, ctx):
    begresponses = ("The rock donated ", "Dwiz was happy so he gave you ", "Oh you poor beggar, take this- ", "There you go, thanks for using this bot- ")
    begearnings = random.randrange(101)
    await ctx.reply(f"{random.choice(begresponses)}{begearnings} Coins")
    with open("users.json","r") as f:
      data = json.load(f)
      data[str(ctx.author.id)]["Coins"] += begearnings
      with open("users.json","w") as f:
        json.dump(data,f)
  

  


def setup(client):
    client.add_cog(EconomyCommands(client))

