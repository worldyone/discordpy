import discord
from discord.ext import commands
import os
import traceback
from imoutocog import ImoutoCog
from kumiromicog import KumiromiCog
from quizcog import QuizCog


token = "NzM2Njc5MzUzNDU4NDkxNDc2.XxyUHA.4tnGIRyhPP7vQFOz6nAYHvbTPNI"

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


if __name__ == '__main__':
    # ボット作成
    bot = DiscordBot(command_prefix='e.')

    # 妹ボットの導入
    bot.add_cog(ImoutoCog(bot))

    # クミロミボットの導入
    bot.add_cog(KumiromiCog(bot))

    # クイズボットの導入
    bot.add_cog(QuizCog(bot))

    # ボット実行
    bot.run(token)
