import discord
from discord.ext import commands
import datetime
from datetime import timedelta
from datetime import datetime as dt

class HelpfulCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def whois(self, ctx, member: discord.Member = None):
        if not member:  # if member is no mentioned
            member = ctx.message.author  # set member as the author
        roles = [role for role in member.roles]
        embed = discord.Embed(colour=discord.Colour.orange(), timestamp=ctx.message.created_at,
                              title=str(member))
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"Requested by {ctx.author}")

        embed.add_field(name="Display Name:", value=member.display_name)
        embed.add_field(name="ID:", value=member.id)

        embed.add_field(name="Created Account On:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
        embed.add_field(name="Joined Server On:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))

        embed.add_field(name="Roles:", value="".join([role.mention for role in roles[1:]]))
        embed.add_field(name="Highest Role:", value=member.top_role.mention)
        await ctx.send(embed=embed)
    @property
    def reactions(self):
        return {
            1: '1️⃣',
            2: '2️⃣',
            3: '3️⃣',
            4: '4️⃣',
            5: '5️⃣',
            6: '6️⃣',
            7: '7️⃣',
            8: '8️⃣',
            9: '9️⃣',
            10: '🔟'
        }

    @commands.command(aliases=["suggestion", "suggest"])
    async def poll(self, ctx, *, suggestion: str):
        await ctx.message.delete()
        embed = discord.Embed(description=suggestion)
        embed.set_author(name=f"Poll by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('👍')
        await msg.add_reaction('👎')

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        user = payload.member
        if user.bot:return
        msg = await self.client.get_guild(payload.guild_id).get_channel(payload.channel_id).fetch_message(payload.message_id)
        emoji = payload.emoji
        users = []
        if msg.author.bot and("👍"and"👎")in[str(i)for i in msg.reactions]:
            for react in msg.reactions:
                if str(react)=="👍":
                    async for reactor in react.users():
                        if reactor.bot:continue
                        if reactor in users:
                            await msg.remove_reaction(emoji, user)
                            return
                        users.append(reactor)
                elif str(react)=="👎":
                    async for reactor in react.users():
                        if reactor.bot:continue
                        if reactor in users:
                            await msg.remove_reaction(emoji, user)
                            return
                    return

    @commands.command()
    async def multipoll(self, ctx, desc: str, *choices):
        await ctx.message.delete()

        if len(choices) < 2:
            ctx.command.reset_cooldown(ctx)
            if len(choices) == 1:
                return await ctx.send("Can't make a poll with only one choice")
            return await ctx.send("You have to enter two or more choices to make a poll")

        if len(choices) > 10:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send("You can't make a poll with more than 10 choices")

        embed = discord.Embed(description=f"**{desc}**\n\n" + "\n\n".join(
            f"{str(self.reactions[i])}  {choice}" for i, choice in enumerate(choices, 1)),
                              timestamp=datetime.datetime.utcnow(), color=discord.colour.Color.green())
        embed.set_footer(text=f"Poll by {str(ctx.author)}")
        msg = await ctx.send(embed=embed)
        for i in range(1, len(choices) + 1):
            await msg.add_reaction(self.reactions[i])
    @commands.command(aliases=["stats", "activity", "messages"])
    async def check(self, ctx, timeframe=7, channel: discord.TextChannel = None, *, user: discord.Member = None):
        if timeframe > 1968:
            await ctx.channel.send("Sorry. The maximum of days you can check is 1968.")
        elif timeframe <= 0:
            await ctx.channel.send("Sorry. The minimum of days you can check is one.")

        else:
            if not channel:
                channel = ctx.channel
            if not user:
                user = ctx.author

            async with ctx.channel.typing():
                msg = await ctx.channel.send('Calculating...')
                await msg.add_reaction('🔎')

                counter = 0
                async for message in channel.history(limit=5000, after=dt.today() - timedelta(days=timeframe)):
                    if message.author.id == user.id:
                        counter += 1

                await msg.remove_reaction('🔎', member=message.author)

                if counter >= 5000:
                    await msg.edit(content=f'{user} has sent over 5000 messages in the channel "{channel}" within the last {timeframe} days!')
                else:
                    await msg.edit(content=f'{user} has sent {str(counter)} messages in the channel "{channel}" within the last {timeframe} days.')
    @commands.command(aliases=["av", "pfp"])
    async def avatar(self, ctx, *, member: discord.Member = None):
        if not member:member=ctx.message.author

        message = discord.Embed(title=str(member), color=discord.Colour.green())
        message.set_image(url=member.avatar_url)

        await ctx.send(embed=message)


def setup(client):
    client.add_cog(HelpfulCommands(client))
