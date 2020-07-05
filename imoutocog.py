import discord
from discord.ext import commands
import inspect
import random


class ImoutoCog(commands.Cog):
    """
    妹ボット
    雑用兼テスト用
    """

    @commands.command()
    async def hello(self, ctx):
        """挨拶"""
        await ctx.send('妹「お兄ちゃん！お兄ちゃん！お兄ちゃん！」')

    @commands.command()
    async def add(self, ctx, a: int, b: int):
        """引数確認用コマンド 足し算"""
        await ctx.send(f'妹「足し算の答えはね {str(a + b)} だよ！」')

    @commands.command()
    async def refer(self, ctx):
        """
        振り返りのために、過去に対局した対局結果をランダムに配信してくれる

        Parameters
        ----------
        ctx : ~ext.commands.Context
            description
        """
        pass

    @commands.command()
    async def ctx_methods(self, ctx):
        """ctxの持つメソッド確認"""
        ctx.send(type(ctx))
        for x in inspect.getmembers(ctx, inspect.ismethod):
            await ctx.send(x[0])
            print(x[0])

        await ctx.send(ctx.__class__.__name__)

    @commands.command(aliases=['tt'])
    async def test(self, ctx):
        """test用コマンド"""
        await ctx.send(ctx.author)
        await ctx.send(ctx.guild.members)
        await ctx.send(ctx.guild)
        await ctx.send(ctx.message)

    @commands.command()
    async def info(self, ctx):
        """ボット紹介・解説"""
        embed = discord.Embed(
            title="elona-bot",
            description="妹「お兄ちゃんのために私頑張るよっ！」",
            color=0xeee657
        )

        # give info about you here
        embed.add_field(name="Author", value="kanikun")

        # give users a link to invite thsi bot to their server
        embed.add_field(
            name="Invite",
            value="[Invite link](<insert your OAuth invitation link here>)"
        )

        await ctx.send(embed=embed)

    @commands.command()
    async def pins(self, ctx):
        """ピン留めメッセージをすべて表示する"""
        await ctx.send("妹「これが今までのすべての問題だよ！」")
        pins = await ctx.pins()
        for pin in pins:
            message = await ctx.fetch_message(pin.id)
            await ctx.send(message.content)

    @commands.command()
    async def pins_random(self, ctx):
        """ピン留めメッセージの中からランダムで一つ表示する"""
        await ctx.send("妹「とっておきの問題を出してあげるね！」")
        pins = await ctx.pins()
        pin = random.choice(pins)
        message = await ctx.fetch_message(pin.id)
        await ctx.send(message.content)

    @commands.group()
    async def rem(self, ctx):
        """リマインド機能

        時間を指定して登録することで、指定時間に通知を飛ばすことができる
        サブコマンド
        add 指定時間の登録
        show 登録したリマインドの表示
        """
        if ctx.invoked_subcommand is None:
            await ctx.send('妹「サブコマンドを入力して欲しいよっ！」')

    @rem.command(name='add')
    async def rem_add(self, ctx, target_time):
        # datetimeList += target_time
        pass

    @rem.command(name='show')
    async def rem_show(self, ctx):
        pass
