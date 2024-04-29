from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time


def check_mail():
    # 设置ChromeDriver
    driver = webdriver.Firefox()
    # service=Service(ChromeDriverManager().install()))

    try:
        # 打开邮箱登录页面
        driver.get("https://mail.sbc.usst.edu.cn/")

        # 根据实际情况调整等待时间，确保页面元素加载完毕
        time.sleep(2)

        # 输入用户名和密码（根据您的页面元素ID修改）
        username_box = driver.find_element(By.ID, "username")
        password_box = driver.find_element(By.ID, "password")
        username_box.send_keys("SBC-23-8052")
        password_box.send_keys("Aa283013")

        # 点击登录按钮（根据您的页面元素ID修改）
        login_button = driver.find_element(By.CLASS_NAME, "signinTxt")
        login_button.click()

        # 等待登录完毕
        time.sleep(3)

        # 从这里开始编写检查邮件的逻辑
        # 例如，查找有无新邮件的标志、读取邮件标题等
        # 下面的代码需要根据您的邮箱页面结构进行调整
        # 示例：找到并打印所有邮件的标题
        latest_email = driver.find_elements(
            By.ID, "_ariaId_27")
        latest_email.click()
        # emails = driver.find_elements(
        #     By.ID, "_lvv_g")  # 假定邮件标题有特定的class name
        # for email in emails:
        #     print(email.text, email.is_displayed())
        time.sleep(1)

    finally:
        # 关闭浏览器
        driver.quit()


if __name__ == "__main__":
    check_mail()
