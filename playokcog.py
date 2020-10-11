import discord
from discord.ext import commands
import time
from selenium.webdriver import Chrome, ChromeOptions


class PlayokCog(commands.Cog):

    USER_ID = "tako2"
    PASSWORD = "qweasd11"

    @commands.group(aliases=['playok', 'po', 'ok'])
    async def playOK(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(
                title="playOKについて",
                description="playOKについて"
            )

            embed.add_field(
                name="create_room", value="部屋の作成\n        e.ok cr 将棋", inline=False)

            await ctx.send(embed=embed)

    @playOK.command(aliases=['create_room', 'cr'])
    async def create_playing_room(self, ctx, event: str):
        """
        PlayOKに自動ログインして、テーブル作成を実施して、部屋のURLを返す機能

        ログインID, ログインパスワードは、作成者:worldyのものを使用する。
        """

        options = ChromeOptions()
        # ヘッドレスモードを有効にする（次の行をコメントアウトすると画面が表示される）。
        options.add_argument('--headless')
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
