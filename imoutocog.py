import discord
from discord.ext import commands
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
    async def roll(self, ctx, dice: str = "1d6"):
        """ダイスロール"""
        try:
            rolls, surfaces = map(int, dice.split("d"))
        except Exception:
            await ctx.send("妹「NdNの形式でサイコロを振ってね！お兄ちゃん！」\ni.e. 1d6で六面ダイスを一回振ります。")
            return

        pips = [random.randint(1, surfaces) for _ in range(rolls)]
        await ctx.send(f'妹「お兄ちゃん！サイコロ{"いっぱい"*(rolls>2)}振るよ！(コロコロー)」')
        m = f'{" ".join(map(str, pips))}\n' + (rolls>1)*f'sum = {sum(pips)}'
        await ctx.send(m)

    @commands.command()
    async def choose(self, ctx, *choices: str):
        """引数からランダムで一つ選ぶ"""
        await ctx.send(random.choice(choices))

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

    @commands.command(aliases=['p'])
    async def pins_random(self, ctx):
        """ピン留めメッセージの中からランダムで一つ表示する"""
        # todo 使用していない

        await ctx.send("妹「とっておきの問題を出してあげるね！」")

        pins = await ctx.pins()
        pin = random.choice(pins)
        message = await ctx.fetch_message(pin.id)
        await ctx.send(message.content)
