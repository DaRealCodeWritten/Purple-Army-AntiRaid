#pylint:disable=C0115
#pylint:disable=C0116
import discord
from discord.ext import commands
from datetime import datetime
from typing import Union
def time_predicate(time):
	minute = 60
	hour = minute * 60
	day = hour * 24
	tsecs = None
	if "m" in time:
		tsecs = int(time[0])*minute
	elif "h" in time:
		tsecs = int(time[0])*hour
	elif "d" in time:
		tsecs = int(time[0])*day
	return tsecs
def has_admin():
	async def predicate(ctx):
		adm = ctx.guild.get_role(324161991365099530)
		if adm in ctx.author.roles or ctx.author.id == 436646726204653589:
			return True
		else:
			embed = discord.Embed(title="Access Denied", color=0x651FFF)
			embed.add_field(name="You can't access that command", value="You must be an Admin to use this command", inline=False)
			await ctx.send(embed=embed)
			return False
	return commands.check(predicate)
class AntiRaid(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	@has_admin()
	@commands.command(brief="New ways to ban!")
	async def customban(self, ctx, mode=None, *, parameters: Union[str, discord.Member]=None):
		if mode is None:
			embed = discord.Embed(title="Error", color=0x651FFF)
			embed.add_field(name="Missing 'mode' arg", value="Modes: multi, joinafter", inline=False)
			await ctx.send(embed=embed)
		elif mode == "multi":
			if parameters is None:
				embed = discord.Embed(name="Error", color=0x651FFF)
				embed.add_field(name="Missing 'parameters' arg", value="Parameters should either be multiple IDs/usernames+tags or a time", inline=False)
				await ctx.send(embed=embed)
			else:
				users = parameters.split(" ")
				for u in users:
					user = ctx.guild.get_member(u)
					if user is None:
						user = await commands.MemberConverter().convert(ctx, u)
						if user is None:
							continue
						else:
							await ctx.guild.ban(user, reason="Suspected Raiding")
					else:
						await ctx.guild.ban(user, reason="Suspected Raiding")
					embed = discord.Embed(name="All done!", color=0x651FFF)
					embed.add_field(name=f"Banned {len(users)} user(s)", value="Success!")
					await ctx.send(embed=embed)
		elif mode == "joinafter":
			time = time_predicate(parameters)
			now = datetime.now()
			counter = 0
			for m in ctx.guild.members:
				print(f"Now: {now}\nThen: {m.joined_at}\nDiff (secs): {((now - m.joined_at).total_seconds())*-1}\nApplies: {((now - m.joined_at).total_seconds())<=time}\nTime: {time}")
				if ((now - m.joined_at).total_seconds()) <= time:
					try:
						await ctx.guild.ban(m, reason="Raid ban")
						counter += 1
					except:
						pass
			embed = discord.Embed(title="Success!", color=0x651FFF)
			embed.add_field(name=f"Banned {counter} users", value=f"Another raid stopped (I hope)", inline=False)
			await ctx.send(embed=embed)
					

def setup(bot):
	bot.add_cog(AntiRaid(bot))
	print ("Cog AntiRaid online...")
