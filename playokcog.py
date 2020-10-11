from selenium import webdriver
import time

user_id = "tako2"
password = "xxxxxx"

driver = webdriver.Chrome(
    executable_path="D:/workspaces/discordpy-startup/libs/chromedriver_win32/chromedriver.exe")

# # 1.Webサイトにアクセスする
driver.get('https://www.playok.com/ja/go/')

# 3. ログイン情報を入力してログインする
tag = driver.find_element_by_xpath(
    '/html/body/div[2]/div[1]/div/table/tbody/tr/td[1]/button')
tag.click()
u = driver.find_element_by_name('username')
u.send_keys(user_id)
p = driver.find_element_by_name('pw')
p.send_keys(password)
p.submit()
time.sleep(1)

tag = driver.find_element_by_xpath('//*[@id="bast"]/p[1]/button')
tag.click()

handle_array = driver.window_handles
driver.switch_to.window(handle_array[-1])
time.sleep(3)
print(driver.current_url)

# 6. 「テーブル作成」ボタンを押下する
# tag = driver.find_element_by_xpath(
# '//*[@id="appcont"]/div[1]/div[1]/div[1]/button')
tag = driver.find_element_by_xpath(
    '/html/body/div/div[1]/div[1]/div[1]/button')
tag.click()
time.sleep(1)
