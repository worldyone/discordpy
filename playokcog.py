import discord
from discord.ext import commands
import time
from selenium.webdriver import Chrome, ChromeOptions
import requests
from bs4 import BeautifulSoup as bs4


class PlayokCog(commands.Cog):

    USER_ID = "tako2"
    PASSWORD = "xxxxxxxx"

    GROUP_MEMBER = ["tako2", "mto2415", "snpc94"]

    @commands.group(aliases=['playok', 'po', 'ok'])
    async def playOK(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(
                title="playOKについて",
                description="playOKについて"
            )

            embed.add_field(
                name="create_room", value="部屋の作成\n        e.ok cr 将棋", inline=False)
            embed.add_field(
                name="get_result", value="個人の対局結果の取得\n        e.ok gr {name}", inline=False)
            embed.add_field(
                name="results", value="グループメンバの対局結果の取得\n        e.ok results", inline=False)

            await ctx.send(embed=embed)

    @playOK.command(aliases=['create_room', 'cr'])
    async def create_playing_room(self, ctx, event: str):
        """
        # todo 未完成というか止めた方が良い気がしてきてる。そもそも相手側のログインが難しい。
        PlayOKに自動ログインして、テーブル作成を実施して、部屋のURLを返す機能

        ログインID, ログインパスワードは、作成者:worldyのものを使用する。
        """

        options = ChromeOptions()
        # ヘッドレスモードを有効にする
        # options.add_argument('--headless')
        # ChromeのWebDriverオブジェクトを作成する。
        driver = Chrome(options=options)

        # Webサイトにアクセスする
        if event in ["碁", "囲碁", "go"]:
            await ctx.send("妹「囲碁の部屋を作成するね！」")
            path = 'https://www.playok.com/ja/go/'
        elif event in ["将棋", "shogi"]:
            await ctx.send("妹「将棋の部屋を作成するね！」")
            path = 'https://www.playok.com/ja/shogi/'
        elif event in ["オセロ", "リバーシ", "othello", "reversi"]:
            await ctx.send("妹「オセロの部屋を作成するね！」")
            path = 'https://www.playok.com/ja/reversi/'
        else:
            # 「囲碁・将棋・オセロ」の中から選んでね！」
            await ctx.send("妹「囲碁・将棋・オセロ」の中から選んでね！」")
            return

        # driverの取得
        driver.get(path)

        # ログイン情報を入力してログインする
        tag = driver.find_element_by_xpath(
            '/html/body/div[2]/div[1]/div/table/tbody/tr/td[1]/button')
        tag.click()
        u = driver.find_element_by_name('username')
        u.send_keys(self.USER_ID)
        p = driver.find_element_by_name('pw')
        p.send_keys(self.PASSWORD)
        p.submit()
        time.sleep(3)

        # 「スタート - {イベント名}」ボタンを押下する
        tag = driver.find_element_by_xpath('//*[@id="bast"]/p[1]/button')
        tag.click()

        handle_array = driver.window_handles
        driver.switch_to.window(handle_array[-1])
        time.sleep(5)

        # 「テーブル作成」ボタンを押下する
        tag = driver.find_element_by_xpath(
            '/html/body/div/div[1]/div[1]/div[1]/button')
        tag.click()
        time.sleep(3)

        # 作成した部屋のURLを返す
        await ctx.send(driver.current_url)

    @playOK.command(aliases=["gr"])
    async def get_results(self, ctx, player_name: str = ""):
        """個人の対局結果を取得する"""

        if player_name == "":
            player_name = self.USER_ID
        go_results = self.get_format_url_by_event("go", player_name, 2)
        sg_results = self.get_format_url_by_event("sg", player_name, 2)
        rv_results = self.get_format_url_by_event("rv", player_name, 2)

        message_results = ""
        for info, url in go_results:
            message_results += "囲碁  " + info + "\n" + url + "\n\n"
        for info, url in sg_results:
            message_results += "将棋  " + info + "\n" + url + "\n\n"
        for info, url in rv_results:
            message_results += "オセロ  " + info + "\n" + url + "\n\n"
        await ctx.send(message_results)

    @playOK.command(aliases=["results"])
    async def get_group_results(self, ctx):
        """グループメンバの対局結果を取得する"""

        go_results = self.get_format_url_by_event(
            "go", self.GROUP_MEMBER[0], 2)
        go_results += self.get_format_url_by_event(
            "go", self.GROUP_MEMBER[1], 2)
        sg_results = self.get_format_url_by_event(
            "sg", self.GROUP_MEMBER[0], 2)
        sg_results += self.get_format_url_by_event(
            "sg", self.GROUP_MEMBER[1], 2)
        rv_results = self.get_format_url_by_event(
            "rv", self.GROUP_MEMBER[0], 2)
        rv_results += self.get_format_url_by_event(
            "rv", self.GROUP_MEMBER[1], 2)

        message_results = ""
        for info, url in go_results:
            if url not in message_results:
                message_results += "囲碁  " + info + " " + url + "\n"
        for info, url in sg_results:
            if url not in message_results:
                message_results += "将棋  " + info + " " + url + "\n"
        for info, url in rv_results:
            if url not in message_results:
                message_results += "オセロ  " + info + " " + url + "\n"

        await ctx.send(message_results)

    def get_format_url_by_event(self, event, player_name, n):
        """
        通算成績ページを開いて、対局結果のURLを取得する

        event: 競技名の略称
        player_name: 対局者の名前
        n: 取得する対局試合数（直近から数える）
        """
        url = f'https://www.playok.com/ja/stat.phtml?u={player_name}&g={event}&sk=2'
        page = requests.get(url)
        soup = bs4(page.content, 'lxml')
        a_tags = soup.find_all('a')
        results = []
        sp = 5 + (event == "rv")  # リンクを取得するにあたり、取得位置の補正
        for m in range(n):  # 直近n試合分
            players = a_tags[sp + m * 4].text + \
                " v.s. " + a_tags[sp + 1 + m * 4].text
            result_url = "https://www.playok.com" + \
                a_tags[sp + 2 + m * 4].get("href")
            results.append([players, result_url])

        return results

    @playOK.command(aliases=['shogi_kento', 'sk'])
    async def playOK_kento(self, ctx, url):
        """
        将棋の検討
        """

        # 指定されたplayOKの対局結果URLから棋譜を取得して、ki2の棋譜に変換する
        playok2ki2_url = 'https://shogi.zukeran.org/cgi-bin/playok2ki2.cgi'
        playok2ki2_kifu_url = playok2ki2_url + '?url=' + url
        page = requests.get(playok2ki2_kifu_url)
        soup = bs4(page.content, 'lxml')
        ki2_kifu = soup.text

        # 検討サイトを開く
        driver = Chrome()
        driver.get('https://www.shogi-extend.com/adapter')

        # 棋譜入力エリアに棋譜を入力する
        kifu_area = driver.find_element_by_xpath(
            '//*[@id="__layout"]/div/div/div/div/div/div[1]/div/textarea')
        kifu_area.send_keys(ki2_kifu)
