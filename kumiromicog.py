import discord
from discord.ext import tasks, commands
from datetime import datetime
from datetime import timedelta
from datetime import timezone
import random
import itertools
from collections import OrderedDict


class KumiromiCog(commands.Cog):
    """
    クミロミボット

    リマインド機能
    """

    # リマインドの「時間: datetime(YYYY-MM-DD HH:MM)」と「メモ: str」
    # 同一時間(分までの粒度)に２つ以上のメモはない想定
    # todo 頑張ってDBに変更する。いつか誰かが頑張る。
    time_and_memos = OrderedDict()

    # トーナメントの設定
    members = ['tako2', 'gushun20', 'murata2415']
    starttime = 5  # トーナメント開始から始めの試合までの準備時間(分)
    playtime = 25  # 対局時間(分)
    breaktime = 15  # 休憩時間(分)

    # 大会種目
    events = ['囲碁', '将棋', 'オセロ']

    # 固定のセリフ
    # 来週のリマインド通知用のセリフ
    REMIND_MESSAGE_1 = "そんな装備で大丈夫か？"

    # トーナメント開始前のセリフ
    MESSAGES_TOURNAMENT_START = [
        "クミロミ「君たちの対局楽しみにしてるよ…」",
        "クミロミ「ずっと見守ってるよ…？」",
        "クミロミ「みんな頑張って…、みんな偉いな…」",
        "クミロミ「前回の盛り上がった対局を思い出してきたよ…」",
        "クミロミ「さぁ…いまから闘おう…？」",
        "クミロミ「ふふ…、今回はどんな対局になるだろうね…」？",
        "クミロミ「闘いの準備が整ったよ…。さぁ、君たちの力を僕に見せて……欲しいな…」",
    ]

    def format_datetime(self, date: str, time: str):
        """日付と時刻からdatetime型を返す

        date: string YYYY-MM-DD
        time: string HH:MM
        return: datetime YYYY-MM-DD HH:MM
        """
        if date == 'today':  # 日付が today だったら、今日の日付に変換する
            n = datetime.now()
            date = datetime(n.year, n.month, n.day)
            date = datetime.strftime(date, '%Y-%m-%d')

        if date == 'nextweek':  # 日付が nextweek だったら、来週の日付に変換する
            n = datetime.now()
            date = datetime(n.year, n.month, n.day + 7)
            date = datetime.strftime(date, '%Y-%m-%d')

        # セットする時刻を整形
        set_time = date + " " + time
        set_datetime = datetime.strptime(set_time, '%Y-%m-%d %H:%M')

        return set_datetime

    def round_now(self):
        """現在の日本時刻をdatetime型YYYY-MM-DD HH:MMで返す"""

        n = datetime.now(timezone(timedelta(hours=9)))  # 日本時刻を指定して取得
        now = datetime(n.year, n.month, n.day, n.hour, n.minute)
        return now

    def cog_unload(self):
        self.reminder_loop.cancel()

    @tasks.loop(seconds=31)
    async def reminder_loop(self, ctx):
        """リマインドのメインループ処理"""

        now = self.round_now()
        if now in self.time_and_memos.keys():
            await ctx.send(self.time_and_memos.pop(now))

    @commands.group(aliases=['rem'])
    async def reminder(self, ctx):
        """リマインド機能

        時間を指定して登録することで、指定時間に通知を飛ばすことができる
        サブコマンド
        start リマインド通知機能の開始
        stop リマインド通知機能の停止
        set リマインドの登録
        show 登録したリマインドの表示
        del リマインドの削除
        """
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(
                title="リマインド機能",
                description="リマインド機能の使い方です。"
            )

            embed.add_field(
                name="start", value="リマインド通知機能の開始\n        e.rem start", inline=False)
            embed.add_field(
                name="set", value="リマインドの登録\n        e.rem set 2020-01-01 20:00 It's TRIBOARDIAN!!", inline=False)
            embed.add_field(
                name="stop", value="リマインド通知機能の停止\n        e.rem stop", inline=False)
            embed.add_field(
                name="show", value="登録したリマインドの表示\n        e.rem show", inline=False)
            embed.add_field(
                name="del", value="リマインドの削除\n        e.rem del 2020-01-01 20:00", inline=False)

            await ctx.send(embed=embed)

    @reminder.command(aliases=['start'])
    async def reminder_start(self, ctx):
        """リマインド機能を開始する"""
        self.reminder_loop.start(ctx)
        await ctx.send("クミロミ「分かった…君に想いを告げるよ…」")

    @reminder.command(aliases=['stop'])
    async def reminder_stop(self, ctx):
        """リマインド機能を停止する"""
        self.reminder_loop.cancel()
        await ctx.send("クミロミ「うん…一旦休憩するね…」")

    @reminder.command(aliases=['set', 'add'])
    async def reminder_set(self, ctx, date: str, time: str, *memo: str):
        """リマインドをセットする"""
        set_datetime = self.format_datetime(date, time)

        self.time_and_memos[set_datetime] = " ".join(memo)
        await ctx.send("クミロミ「君の未来への想いを受け取ったよ…」 " + "時刻：" + str(set_datetime) + "  内容：" + " ".join(memo))

    @reminder.command(aliases=['show', 'look', 'list'])
    async def reminder_show(self, ctx):
        """リマインドの一覧を見せる"""
        str_all_time_and_memos = ""
        if self.time_and_memos:
            await ctx.send("クミロミ「これが君たちのこれからの想いだよ…」")
            for k, v in self.time_and_memos.items():
                str_all_time_and_memos += str(k) + "    " + str(v) + "\n"
            await ctx.send(str_all_time_and_memos)
        else:
            await ctx.send("クミロミ「これから想いを綴っていこうね…？」")

    @reminder.command(aliases=['del', 'delete', 'remove'])
    async def reminder_delete(self, ctx, index: int = 0):
        """リマインドを削除する"""
        # 引数が指定されなければ、リストを提示する
        if index == 0:
            message = "クミロミ「消したい番号を選択してね…」\n  i.e. e.rem del 3\n"
            i = 1
            for time, memo in self.time_and_memos.items():
                message += f'[{i}]: {time} , {memo}\n'
                i += 1
            await ctx.send(message)
        else:
            # 選択された番号のリマインドを削除して、削除終えたリマインドリストを提示する
            message = ""
            i = print_i = 0
            for time, memo in self.time_and_memos.items():
                i += 1
                if i == index:
                    remove_time = time
                    continue
                print_i += 1
                message += f'[{print_i}]: {time} , {memo}\n'
            del self.time_and_memos[remove_time]

            await ctx.send(message)

    @reminder.command(aliases=['all delete'])
    async def reminder_all_delete(self, ctx):
        """リマインドをすべて削除する"""
        self.time_and_memos.clear()

    @commands.group(aliases=['tour', 'tt'])
    async def tournament(self, ctx):
        """トーナメント機能

        メンバと時間の設定をすることで、大会用のリマインドを発行する
        """
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(
                title="トーナメント機能",
                description="トーナメント機能の使い方です。"
            )

            embed.add_field(
                name="start", value="トーナメントの開始\n        e.tour start", inline=False)
            embed.add_field(
                name="set", value="トーナメントの設定\n        e.tour set", inline=False)
            embed.add_field(
                name="member", value="登録したメンバの表示・設定\n        e.tour member", inline=False)
            embed.add_field(name="playtime",
                            value="トーナメントの対局時間の設定\n        e.tour playtime 15", inline=False)
            embed.add_field(name="breaktime",
                            value="トーナメントの休憩時間の設定\n        e.tour breaktime 10", inline=False)

            await ctx.send(embed=embed)

    @tournament.command(aliases=['start'])
    async def tournament_start(self, ctx):
        player_comb = list(itertools.combinations(self.members, 2))  # 対局総組み合わせ

        now = self.round_now()
        targettime = now + timedelta(minutes=self.starttime)  # 開始時間のセット

        for pl1, pl2 in player_comb:  # 対局者2人ずつ
            for event in self.events:  # 全種目
                memo = str(pl1) + " と " + str(pl2) + \
                    " の " + event + " の対局開始時間です。"
                self.time_and_memos[targettime] = memo
                targettime += timedelta(minutes=self.playtime)

            # 2人の全種目対戦終了して、休憩タイム
            targettime += timedelta(minutes=self.breaktime)

        # 大会終了後に、次回大会を実施するかどうか聞くリマインド
        # 一週間後前日(6日後)の20時を指定
        remind_time = datetime(
            year=now.year, month=now.month, day=now.day + 6, hour=20)
        memo = "クミロミ「大会よく頑張ったね……。とても有意義な時間だったよ。」\n" + \
            "クミロミ「今度もまた一緒に遊んでもいい……かな……？」\n" + \
            "e.rem set " + \
            datetime.strftime(remind_time, '%Y-%m-%d %H:%M') + \
            " " + self.REMIND_MESSAGE_1
        self.time_and_memos[targettime] = memo

        await ctx.send(random.choice(self.MESSAGES_TOURNAMENT_START))
        await self.reminder_show(ctx)

    @tournament.command(aliases=['set', 'show', 'look', 'list'])
    async def tournament_set(self, ctx):
        """トーナメントの設定・表示"""
        if ctx.invoked_subcommand is None:
            await ctx.send("クミロミ「いまの設定はこんな感じ……だね…」")
            embed = discord.Embed(
                title="トーナメント設定",
                description="トーナメントの設定情報です。"
            )

            embed.add_field(
                name="メンバ", value="\n    ".join(self.members), inline=False)
            embed.add_field(
                name="対局時間", value=str(self.playtime), inline=False)
            embed.add_field(
                name="休憩時間", value=str(self.breaktime), inline=False)

            await ctx.send(embed=embed)

    @tournament.command(aliases=['playtime'])
    async def tournament_playtime(self, ctx, time: int):
        """トーナメントの設定・対局時間の設定"""
        self.playtime = time
        await ctx.send("クミロミ「遊ぶ時間を " + str(self.playtime) + "分 に設定したよ…」")

    @tournament.command(aliases=['breaktime'])
    async def tournament_breaktime(self, ctx, time: int):
        """トーナメントの設定・休憩時間の設定"""
        self.breaktime = time
        await ctx.send("クミロミ「休憩時間を " + str(self.breaktime) + "分 に設定したよ…」")

    @tournament.group(aliases=['member'])
    async def tournament_member(self, ctx):
        """トーナメントの設定・メンバ"""
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(
                title="メンバ設定機能",
                description="トーナメントのメンバ設定機能の使い方です。"
            )

            embed.add_field(
                name="add", value="メンバの追加\n        e.tour member add Taro", inline=False)
            embed.add_field(
                name="remove", value="メンバの脱退\n        e.tour member remove Taro", inline=False)
            embed.add_field(
                name="shuffle", value="メンバの順番をシャッフル\n        e.tour member shuffle", inline=False)

            await ctx.send(embed=embed)

    @tournament_member.command(aliases=['add'])
    async def tournament_member_add(self, ctx, name: str):
        """トーナメントの設定・メンバーの追加"""
        self.members.append(name)
        await ctx.send("クミロミ「ふふ…" + name + "というんだね…。君も僕の信者になる…？」")

    @tournament_member.command(aliases=['remove'])
    async def tournament_member_remove(self, ctx, name: str):
        """トーナメントの設定・メンバーの削除"""
        if name in self.members:
            self.members.remove(name)
            await ctx.send("クミロミ「" + name + "なんていう人、元から居なかった…よね…」")
        else:
            await ctx.send("クミロミ「そんな人、元から居ないよ…？」")

    @tournament_member.command(aliases=['shuffle'])
    async def tournament_member_shuffle(self, ctx):
        """メンバの順番をシャッフルする

        トーナメント開始前に実施する想定"""
        random.shuffle(self.members)
        await ctx.send("クミロミ「メンバの順番…これでバラバラだよ…」")

        embed = discord.Embed(
            title="トーナメントのメンバ",
            description="トーナメントの参加メンバです。"
        )
        embed.add_field(
            name="メンバ", value="\n    ".join(self.members), inline=False)
        await ctx.send(embed=embed)
