#pylint:disable=W0611
#pylint:disable=C0304
import discord
from discord.ext import commands as cmds
from datetime import datetime
bot = cmds.Bot(command_prefix="//", case_insensitive=True, intents=discord.Intents.all())
class MyHelp(cmds.MinimalHelpCommand):
    def get_command_signature(self, command):
        return '%s%s %s' % (self.clean_prefix, command.qualified_name, command.signature)

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Help")
        for cog, commands in mapping.items():
            filtered = await self.filter_commands(commands, sort=True)
            command_signatures = [self.get_command_signature(c) for c in filtered]
            if command_signatures:
                cog_name = getattr(cog, "qualified_name", "No Category")
                embed.add_field(name=cog_name, value="\n".join(command_signatures), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)
    async def send_command_help(self, command):
        embed = discord.Embed(title=self.get_command_signature(command))
        embed.add_field(name="Help", value=command.help)
        alias = command.aliases
        if alias:
            embed.add_field(name="Aliases", value=", ".join(alias), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)

bot.help_command = MyHelp()
bot.uptime = datetime.now()
bot.cogs_list = [
"cogs.antiraid",
"cogs.UserManagement",
"cogs.DevNStat"]
@bot.event
async def on_ready():
	print("Sharp shooting, Pilot")
	print(f"Signed on as {bot.user}\nIn {len(bot.guilds)} Guilds\n{len(bot.users)} Users Are Visible")
bot.load_extension("cogs.antiraid")
bot.load_extension("cogs.UserManagement")
bot.load_extension("cogs.DevNStat")

bot.run("ODAxOTA5NTI5MzYwMjAzNzg4.YAnicg._tZFrP99_66chtLSUqlA1biTyac")