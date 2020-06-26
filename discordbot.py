import discord
from discord.ext import commands
import os
import traceback

bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']


@bot.event
async def on_command_error(ctx, error):
    """
    コマンドエラー時メッセージ
    """
    # orig_error = getattr(error, "original", error)
    # error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    # await ctx.send(error_msg)
    await ctx.send("そんなコマンド知らないにゃ！")


@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def neko(ctx):
    await ctx.send('nyan')

@bot.command()
async def add(ctx, a: int, b: int):
    await ctx.send("result is " + (a + b))

@bot.command()
async def info(ctx):
    embed = discord.Embed(title="nice bot", description="Nicest bot there is ever.", color=0xeee657)

    # give info about you here
    embed.add_field(name="Author", value="<YOUR-USERNAME>")

    # Shows the number of servers the bot is member of.
    embed.add_field(name="Server count", value=f"{len(bot.guilds)}")

    # give users a link to invite thsi bot to their server
    embed.add_field(name="Invite", value="[Invite link](<insert your OAuth invitation link here>)")

    await ctx.send(embed=embed)

# @bot.command()
# async def refer(ctx):
#     """
#     振り返りのために、過去に対局した対局結果をランダムに配信してくれる

#     Parameters
#     ----------
#     ctx : ~ext.commands.Context
#         対象の果物のマスタID。
#     """
#     msg = "aa"
#     await ctx.send(msg)

#     member = Guild.get_member()
#     await ctx.send(member)


# def pred(m):
#     return m.author == message.author and m.channel == message.channel

# try:
#     msg = await client.wait_for('message', check=pred, timeout=60.0)
# except asyncio.TimeoutError:
#     await channel.send('You took too long...')
# else:
#     await channel.send('You said {0.content}, {0.author}.'.format(msg))

bot.run(token)
