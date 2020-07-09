from discord.ext import tasks, commands
from datetime import datetime
from datetime import timedelta
import random
import itertools


class KumiromiCog(commands.Cog):
    """
    クミロミボット

    リマインド機能
    """

    # リマインドの「時間」と「メモ」
    # 同一時間に２つ以上のメモはない想定
    time_and_memos = {}

    # トーナメントの設定
    members = ['tako', 'ojii', 'potta']
    starttime = 1  # トーナメント開始から始めの試合までの準備時間
    playtime = 1
    breaktime = 2

    # 大会種目
    events = ['囲碁', '将棋', 'オセロ']

    def format_datetime(self, date, time):
        """日付と時刻からdatetime型を返す

        date: string YYYY-MM-DD
        time: string HH:MM
        return: datetime YYYY-MM-DD HH:MM
        """
        if date == 'today':  # 日付が today だったら、今日の日付に変換する
            n = datetime.now()
            date = datetime(n.year, n.month, n.day)
            date = datetime.strftime(date, '%Y-%m-%d')

        # セットする時刻を整形
        set_time = date + " " + time
        set_datetime = datetime.strptime(set_time, '%Y-%m-%d %H:%M')

        return set_datetime

    def round_now(self):
        """現在の時刻をdatetime型YYYY-MM-DD HH:MMで返す"""

        n = datetime.now()
        now = datetime(n.year, n.month, n.day, n.hour, n.minute)
        return now

    def cog_unload(self):
        self.reminder_loop.cancel()

    @tasks.loop(minutes=1.0)
    async def reminder_loop(self, ctx):
        """リマインドのメインループ処理"""

        now = self.round_now()
        if now in self.time_and_memos.keys():
            await ctx.send(self.time_and_memos[now])

    @commands.group(aliases=['rem'])
    async def reminder(self, ctx):
        """リマインド機能

        時間を指定して登録することで、指定時間に通知を飛ばすことができる
        サブコマンド
        set 指定時間の登録
        del リマインドの削除
        show 登録したリマインドの表示
        """
        if ctx.invoked_subcommand is None:
            await ctx.send('クミロミ「…？お願いだからサブコマンドを入力してね…？」')

    @reminder.command(aliases=['start'])
    async def reminder_start(self, ctx):
        """リマインド機能を開始する"""
        self.reminder_loop.start(ctx)
        await ctx.send("クミロミ「分かった…君に時を告げるよ…」")

    @reminder.command(aliases=['set', 'add'])
    async def reminder_set(self, ctx, date, time, memo):
        """リマインドをセットする"""
        set_datetime = self.format_datetime(date, time)

        self.time_and_memos[set_datetime] = memo
        await ctx.send("クミロミ「君の未来への想いを受け取ったよ…」 " + "時刻：" + str(set_datetime) + "  内容：" + memo)

    @reminder.command(aliases=['show', 'look'])
    async def reminder_show(self, ctx):
        """リマインドの一覧を見せる"""
        str_all_time_and_memos = ""
        if self.time_and_memos:
            await ctx.send("クミロミ「これが君たちのこれからの想いだよ…」")
            for k, v in self.time_and_memos.items():
                str_all_time_and_memos += str(k) + ", " + str(v)
                await ctx.send(str_all_time_and_memos)
        else:
            await ctx.send("クミロミ「これから想いを綴っていこうね…？」")

    @reminder.command(aliases=['del'])
    async def reminder_delete(self, ctx, date, time):
        set_datetime = self.format_datetime(date, time)

        if set_datetime in self.time_and_memos.keys():
            self.time_and_memos.remove(set_datetime)
            await ctx.send("クミロミ「消した…消しちゃったね…、悲しいね…」")

    @commands.group(aliases=['tour'])
    async def tournament(self, ctx):
        """トーナメント機能

        メンバと時間の設定をすることで、大会用のリマインドを発行する
        """
        if ctx.invoked_subcommand is None:
            await ctx.send('クミロミ「…？お願いだからサブコマンドを入力してね…？')

    @tournament.command(aliases=['start'])
    async def tournament_start(self, ctx):
        player_comb = list(itertools.combinations(self.members, 2))  # 対局総組み合わせ

        now = self.round_now()
        targettime = now + timedelta(minutes=self.starttime)

        for pl1, pl2 in player_comb:  # 対局者2人ずつ
            for event in self.events:  # 全種目
                memo = str(pl1) + "と" + str(pl2) + "の" + event + "の対局開始時間です。"
                self.time_and_memos[targettime] = memo
                targettime += timedelta(minutes=self.playtime)

            # 2人の全種目対戦終了して、休憩タイム
            targettime += timedelta(self.breaktime)

        await ctx.send("クミロミ「さぁ、僕に君たちの力を見せて…欲しいな…」")

    @tournament.command(aliases=['set', 'show'])
    async def tournament_set(self, ctx):
        """トーナメントの設定・表示"""
        if ctx.invoked_subcommand is None:
            await ctx.send("クミロミ「いまの設定はこんな感じ…だね…」")
            await ctx.send("members:" + " ".join(self.members))
            await ctx.send("playtime:" + str(self.playtime))
            await ctx.send("breaktime:" + str(self.breaktime))

    @ tournament.group(aliases=['member'])
    async def tournament_member(self, ctx):
        """トーナメントの設定・メンバ"""
        pass

    @ tournament_member.command(aliases=['add'])
    async def tournament_member_add(self, ctx, name):
        """トーナメントの設定・メンバーの追加"""
        self.members.append(name)
        await ctx.send("クミロミ「ふふ…" + name + "というんだね…。君も僕の信者になる…？」")

    @ tournament_member.command(aliases=['remove'])
    async def tournament_member_remove(self, ctx, name):
        """トーナメントの設定・メンバーの削除"""
        if name in self.members:
            self.members.remove(name)
            await ctx.send("クミロミ「" + name + "なんていう人、元から居なかった…よね…」")
        else:
            await ctx.send("クミロミ「そんな人、元から居ないよ…？」")

    @ tournament_member.command(aliases=['shuffle'])
    async def tournament_member_shuffle(self, ctx):
        """メンバの順番をシャッフルする

        トーナメント開始前に実施する想定"""
        random.shuffle(self.members)
        await ctx.send("クミロミ「メンバの順番…これでバラバラだよ…」")
        await ctx.send("members:" + " ".join(self.members))

    @ tournament.command(aliases=['playtime'])
    async def tournament_playtime(self, ctx, time):
        """トーナメントの設定・対局時間の設定"""
        self.playtime = time
        await ctx.send("クミロミ「遊ぶ時間を" + str(self.playtime) + "に設定したよ…？」")

    @ tournament.command(aliases=['breaktime'])
    async def tournament_breaktime(self, ctx, time):
        """トーナメントの設定・休憩時間の設定"""
        self.breaktime = time
        await ctx.send("クミロミ「休憩時間を" + str(self.breaktime) + "に設定したよ…？」")
