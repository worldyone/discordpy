import discord
from discord.ext import commands
import os
import traceback
import asyncio
from imoutocog import ImoutoCog
from kumiromicog import KumiromiCog


token = os.environ['DISCORD_BOT_TOKEN']


class DiscordBot(commands.Bot):

    async def on_ready(self):
        """
        起動準備完了時イベント
        """
        print("妹「お兄ちゃん、私はもう準備万端だよっ！」")
        print(discord.__version__)

    async def on_command_error(self, ctx, error):
        """
        コマンドエラー時イベント
        """
        await ctx.send("妹「お兄ちゃん？何言ってるの？」")
        orig_error = getattr(error, "original", error)
        error_msg = ''.join(
            traceback.TracebackException.from_exception(orig_error).format())
        await ctx.send(error_msg)


def setup(bot):
    """
    ボット実行前処理
    """
    @bot.command()
    async def thumbup(ctx):
        """
        リアクションを待機するアクション

        :thumbup:してあげてね！
        """
        await ctx.send('妹「お兄ちゃん！私に 👍 を送って欲しいな！」')

        def check(reaction, user):
            return user == ctx.message.author and str(reaction.emoji) == '👍'

        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send('👎')
        else:
            await ctx.send('👍')


if __name__ == '__main__':
    # ボット作成
    bot = DiscordBot(command_prefix='e.')

    # 妹ボットの導入
    bot.add_cog(ImoutoCog(bot))

    # クミロミボットの導入
    bot.add_cog(KumiromiCog(bot))

    # ボット実行前処理
    setup(bot)

    # ボット実行
    bot.run(token)
