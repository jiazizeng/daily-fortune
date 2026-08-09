# -*- coding: utf-8 -*-
"""每日运势生成主程序 - 作为 GitHub Action 运行或本地手动执行"""

import os
import sys
from datetime import date

# 添加 src 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from bazi import BaziChart
from fortune import generate_fortune


def main():
    # 用户命盘信息
    BIRTH_YEAR = 2000
    BIRTH_MONTH = 1
    BIRTH_DAY = 21
    BIRTH_HOUR = 5
    GENDER = "男"
    BIRTH_PLACE = "广东省潮州市潮安区"
    CURRENT_PLACE = "广东省肇庆市高要区"

    print("=" * 50)
    print("  每日运势生成器")
    print(f"  命主：{GENDER} | 出生：{BIRTH_YEAR}年{BIRTH_MONTH}月{BIRTH_DAY}日 {BIRTH_HOUR}:00")
    print(f"  出生地：{BIRTH_PLACE}")
    print(f"  现居地：{CURRENT_PLACE}")
    print("=" * 50)
    print()

    # 计算命盘
    print("[1/3] 计算本命八字...")
    chart = BaziChart(BIRTH_YEAR, BIRTH_MONTH, BIRTH_DAY, BIRTH_HOUR, GENDER)
    print(f"  八字：{chart.bazi['年柱']} {chart.bazi['月柱']} {chart.bazi['日柱']} {chart.bazi['时柱']}")
    print(f"  日主：{chart.ri_wuxing}（{chart.ri_gan}）")
    print(f"  日主状态：{chart.xiyong['日主状态']}")
    print()

    # 确定目标日期
    if len(sys.argv) > 1 and sys.argv[1] == "--yesterday":
        target = date.today()
        target = (target.year, target.month, target.day - 1 if target.day > 1 else target.day)
    else:
        today = date.today()
        target = (today.year, today.month, today.day)

    print(f"[2/3] 分析 {target[0]}年{target[1]}月{target[2]}日 运势...")
    fortune_text = generate_fortune(chart, target)
    print()

    # 输出
    print("[3/3] 生成运势报告...")

    # 输出目录
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    os.makedirs(output_dir, exist_ok=True)

    # 保存为当日运势文件
    filename = f"fortune_{target[0]}_{target[1]:02d}_{target[2]:02d}.md"
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(fortune_text)
    print(f"  已保存: {filepath}")

    # 同时更新最新运势文件
    latest_path = os.path.join(output_dir, "latest.md")
    with open(latest_path, "w", encoding="utf-8") as f:
        f.write(fortune_text)
    print(f"  已更新: {latest_path}")

    # 打印到控制台
    print()
    print(fortune_text)

    print("=" * 50)
    print("  运势生成完成！")
    print("=" * 50)


if __name__ == "__main__":
    main()
