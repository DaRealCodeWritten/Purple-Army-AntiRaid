from discord.ext import commands
from discord import Embed as Em

class UserMgmt(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command(brief="Reports a user")
	async def report(self, ctx, user, *, reason):
		try:
			mc = commands.MemberConverter()
			member = await mc.convert(ctx, user)
		except Exception:
			pass
		else:
			user = member.display_name
		def check(m):
			return m.channel == ctx.channel and m.author == ctx.author
		embed = Em(title="Are you sure?",
		color=0x651FFF)
		embed.add_field(name=f"Do you wish to report '{user}' for '{reason}'?", value="Send Yes to proceed or No to cancel")
		await ctx.send(embed=embed)
		m = await self.bot.wait_for('message', check=check)
		if m.author == ctx.author and m.channel == ctx.channel:
			if m.content.lower() == "yes":
				embed = Em(title="Success!", color=0x651FFF)
				embed.add_field(name=f"Reported {user}", value="An admin will look into it when they can", inline=False)
				await ctx.send(embed=embed)
			else:
				embed = Em(title="Cancelled",
				color=0x651FFF)
				embed.add_field(name="Your report was not submitted",
					value="Try again if you believe this is an error", inline=False)
				await ctx.send(embed=embed)
	@report.error
	async def report_error(self, ctx, exc):
		if isinstance(exc, commands.errors.MissingRequiredArgument):
			error = Em(color=0x651FFF)
			error.add_field(name="An Error Occurred", value=f"Missing {exc.param.name} arg", inline=False)
			await ctx.send(embed=error)
		else:
			error = Em(color=0x651FFF)
			error.add_field(name="An unknown error occurred", value="We don't know what happened")
			error.add_field(name="Here is the error", value=exc, inline=False)
			await ctx.send(embed=error)

def setup(bot):
	bot.add_cog(UserMgmt(bot))
	print ("Cog UserMgmt online...")