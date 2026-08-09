# -*- coding: utf-8 -*-
"""干支系统：天干、地支、五行、纳音等基础数据与计算"""

import sys

# 十天干
TIAN_GAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]

# 十二地支
DI_ZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

# 五行: 0=木, 1=火, 2=土, 3=金, 4=水
WU_XING = ["木", "火", "土", "金", "水"]

# 天干对应的五行索引
GAN_WUXING = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]

# 地支对应的五行索引
ZHI_WUXING = [4, 2, 0, 0, 2, 1, 1, 2, 3, 3, 2, 4]

# 天干阴阳 (0=阴, 1=阳)
GAN_YINYANG = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0]

# 地支阴阳
ZHI_YINYANG = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]

# 地支藏干
ZHI_CANGGAN = {
    "子": [(9, 1.0)],
    "丑": [(5, 0.6), (9, 0.3), (7, 0.1)],
    "寅": [(0, 0.6), (2, 0.3), (4, 0.1)],
    "卯": [(1, 1.0)],
    "辰": [(4, 0.6), (1, 0.3), (9, 0.1)],
    "巳": [(2, 0.6), (4, 0.3), (6, 0.1)],
    "午": [(3, 0.6), (5, 0.4)],
    "未": [(5, 0.6), (3, 0.3), (1, 0.1)],
    "申": [(6, 0.6), (9, 0.3), (4, 0.1)],
    "酉": [(7, 1.0)],
    "戌": [(4, 0.6), (7, 0.3), (3, 0.1)],
    "亥": [(8, 0.6), (0, 0.4)],
}

# 天干五合
GAN_HE = {
    (0, 5): 2, (5, 0): 2,
    (1, 6): 3, (6, 1): 3,
    (2, 7): 4, (7, 2): 4,
    (3, 8): 0, (8, 3): 0,
    (4, 9): 1, (9, 4): 1,
}

# 地支六合
ZHI_HE = {
    (0, 1): 2, (1, 0): 2,
    (2, 11): 0, (11, 2): 0,
    (3, 10): 1, (10, 3): 1,
    (4, 9): 3, (9, 4): 3,
    (5, 8): 4, (8, 5): 4,
    (6, 7): 2, (7, 6): 2,
}

# 地支六冲
ZHI_CHONG = {
    0: 6, 6: 0,
    1: 7, 7: 1,
    2: 8, 8: 2,
    3: 9, 9: 3,
    4: 10, 10: 4,
    5: 11, 11: 5,
}

# 地支相害
ZHI_HAI = {
    0: 7, 7: 0,
    1: 6, 6: 1,
    2: 5, 5: 2,
    3: 4, 4: 3,
    8: 11, 11: 8,
    9: 10, 10: 9,
}

# 地支相刑
ZHI_XING = {
    0: 3, 3: 0,
    2: 5, 5: 8, 8: 2,
    1: 10, 10: 7, 7: 1,
}

ZHI_ZIXING = {4, 6, 9, 11}

# 三合局
SAN_HE = {
    frozenset({8, 0, 4}): 4,
    frozenset({11, 3, 7}): 0,
    frozenset({2, 6, 10}): 1,
    frozenset({5, 9, 1}): 3,
}

# 六十甲子
JIAZI = [f"{TIAN_GAN[i%10]}{DI_ZHI[i%12]}" for i in range(60)]

# 纳音五行
NAYIN = [
    3, 3, 1, 1, 2, 2,
    2, 2, 4, 4, 2, 2,
    4, 4, 2, 2, 0, 0,
    3, 3, 1, 1, 4, 4,
    1, 1, 0, 0, 3, 3,
    3, 3, 2, 2, 0, 0,
    2, 2, 4, 4, 2, 2,
    4, 4, 2, 2, 0, 0,
    3, 3, 1, 1, 4, 4,
    1, 1, 0, 0, 3, 3,
]

# 节气日期表
JIEQI = [
    (1, 6, "小寒"), (1, 20, "大寒"),
    (2, 4, "立春"), (2, 19, "雨水"),
    (3, 6, "惊蛰"), (3, 21, "春分"),
    (4, 5, "清明"), (4, 20, "谷雨"),
    (5, 6, "立夏"), (5, 21, "小满"),
    (6, 6, "芒种"), (6, 22, "夏至"),
    (7, 7, "小暑"), (7, 23, "大暑"),
    (8, 7, "立秋"), (8, 23, "处暑"),
    (9, 8, "白露"), (9, 23, "秋分"),
    (10, 8, "寒露"), (10, 24, "霜降"),
    (11, 7, "立冬"), (11, 22, "小雪"),
    (12, 7, "大雪"), (12, 22, "冬至"),
]

