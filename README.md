# 每日运势 GitHub Action

基于八字命理和五行分析的每日运势自动生成工具。

## 功能

- 自动计算个人八字命盘（四柱：年、月、日、时）
- 每日自动分析当日干支与命局的交互关系
- 从事业、财运、感情、健康等维度生成运势分析
- 提供宜做/不宜做建议和开运锦囊
- 通过 GitHub Actions 每日自动运行

## 项目结构

```
每日运势/
├── .github/workflows/daily-fortune.yml   # GitHub Actions 工作流
├── src/
│   ├── ganzhi.py    # 干支计算引擎（天干地支、五行、纳音）
│   ├── bazi.py      # 八字命盘分析与交互计算
│   └── fortune.py   # 运势生成引擎
├── main.py          # 主程序入口
├── output/          # 生成的运势文件
└── requirements.txt # 依赖（仅 Python 标准库，无需额外安装）
```

## 本地运行

```bash
# 无需安装任何依赖，直接运行
python main.py
```

## 配置个人命盘

编辑 `main.py` 中的以下变量：

```python
BIRTH_YEAR = 2000
BIRTH_MONTH = 1
BIRTH_DAY = 21
BIRTH_HOUR = 5      # 24小时制
GENDER = "男"
BIRTH_PLACE = "广东省潮州市潮安区"
CURRENT_PLACE = "广东省肇庆市高要区"
```

## GitHub Actions 设置

1. 将本项目推送到 GitHub 仓库
2. 在仓库 Settings → Actions → General → Workflow permissions 中，选择 "Read and write permissions"
3. 工作流默认每天早上 7:00（北京时间）自动运行
4. 也可以在 Actions 页面手动触发

## 说明

本项目的干支计算和八字排盘基于传统命理算法实现，运势解读为程式化生成，仅供娱乐参考。

## License

MIT
