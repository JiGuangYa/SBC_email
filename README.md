# SBC_email
基于selenium实现的SBC邮箱自动转发给QQ邮箱（实现微信提醒）

请在main.py同目录下创建一个config.py文件

里面格式为:

```python
# 定义全局变量

USERNAME = "SBC-xx-xxxx"  # 邮箱账号

PASSWORD = "xxxxxx"  # 邮箱密码

EMAIL_FILE = 'emails.txt'  # 保存邮件信息

LAST_CHECK_TIME_FILE = 'last_check_time.txt'  # 保存上一次检查邮件的时间

FORWARD_EMAIL = "xxxxxxx@xxxxx.com"  # 转发的邮箱地址
```

