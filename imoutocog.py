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
        """引数確認用コマンド 足し算 i.e. e.add 1 2"""
        await ctx.send(f'妹「{a}＋{b}の答えはね、 {str(a + b)} だよ！」')

    @commands.command()
    async def roll(self, ctx, dice: str):
        """ダイスロール"""
        try:
            rolls, surfaces = map(int, dice.split("d"))
        except Exception:
            await ctx.send("NdNの形式でサイコロを振ってね！お兄ちゃん！\ni.e. 1d6で六面ダイスを一回振ります。")
            return

        pips = [random.randint(1, surfaces) for _ in range(rolls)]
        await ctx.send(f'お兄ちゃん！サイコロ{"いっぱい"*(rolls>1)}振るよ！(コロコロー)')
        m = f'{" ".join(map(str, pips))}\nsum = {sum(pips)}'
        await ctx.send(m)

    @commands.command()
    async def choose(self, ctx, *choices: str):
        """引数からランダムで一つ選ぶ"""
        await ctx.send(random.choice(choices))

    @commands.command()
    async def refer(self, ctx):
        """
        振り返りのために、過去に対局した対局結果をランダムに配信してくれる
        """

        # todo 未実装
        pass
        # ch = ctx.get_channnel(CHANNEL_ID)
        # messages = ch.history(200)
        # result_messages = list(filter(lambda x: "クエスト棋譜" in x, messages))
        # await ctx.send(random.choice(result_messages))

    @commands.command()
    async def ctx_methods(self, ctx):
        """ctxの持つメソッド確認"""
        ctx.send(type(ctx))
        for x in inspect.getmembers(ctx, inspect.ismethod):
            await ctx.send(x[0])
            print(x[0])

        await ctx.send(ctx.__class__.__name__)

    @commands.command()
    async def test(self, ctx):
        """test用コマンド"""
        # await ctx.send(ctx.author)
        # await ctx.send(ctx.guild.members)
        # await ctx.send(ctx.guild)
        # await ctx.send(ctx.message)

        # game = discord.Game("playing Triboardian!")
        # await ctx.change_presence(activity=game)
        mm = ctx.message.guild.members
        for m in mm:
            await ctx.send(m.name)

    @commands.command()
    async def info(self, ctx):
        """ボット紹介・解説"""
        embed = discord.Embed(
            title="elona-bot",
            description="妹「お兄ちゃんのために私、頑張るよっ！」",
            color=0xeee657
        )

        # give info about you here
        embed.add_field(name="Author", value="kanikun")

        await ctx.send(embed=embed)

    @commands.command()
    async def pins(self, ctx):
        """ピン留めメッセージをすべて表示する"""

        await ctx.send("妹「これが今までのすべての問題だよ！」")

        pins = await ctx.pins()
        for pin in pins:
            message = await ctx.fetch_message(pin.id)
            await ctx.send(message.content)

    @commands.command(aliases=['p'])
    async def pins_random(self, ctx):
        """ピン留めメッセージの中からランダムで一つ表示する"""

        await ctx.send("妹「とっておきの問題を出してあげるね！」")

        pins = await ctx.pins()
        pin = random.choice(pins)
        message = await ctx.fetch_message(pin.id)
        await ctx.send(message.content)
