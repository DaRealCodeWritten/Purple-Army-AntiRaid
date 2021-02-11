import discord
import humanize
from discord.ext import commands
from discord import Embed
from datetime import datetime
import platform
import traceback
import io
from contextlib import redirect_stdout
import textwrap
def is_dev():
	async def predicate(ctx):
		return ctx.author.id == 436646726204653589
	return commands.check(predicate)

class DevNStats(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.uptime = bot.uptime
		self._last_result = None
	
	@commands.command(brief="Shows some stats about the bot", description="Gives the user some info about the bot including uptime, OS, and more")
	async def info(self, ctx):
		up = self.uptime - datetime.now()
		huup = humanize.naturaldelta(up)
		info_emb = Embed(title="Information", color=0x651FFF)
		info_emb.add_field(name="Uptime", value=f"Bot has been up for {huup}")
		info_emb.add_field(name="Guilds i am in", value=f"I am in {len(self.bot.guilds)} guilds")
		info_emb.add_field(name="Users i can see", value=f"I can see {len(self.bot.users)} users")
		info_emb.add_field(name="OS i am on", value=f"I am running on {platform.platform()}")
		info_emb.add_field(name="Library Version", value=f"I am on Discord.py Version {discord.__version__}")
		await ctx.send(embed=info_emb)
	@is_dev()
	@commands.command(brief="Reloads all cogs [DEVELOPER ONLY]", description="Shuts off and restarts all cogs, [DEV ONLY]")
	async def reloadall(self, ctx):
		before = Embed(title="Working...", color=0x651FFF)
		before.add_field(name="Reloading all cogs...", value=(", ".join(self.bot.cogs_list)))
		after= Embed(title="All done!", color=0x651FFF)
		after.add_field(name="All cogs were reloaded", value=(", ".join(self.bot.cogs_list)))
		message = await ctx.send(embed=before)
		async with ctx.channel.typing():
			for c in self.bot.cogs_list:
				self.bot.reload_extension(c)
		await message.edit(embed=after)
	@reloadall.error
	async def rla_error(self, ctx, exc):
		if isinstance(exc, commands.errors.CheckFailure):
			embed = Embed(color=0x651FFF)
			embed.add_field(name="An Error Occurred", value="You are not a dev, you cannot run this command")
			await ctx.send(embed=embed)
		else:
			error = Embed(color=0x651FFF)
			error.add_field(name="An unknown error occurred", value="We don't know what happened")
			error.add_field(name="Here is the error", value=exc, inline=False)
			await ctx.send(embed=error)

	def cleanup_code(self, content):
		"""Automatically removes code blocks from the code."""
        # remove ```py\n```
		if content.startswith('```') and content.endswith('```'):
			return '\n'.join(content.split('\n')[1:-1])

        # remove `foo`
		return content.strip('` \n')
	
	@is_dev()
	@commands.command(pass_context=True, hidden=False, name='eval', description="Evaluates a given codeblock with a predefined environment [DEV ONLY]", brief="Runs given code [DEV ONLY]")
	async def _eval(self, ctx, *, body: str):
		"""Evaluates a code"""
		env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result,
            'mod_env': self,
            '': 
        }

		env.update(globals())

		body = self.cleanup_code(body)
		stdout = io.StringIO()

		to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

		try:
			exec(to_compile, env)
		except Exception as e:
			return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

		func = env['func']
		try:
			with redirect_stdout(stdout):
				ret = await func()
		except Exception as e:
			value = stdout.getvalue()
			await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
		else:
			value = stdout.getvalue()
			try:
				await ctx.message.add_reaction('\u2705')
			except:
				pass

			if ret is None:
				if value:
					await ctx.send(f'```py\n{value}\n```')
			else:
				self._last_result = ret
				await ctx.send(f'```py\n{value}{ret}\n```')
	
def setup(bot):
	bot.add_cog(DevNStats(bot))
	print ("Cog DevNStats online...")