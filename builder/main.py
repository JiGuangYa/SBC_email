from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import datetime
import os
import argparse

# 创建一个解析器
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--username', type=str, required=True, help='邮箱账号')
parser.add_argument('--password', type=str, required=True, help='邮箱密码')
parser.add_argument('--email_file', type=str,
                    default='emails.txt', help='保存邮件信息的文件')
parser.add_argument('--last_check_time_file', type=str,
                    default='last_check_time.txt', help='保存上一次检查邮件的时间的文件')
parser.add_argument('--forward_email', type=str, required=True, help='转发的邮箱地址')

# 解析命令行参数
args = parser.parse_args()

# 使用命令行参数作为全局变量
USERNAME = args.username
PASSWORD = args.password
EMAIL_FILE = args.email_file
LAST_CHECK_TIME_FILE = args.last_check_time_file
FORWARD_EMAIL = args.forward_email

# 创建一个文件来保存邮件信息
if not os.path.exists(EMAIL_FILE):
    with open(EMAIL_FILE, 'a') as f:
        f.write('Receive Time\n')

# 保存上一次检查邮件的时间
if os.path.exists(LAST_CHECK_TIME_FILE):
    with open(LAST_CHECK_TIME_FILE, 'r') as f:
        content = f.read()
        if content:
            last_check_time = datetime.datetime.strptime(
                content, '%Y-%m-%d %H:%M:%S')
        else:
            last_check_time = datetime.datetime.now()
else:
    last_check_time = datetime.datetime.now()


def convert_time(receive_time):
    now = datetime.datetime.now()
    if '昨天' in receive_time:
        date = now - datetime.timedelta(days=1)
        time = datetime.datetime.strptime(
            receive_time.split(', ')[1], '%H:%M').time()
    elif '今天' in receive_time:
        date = now
        time = datetime.datetime.strptime(
            receive_time.split(', ')[1], '%H:%M').time()
    else:
        weekday_dict = {'周一': 0, '周二': 1, '周三': 2,
                        '周四': 3, '周五': 4, '周六': 5, '周日': 6}
        weekday = receive_time.split(', ')[0]
        days_ago = (now.weekday() - weekday_dict[weekday]) % 7
        date = now - datetime.timedelta(days=days_ago)
        time = datetime.datetime.strptime(
            receive_time.split(', ')[1], '%H:%M').time()
    return datetime.datetime.combine(date, time)


def check_mail():
    global last_check_time
    # 设置FirefoxDriver 默认采用火狐浏览器
    driver = webdriver.Firefox()

    # 打开邮箱登录页面
    driver.get("https://mail.sbc.usst.edu.cn/")
    time.sleep(1)

    # 输入用户名和密码（根据您的页面元素ID修改）
    username_box = driver.find_element(By.ID, "username")
    password_box = driver.find_element(By.ID, "password")
    username_box.send_keys(USERNAME)
    password_box.send_keys(PASSWORD)

    # 点击登录按钮（根据您的页面元素ID修改）
    login_button = driver.find_element(By.CLASS_NAME, "signinTxt")
    login_button.click()
    time.sleep(1)

    while True:

        # 从这里开始编写检查邮件的逻辑
        latest_email = driver.find_element(
            By.ID, "_ariaId_27")
        latest_email.click()
        time.sleep(1)

        # 获取收信人
        sender = driver.find_element(By.CLASS_NAME, "bidi.allowTextSelection")
        sender_text = sender.text
        print("Sender:", sender_text)
        time.sleep(1)

        # 获取收件时间
        receive_time = driver.find_element(
            By.XPATH, "//*[@id='primaryContainer']/div[5]/div/div[1]/div/div[5]/div[3]/div/div[5]/div[1]/div/div[1]/div[4]/div[2]/div[5]/div[2]/div[1]/div[2]/div[1]/div[1]/div/div[2]/div[3]/div/div[1]/div[1]/span").text
        print("Receive Time:", receive_time)
        time.sleep(1)

        # 将收件时间转换为datetime对象
        receive_time = convert_time(receive_time)

        # 打印出receive_time和last_check_time的值
        print(f'receive_time: {receive_time}, last_check_time: {
              last_check_time}')

        # 判断是否有新邮件
        if receive_time != last_check_time:
            # 将新的收件时间写入文件
            with open(EMAIL_FILE, 'a', encoding='utf-8-sig') as f:
                f.write(f'{receive_time}\n')

            # 更新上一次检查邮件的时间
            last_check_time = receive_time
            with open(LAST_CHECK_TIME_FILE, 'w') as f:
                f.write(str(last_check_time))
            time.sleep(1)

            extra_button = driver.find_element(
                By.XPATH, "/html/body/div[2]/div/div[3]/div[5]/div/div[1]/div/div[5]/div[3]/div/div[5]/div[1]/div/div[1]/div[4]/div[2]/div[5]/div[2]/div[1]/div[2]/div[1]/div[1]/div/div[2]/div[2]/div[1]/div[4]/button[4]/span[1]")
            extra_button.click()
            time.sleep(1)

            forword_button = driver.find_element(
                By.XPATH, "/html/body/div[12]/div/div/div/div/div[3]/button/div/span[2]")
            forword_button.click()
            time.sleep(1)

            receiver_mail = driver.find_element(
                By.XPATH, "/html/body/div[2]/div/div[3]/div[5]/div/div[1]/div/div[5]/div[3]/div/div[5]/div[1]/div/div[3]/div[4]/div/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div/div/div/span/div[1]/form/input")
            receiver_mail.send_keys(FORWARD_EMAIL)
            time.sleep(2)

            send_button = driver.find_element(
                By.XPATH, "/html/body/div[2]/div/div[3]/div[5]/div/div[1]/div/div[5]/div[3]/div/div[5]/div[1]/div/div[3]/div[5]/div/div[2]/div[1]/button[1]")
            driver.execute_script(
                "arguments[0].scrollIntoView();", send_button)
            send_button.click()
            print("Email has been sent")
            time.sleep(1)

        else:
            print("No new email")
            time.sleep(1)
        # 刷新页面
        print("Refreshing the page")
        driver.refresh()
        time.sleep(1)

        # 暂停5分钟
        print("Waiting for 5 minutes")
        time.sleep(300)


if __name__ == "__main__":
    check_mail()
