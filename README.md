# 每日运势 GitHub Action

基于八字命理和五行分析的每日运势自动生成工具，支持 WxPusher 微信推送和邮件通知。

## 功能

- 自动计算个人八字命盘（四柱：年、月、日、时）
- 每日自动分析当日干支与命局的交互关系
- 从事业、财运、感情、健康等维度生成运势分析
- 通过 WxPusher 推送到微信 + 邮件发送
- 通过 GitHub Actions 每日自动运行

## 项目结构

```
每日运势/
├── .github/workflows/daily-fortune.yml   # GitHub Actions 工作流
├── src/
│   ├── ganzhi.py    # 干支计算引擎
│   ├── bazi.py      # 八字命盘分析
│   ├── fortune.py   # 运势生成引擎
│   └── notify.py    # 通知模块 (WxPusher + 邮件)
├── main.py          # 主程序入口
├── output/          # 生成的运势文件
└── requirements.txt # 依赖（仅 Python 标准库）
```

## 配置个人命盘

编辑 `main.py` 中的变量：

```python
BIRTH_YEAR = 2000
BIRTH_MONTH = 1
BIRTH_DAY = 21
BIRTH_HOUR = 5
GENDER = "男"
```

## 配置通知

### WxPusher 微信推送

1. 访问 [wxpusher.zjiecode.com](https://wxpusher.zjiecode.com) 注册登录
2. 创建应用，获取 **AppToken**
3. 扫码关注应用，获取你的 **UID**
4. 在 GitHub 仓库 Settings → Secrets and variables → Actions 中添加：
   - `WX_PUSHER_APP_TOKEN`: 你的 AppToken
   - `WX_PUSHER_UID`: 你的 UID（多个用英文逗号分隔）

### 邮件通知 (QQ 邮箱示例)

1. 登录 QQ 邮箱 → 设置 → 账户 → 开启 SMTP 服务，获取**授权码**
2. 在 GitHub Secrets 中添加：
   - `SMTP_HOST`: `smtp.qq.com`
   - `SMTP_PORT`: `587`
   - `SMTP_USER`: 你的 QQ 邮箱地址
   - `SMTP_PASS`: SMTP 授权码（不是邮箱密码）
   - `SMTP_TO`: 接收运势的邮箱地址

## GitHub Actions 设置

1. 仓库 Settings → Actions → General → Workflow permissions → Read and write permissions
2. 默认每天北京时间 7:00 自动运行
3. 可在 Actions 页面手动触发

## 本地运行

```bash
python main.py
```

本地运行不会发送通知。

## License

MIT
