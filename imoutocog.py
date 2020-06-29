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
    async def neko(self, ctx):
        """挨拶"""
        await ctx.send('妹「お兄ちゃん！お兄ちゃん！お兄ちゃん！」')

    @commands.command()
    async def add(self, ctx, a: int, b: int):
        """引数確認用コマンド 足し算"""
        await ctx.send("result is " + str(a + b))

    @commands.command()
    async def refer(self, ctx):
        """
        振り返りのために、過去に対局した対局結果をランダムに配信してくれる

        Parameters
        ----------
        ctx : ~ext.commands.Context
            description
        """
        msg = "aa"
        await ctx.send(msg)

        # await ctx.send(guild.get_member())
        await ctx.send(ctx.guild.get_member())
        # member = Guild.get_member()
        # await ctx.send(member)

        # pin

    @commands.command()
    async def ctx_methods(self, ctx):
        """ctxの持つメソッド確認"""
        ctx.send(type(ctx))
        for x in inspect.getmembers(ctx, inspect.ismethod):
            await ctx.send(x[0])
            print(x[0])

        await ctx.send(ctx.__class__.__name__)
        # await ctx.send(guild)

    @commands.command()
    async def test(self, ctx):
        """test用コマンド"""
        await ctx.send(ctx.author)
        await ctx.send(ctx.guild.members)
        await ctx.send(ctx.guild)
        await ctx.send(ctx.message)

    @commands.command()
    async def test2(self, ctx):
        """test用コマンドその二"""
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

        # Shows the number of servers the bot is member of.
        # embed.add_field(name="Server count", value=f"{len(ctx.guild)}")

        # give users a link to invite thsi bot to their server
        embed.add_field(
            name="Invite",
            value="[Invite link](<insert your OAuth invitation link here>)"
        )

        await ctx.send(embed=embed)

    @commands.command()
    async def hello(self, ctx, *, member: discord.Member = None):
        """Says hello"""
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send('Hello {0.name}~'.format(member))
        else:
            await ctx.send('Hello {0.name}... This feels familiar.'.format(member))
        self._last_member = member

    @commands.command()
    async def pins(self, ctx):
        """ピン留めメッセージをすべて表示する"""
        pins = await ctx.pins()
        for pin in pins:
            message = await ctx.fetch_message(pin.id)
            await ctx.send(message.content)

    @commands.command()
    async def pins_random(self, ctx):
        """ピン留めメッセージの中からランダムで一つ表示する"""
        pins = await ctx.pins()
        pin = random.choice(pins)
        message = await ctx.fetch_message(pin.id)
        await ctx.send(message.content)
