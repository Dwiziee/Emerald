import discord
from discord.ext import commands


class AdminCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f"{member} has been kicked.")
    @commands.command()
    async def mute(self, ctx, guy: discord.Member):
        muted_role = discord.utils.find(lambda r: r.name.upper() == 'MUTED', ctx.guild.roles)
        staff_role = discord.utils.find(lambda r: r.name.upper() == 'STAFF', ctx.guild.roles)
        if staff_role not in ctx.author.roles:
            return await ctx.send("Sorry. You don't have the permission for that command.")
        if muted_role:
            #if muted_role in guy:
              #await ctx.send("That person is already muted!")

            await guy.add_roles(muted_role)
            await ctx.send(f"{guy} has been muted.")
        else:
            await ctx.send("Couldn't find a role with 'muted' in the name.")
    @commands.command()
    async def unmute(self,ctx, unguy: discord.Member):
      muted_role = discord.utils.find(lambda r: r.name.upper() == 'MUTED', ctx.guild.roles)
      staff_role = discord.utils.find(lambda r: r.name.upper() == 'STAFF', ctx.guild.roles)
      if staff_role not in ctx.author.roles:
          return await ctx.send("Sorry. You don't have the permission for that command.")
      if muted_role:
        #if muted_role not in unguy:
          #await ctx.send("That person is not muted.")
        await unguy.remove_roles(muted_role)
        await ctx.send(f"{unguy} has been unmuted.")


def setup(client):
    client.add_cog(AdminCommands(client))