from discord.ext import tasks, commands
from datetime import datetime


class KumiromiCog(commands.Cog):
    """
    クミロミボット

    リマインド機能
    """

    # リマインドの「時間」と「メモ」
    # 同一時間に２つ以上のメモはない想定
    time_and_memos = {}

    members = []
    playtime = 15
    breaktime = 10

    def cog_unload(self):
        self.reminder_loop.cancel()

    @tasks.loop(minutes=1.0)
    async def reminder_loop(self, ctx):
        # await ctx.send("<@{0}> {1}".format(ctx.author.id, content))
        await ctx.send("check time now")

        now = datetime.now()
        now = datetime(now.year, now.month, now.day, now.hour, now.minute)
        if now in self.time_and_memos.keys():
            await ctx.send(self.time_and_memos[now])

    @commands.group(aliases=['rem'])
    async def reminder(self, ctx):
        """リマインド機能

        時間を指定して登録することで、指定時間に通知を飛ばすことができる
        サブコマンド
        add 指定時間の登録
        show 登録したリマインドの表示
        """
        if ctx.invoked_subcommand is None:
            await ctx.send('クミロミ「…？お願いだからサブコマンドを入力してね…？」')

    @reminder.command(aliases=['start'])
    async def reminder_start(self, ctx):
        """リマインド機能を開始する"""
        self.reminder_loop.start(ctx)
        await ctx.send("クミロミ「分かった…君に時を告げるよ…")

    @reminder.command(aliases=['set'])
    async def reminder_set(self, ctx, date, time, memo):
        """リマインドをセットする"""
        set_time = date + " " + time
        set_datetime = datetime.strptime(set_time, '%Y-%m-%d %H:%M')
        self.time_and_memos[set_datetime] = memo
        await ctx.send("クミロミ「君の未来への想いを受け取ったよ…」 " + "時刻：" + set_time + "  内容：" + memo)

    @commands.group(aliases=['tour'])
    async def tournament(self, ctx):
        """トーナメント機能

        メンバと時間の設定をすることで、大会用のリマインドを発行する
        """
        if ctx.invoked_subcommand is None:
            await ctx.send('クミロミ「…？お願いだからサブコマンドを入力してね…？')

    @tournament.command(aliases=['start'])
    async def tournament_start(self, ctx):
        pass

    @tournament.group(aliases=['set'])
    async def tournament_set(self, ctx):
        """トーナメントの設定・表示"""
        if ctx.invoked_subcommand is None:
            await ctx.send("クミロミ「いまの設定はこんな感じ…だね…」")
            await ctx.send("members:" + " ".join(self.members))
            await ctx.send("playtime:" + str(self.playtime))
            await ctx.send("breaktime:" + str(self.breaktime))

    @tournament_set.group(aliases=['member'])
    async def tournament_set_member(self, ctx):
        """トーナメントの設定・メンバ"""
        pass

    @tournament_set_member.command(aliases=['add'])
    async def tournament_set_member_add(self, ctx, name):
        """トーナメントの設定・メンバーの追加"""
        self.members.append(name)
        await ctx.send("クミロミ「ふふ…" + name + "というんだね…。君も僕の信者になる…？」")

    @tournament_set_member.command(aliases=['remove'])
    async def tournament_set_member_remove(self, ctx, name):
        """トーナメントの設定・メンバーの削除"""
        if name in self.member:
            self.members.remove(name)
            await ctx.send("クミロミ「" + name + "なんていう人、元から居なかった…よね…」")
        else:
            await ctx.send("クミロミ「そんな人、元から居ないよ…？」")

    @tournament_set.command(aliases=['playtime'])
    async def tournament_set_playtime(self, ctx, time):
        """トーナメントの設定・対局時間の設定"""
        self.playtime = time
        await ctx.send("クミロミ「遊ぶ時間を" + str(self.playtime) + "に設定したよ…？」")

    @tournament_set.command(aliases=['breaktime'])
    async def tournament_set_breaktime(self, ctx, time):
        """トーナメントの設定・休憩時間の設定"""
        self.breaktime = time
        await ctx.send("クミロミ「休憩時間を" + str(self.breaktime) + "に設定したよ…？」")
