import time
from selenium.webdriver import Chrome, ChromeOptions

options = ChromeOptions()
# ヘッドレスモードを有効にする（次の行をコメントアウトすると画面が表示される）。
options.add_argument('--headless')
# ChromeのWebDriverオブジェクトを作成する。
driver = Chrome(options=options)

user_id = "tako2"
password = "xxxxxx"

# 1.Webサイトにアクセスする
driver.get('https://www.playok.com/ja/go/')

# 2. ログイン情報を入力してログインする
tag = driver.find_element_by_xpath(
    '/html/body/div[2]/div[1]/div/table/tbody/tr/td[1]/button')
tag.click()
u = driver.find_element_by_name('username')
u.send_keys(user_id)
p = driver.find_element_by_name('pw')
p.send_keys(password)
p.submit()
time.sleep(1)

# 3. 「スタート - 碁」ボタンを押下する
tag = driver.find_element_by_xpath('//*[@id="bast"]/p[1]/button')
tag.click()

handle_array = driver.window_handles
driver.switch_to.window(handle_array[-1])
time.sleep(3)

# 4. 「テーブル作成」ボタンを押下する
tag = driver.find_element_by_xpath(
    '/html/body/div/div[1]/div[1]/div[1]/button')
tag.click()
time.sleep(1)

# 5. 現在のURLを出力
print(driver.current_url)
