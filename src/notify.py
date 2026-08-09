# -*- coding: utf-8 -*-
"""通知模块：WxPusher 微信推送 + 邮件发送"""

import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

try:
    from urllib.request import Request, urlopen
    from urllib.error import URLError
except ImportError:
    from urllib2 import Request, urlopen, URLError


def send_wxpusher(title, content, content_type=1):
    """通过 WxPusher 推送到微信。

    Args:
        title: 消息摘要/标题
        content: 消息正文
        content_type: 1=纯文本, 2=HTML, 3=Markdown

    需要环境变量:
        WX_PUSHER_APP_TOKEN: WxPusher 应用的 AppToken
        WX_PUSHER_UID: 接收用户的 UID (多个用逗号分隔)
    """
    app_token = os.environ.get("WX_PUSHER_APP_TOKEN", "")
    uid_str = os.environ.get("WX_PUSHER_UID", "")

    if not app_token or not uid_str:
        print("[WxPusher] 未配置 WX_PUSHER_APP_TOKEN 或 WX_PUSHER_UID，跳过推送")
        return False

    uids = [u.strip() for u in uid_str.split(",") if u.strip()]
    if not uids:
        print("[WxPusher] UID 列表为空，跳过推送")
        return False

    payload = json.dumps({
        "appToken": app_token,
        "content": content,
        "contentType": content_type,
        "uids": uids,
        "summary": title[:100],
    }).encode("utf-8")

    req = Request(
        "https://wxpusher.zjiecode.com/api/send/message",
        data=payload,
        headers={"Content-Type": "application/json"},
    )

    try:
        resp = urlopen(req, timeout=15)
        result = json.loads(resp.read().decode("utf-8"))
        if result.get("code") == 1000:
            print(f"[WxPusher] 推送成功: {result.get('msg', 'OK')}")
            return True
        else:
            print(f"[WxPusher] 推送失败: {result}")
            return False
    except URLError as e:
        print(f"[WxPusher] 网络错误: {e}")
        return False
    except Exception as e:
        print(f"[WxPusher] 异常: {e}")
        return False


def send_email(subject, body_html, body_text=""):
    """通过 SMTP 发送邮件 (默认使用 QQ 邮箱)。

    需要环境变量:
        SMTP_HOST: SMTP 服务器 (默认 smtp.qq.com)
        SMTP_PORT: SMTP 端口 (默认 587)
        SMTP_USER: 发件邮箱地址
        SMTP_PASS: SMTP 授权码 (非邮箱密码)
        SMTP_TO: 收件邮箱地址
    """
    smtp_host = os.environ.get("SMTP_HOST", "smtp.qq.com")
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))
    smtp_user = os.environ.get("SMTP_USER", "")
    smtp_pass = os.environ.get("SMTP_PASS", "")
    smtp_to = os.environ.get("SMTP_TO", "")

    if not smtp_user or not smtp_pass or not smtp_to:
        print("[Email] 未配置 SMTP 凭证，跳过邮件发送")
        return False

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = smtp_user
    msg["To"] = smtp_to

    if body_text:
        msg.attach(MIMEText(body_text, "plain", "utf-8"))
    msg.attach(MIMEText(body_html, "html", "utf-8"))

    try:
        server = smtplib.SMTP(smtp_host, smtp_port, timeout=15)
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail(smtp_user, [smtp_to], msg.as_string())
        server.quit()
        print(f"[Email] 邮件发送成功 -> {smtp_to}")
        return True
    except Exception as e:
        print(f"[Email] 发送失败: {e}")
        return False


def notify_daily_fortune(fortune_text, date_str=""):
    """发送每日运势通知 (WxPusher + 邮件)"""
    title = f"每日运势 | {date_str}" if date_str else "每日运势"

    # WxPusher 推送 (纯文本，微信消息长度有限制)
    wx_content = fortune_text[:600]  # 截取前 600 字
    if len(fortune_text) > 600:
        wx_content += "\n\n...（内容过长已截断，完整版见 GitHub）"
    send_wxpusher(title, wx_content, content_type=1)

    # 邮件发送 (HTML 格式，完整内容)
    html_body = fortune_text.replace("\n", "<br>")
    html = f"""<html><body style="font-family: sans-serif; max-width: 600px; margin: 0 auto;">
<h2>{title}</h2>
<pre style="white-space: pre-wrap; font-family: inherit; line-height: 1.8;">{html_body}</pre>
<hr>
<p style="color: #999; font-size: 12px;">由 GitHub Actions 自动生成，仅供娱乐参考</p>
</body></html>"""
    send_email(f"每日运势 | {date_str}", html, body_text=fortune_text)


def notify_workflow_status(success, detail=""):
    """发送工作流运行状态通知"""
    if success:
        title = "运势生成成功"
        content = f"今日运势已自动生成并推送到仓库。{detail}"
    else:
        title = "运势生成失败"
        content = f"今日运势生成过程中出现错误。{detail}"

    send_wxpusher(title, content, content_type=1)