# 节对应的地支月
JIE_ZHI_MAP = {
    "立春": 2, "惊蛰": 3, "清明": 4, "立夏": 5,
    "芒种": 6, "小暑": 7, "立秋": 8, "白露": 9,
    "寒露": 10, "立冬": 11, "大雪": 0, "小寒": 1,
}

# 年干确定月干起始: 甲己之年丙作首
YEAR_GAN_TO_MONTH_START = {0: 2, 5: 2, 1: 4, 6: 4, 2: 6, 7: 6, 3: 8, 8: 8, 4: 0, 9: 0}


def get_shishen(ri_gan_idx, other_gan_idx):
    """十神计算。
    五行关系 (other - ri) % 5:
      0: 同我(比劫)  1: 我生(食伤)  2: 我克(财)
      3: 克我(官杀)  4: 生我(印)
    """
    if ri_gan_idx == other_gan_idx:
        return "日主"
    ri_wx = GAN_WUXING[ri_gan_idx]
    other_wx = GAN_WUXING[other_gan_idx]
    same_yy = GAN_YINYANG[ri_gan_idx] == GAN_YINYANG[other_gan_idx]
    rel = (other_wx - ri_wx) % 5

    if rel == 0:
        return "比肩" if same_yy else "劫财"
    elif rel == 1:
        return "食神" if same_yy else "伤官"
    elif rel == 2:
        return "偏财" if same_yy else "正财"
    elif rel == 3:
        return "七杀" if same_yy else "正官"
    else:  # rel == 4
        return "偏印" if same_yy else "正印"


def get_gan_index(gan_char):
    return TIAN_GAN.index(gan_char)


def get_zhi_index(zhi_char):
    return DI_ZHI.index(zhi_char)


def get_wuxing_name(wx_idx):
    return WU_XING[wx_idx]


def get_day_ganzhi(year, month, day):
    """计算日干支 (基于基准日期推算)"""
    from datetime import date as dt_date
    base = dt_date(1900, 1, 1)
    target = dt_date(year, month, day)
    delta = (target - base).days
    jiazi_idx = (10 + delta) % 60
    return TIAN_GAN[jiazi_idx % 10] + DI_ZHI[jiazi_idx % 12]


def get_year_ganzhi(year):
    gan_idx = (year - 4) % 10
    zhi_idx = (year - 4) % 12
    return TIAN_GAN[gan_idx] + DI_ZHI[zhi_idx]


def get_month_ganzhi(year, month, day):
    """计算月干支 (基于节气划分)"""
    target_val = month * 100 + day
    jieqi_vals = [(m * 100 + d, name) for m, d, name in JIEQI]

    jie_name = None
    for i, (val, name) in enumerate(jieqi_vals):
        if target_val < val:
            if i == 0:
                jie_name = "大雪"
            else:
                jie_name = jieqi_vals[i - 1][1]
                if jie_name not in JIE_ZHI_MAP:
                    if i - 2 >= 0:
                        jie_name = jieqi_vals[i - 2][1]
                    else:
                        jie_name = "大雪"
            break
    if jie_name is None:
        jie_name = "大雪"

    zhi_idx = JIE_ZHI_MAP[jie_name]
    zhi_char = DI_ZHI[zhi_idx]

    if target_val < 204:
        lichun_year = year - 1
    else:
        lichun_year = year

    year_gan_idx = (lichun_year - 4) % 10
    start_gan = YEAR_GAN_TO_MONTH_START[year_gan_idx]
    month_seq = (zhi_idx - 2) % 12
    gan_idx = (start_gan + month_seq) % 10
    gan_char = TIAN_GAN[gan_idx]

    return gan_char + zhi_char


def get_hour_ganzhi(day_gan, hour):
    """计算时柱"""
    day_gan_idx = TIAN_GAN.index(day_gan)
    shichen_index = ((hour + 1) // 2) % 12
    zhi_char = DI_ZHI[shichen_index]

    day_groups = {0: 0, 5: 0, 1: 2, 6: 2, 2: 4, 7: 4, 3: 6, 8: 6, 4: 8, 9: 8}
    start_gan = day_groups[day_gan_idx]
    gan_idx = (start_gan + shichen_index) % 10
    gan_char = TIAN_GAN[gan_idx]

    return gan_char + zhi_char


def get_full_bazi(year, month, day, hour):
    """计算完整八字四柱"""
    return {
        "年柱": get_year_ganzhi(year),
        "月柱": get_month_ganzhi(year, month, day),
        "日柱": get_day_ganzhi(year, month, day),
        "时柱": get_hour_ganzhi(get_day_ganzhi(year, month, day)[0], hour),
    }
