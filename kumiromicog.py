from discord.ext import tasks, commands
from datetime import datetime


class KumiromiCog(commands.Cog):
    """
    クミロミボット

    リマインド機能
    """

    datetimeList = []

    def cog_unload(self):
        self.reminder.cancel()

    @tasks.loop(minutes=1.0)
    async def reminder(self, ctx):
        # await ctx.send("<@{0}> {1}".format(ctx.author.id, content))
        await ctx.send("check time now")

        now = datetime.now().strftime('%Y/%m/%d %H:%M')
        if now in self.datetimeList:
            await ctx.send(now)

    @commands.command()
    async def start_reminder(self, ctx):
        self.reminder.start(ctx)
        await ctx.send("リマインダを開始しました")

    @commands.command()
    async def set_reminder(self, ctx, time):
        self.datetimeList += '2020/07/05 19:52'
        await ctx.send("リマインダをセットしました")
