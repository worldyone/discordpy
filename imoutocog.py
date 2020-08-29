import discord
from discord.ext import commands
import inspect
import random
import wikipedia


class ImoutoCog(commands.Cog):
    """
    妹ボット
    雑用兼テスト用
    """

    wikipedia_page = wikipedia.page("wikipedia")

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

    @commands.group(aliases=['q'])
    async def quiz_wikipedia(self, ctx):
        """wikipedia問題

        サブコマンド
        get 新しい単語をランダムで決定して、wikipediaページを取得する
        one 取得中のwikipediaページの一行目を表示する
        summary 取得中のwikipediaページのサマリーを表示する
        answer 取得中のwikipediaページのタイトルを表示する
        url 取得中のwikipediaページのurlを表示する
        find 指定した単語のwikipediaのページを取得する
        """
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(
                title="wikipediaクイズ機能",
                description="wikipediaクイズ機能の使い方です。"
            )

            embed.add_field(
                name="start", value="リマインド通知機能の開始\n        e.rem start", inline=False)

            await ctx.send(embed=embed)

    @quiz_wikipedia.command(aliases=['get', 'g'])
    async def get_random_wikipedia_page(self, ctx):
        wikipedia.set_lang("ja")

        await ctx.send("妹「wikipediaからランダムな記事を取ってくるね！」")

        # 日本語wikipediaからランダムな単語を一つ決めてページを取得する
        self.wikipedia_page = wikipedia.page(wikipedia.random())

        await ctx.send("妹「ランダムな記事を取ってきたよ！」")

    def do_hide_words(self, s: str):
        """答えがそのまま記載されている場合が多いので、マスクする"""

        hide_words = [self.wikipedia_page.title]
        space_word = s[:s.find("（")]
        hide_words.append(space_word)
        hide_words.append(
            self.wikipedia_page.title.replace(" ", ""))  # 「霧雨 魔理沙」を「霧雨魔理沙」でもヒットするように
        # 「Python（パイソン）は、...」の「パイソン」を取得する
        para_title = s[s.find("（") + 1: s.find("）")]
        hide_words.append(para_title)

        for hide_word in hide_words:
            s = s.replace(hide_word, "**ANSWER**")

        return s

    @quiz_wikipedia.command(aliases=['one'])
    async def print_one_summary(self, ctx):
        """一行表示"""
        one_line = self.wikipedia_page.summary  # まずサマリーを取得する
        one_line = one_line[:one_line.find("\n")]  # 最初の改行が来るまでを取得する

        # 答えがそのまま記載されている場合が多いので、マスクする
        question_sentence = self.do_hide_words(one_line)

        await ctx.send(question_sentence)

    @quiz_wikipedia.command(aliases=['summary'])
    async def print_summary(self, ctx):
        """サマリー表示"""
        summary = self.wikipedia_page.summary
        question_sentence = self.do_hide_words(summary)
        await ctx.send(question_sentence)

    @quiz_wikipedia.command(aliases=['answer', 'title'])
    async def print_answer(self, ctx):
        """答え表示"""
        await ctx.send(self.wikipedia_page.title)

    @quiz_wikipedia.command(aliases=['url'])
    async def print_url(self, ctx):
        """URLを表示"""
        await ctx.send(self.wikipedia_page.url)

    @quiz_wikipedia.command(aliases=['find', 'page'])
    async def get_wikipedia_page(self, ctx, target_word: str):
        """指定した単語のwikipediaページを取得する"""
        self.wikipedia_page = wikipedia.page(target_word)

    @quiz_wikipedia.command(aliases=['content'])
    async def get_content(self, ctx):
        await ctx.send(self.wikipedia_page.content)

    @quiz_wikipedia.command(aliases=['hint'])
    async def print_hint(self, ctx, key: str):
        if key == "wo1":
            await ctx.send("妹「一文字目は「" + self.wikipedia_page.title[0] + "」だよ！」")
        if key == "se2":
            se2 = self.wikipedia_page.summary
            s1 = se2.find("\n")
            se2 = se2[s1: se2.find("\n", s1 + 1)]
            se2 = self.do_hide_words(se2)
            await ctx.send("妹「サマリーの二行目は\n「" + se2 + "\n」だよ！」")
