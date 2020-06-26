import discord
import inspect
from discord.ext import commands
import os
import traceback
GUILD_ID = "696698789989187604"

bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']

# get_guild
guild = bot.get_guild(GUILD_ID)

@bot.event
async def on_ready():
    print("妹「お兄ちゃん、私はもう準備万端だよっ！」")
    print(discord.__version__)

@bot.event
async def on_command_error(ctx, error):
    """
    コマンドエラー時メッセージ
    """
    await ctx.send("妹「お兄ちゃん？何言ってるの？」")
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)

@bot.command()
async def neko(ctx):
    await ctx.send('お兄ちゃん！お兄ちゃん！お兄ちゃん！')

@bot.command()
async def add(ctx, a: int, b: int):
    await ctx.send("result is " + str(a + b))

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

@bot.command()
async def refer(ctx):
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

@bot.command()
async def aa(ctx):
    ctx.send(type(ctx))
    for x in inspect.getmembers(ctx, inspect.ismethod):
        ctx.send(x[0])
        print(x[0])

    await ctx.send(ctx.__class__.__name__)
    # await ctx.send(guild)

@bot.command()
async def test(ctx):
    ctx.send(ctx.author)
    ctx.send(ctx.guild.members)
    ctx.send(ctx.guild)
    ctx.send(ctx.user)
    ctx.send(ctx.message)

bot.run(token)
