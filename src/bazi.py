# -*- coding: utf-8 -*-
"""八字命盘分析与交互计算"""

from ganzhi import (
    TIAN_GAN, DI_ZHI, WU_XING, GAN_WUXING, ZHI_WUXING,
    GAN_YINYANG, ZHI_YINYANG, ZHI_CANGGAN,
    GAN_HE, ZHI_HE, ZHI_CHONG, ZHI_HAI, ZHI_XING, ZHI_ZIXING, SAN_HE,
    get_shishen, get_gan_index, get_zhi_index, get_wuxing_name,
    get_full_bazi, get_day_ganzhi, get_year_ganzhi, get_month_ganzhi,
)


class BaziChart:
    """八字命盘"""

    def __init__(self, year, month, day, hour, gender="男"):
        self.gender = gender
        self.birth_year = year
        self.birth_month = month
        self.birth_day = day
        self.birth_hour = hour
        self.bazi = get_full_bazi(year, month, day, hour)

        self.nian_gan = self.bazi["年柱"][0]
        self.nian_zhi = self.bazi["年柱"][1]
        self.yue_gan = self.bazi["月柱"][0]
        self.yue_zhi = self.bazi["月柱"][1]
        self.ri_gan = self.bazi["日柱"][0]
        self.ri_zhi = self.bazi["日柱"][1]
        self.shi_gan = self.bazi["时柱"][0]
        self.shi_zhi = self.bazi["时柱"][1]

        self.ri_gan_idx = get_gan_index(self.ri_gan)
        self.ri_wuxing_idx = GAN_WUXING[self.ri_gan_idx]
        self.ri_wuxing = WU_XING[self.ri_wuxing_idx]

        self.shishen = self._calc_shishen()
        self.wuxing_power = self._calc_wuxing_power()
        self.strong_weak = self._eval_strong_weak()
        self.xiyong = self._calc_xiyong()

    def _calc_shishen(self):
        return {
            "年干": get_shishen(self.ri_gan_idx, get_gan_index(self.nian_gan)),
            "月干": get_shishen(self.ri_gan_idx, get_gan_index(self.yue_gan)),
            "时干": get_shishen(self.ri_gan_idx, get_gan_index(self.shi_gan)),
            "年支": [get_shishen(self.ri_gan_idx, g[0]) for g in ZHI_CANGGAN[self.nian_zhi]],
            "月支": [get_shishen(self.ri_gan_idx, g[0]) for g in ZHI_CANGGAN[self.yue_zhi]],
            "日支": [get_shishen(self.ri_gan_idx, g[0]) for g in ZHI_CANGGAN[self.ri_zhi]],
            "时支": [get_shishen(self.ri_gan_idx, g[0]) for g in ZHI_CANGGAN[self.shi_zhi]],
        }

    def _calc_wuxing_power(self):
        power = {wx: 0.0 for wx in WU_XING}
        gan_weights = [0.1, 0.3, 0.4, 0.2]
        gans = [self.nian_gan, self.yue_gan, self.ri_gan, self.shi_gan]
        for gan, w in zip(gans, gan_weights):
            wx_idx = GAN_WUXING[get_gan_index(gan)]
            power[WU_XING[wx_idx]] += w
        zhis = [self.nian_zhi, self.yue_zhi, self.ri_zhi, self.shi_zhi]
        for zhi in zhis:
            for gan_idx, ratio in ZHI_CANGGAN[zhi]:
                wx_idx = GAN_WUXING[gan_idx]
                power[WU_XING[wx_idx]] += ratio * 0.25
        return power

    def _eval_strong_weak(self):
        ri_power = self.wuxing_power[self.ri_wuxing]
        yue_zhi_wx = WU_XING[ZHI_WUXING[get_zhi_index(self.yue_zhi)]]
        de_yueling = (yue_zhi_wx == self.ri_wuxing)
        de_di = sum(1 for z in [self.nian_zhi, self.yue_zhi, self.ri_zhi, self.shi_zhi]
                    if ZHI_WUXING[get_zhi_index(z)] == GAN_WUXING[self.ri_gan_idx])
        sheng_count = sum(1 for key in ["年干", "月干", "时干"]
                          if self.shishen[key] in ("正印", "偏印"))
        score = ri_power * 2 + (1.5 if de_yueling else 0) + de_di * 0.5 + sheng_count * 0.3
        if score > 6: return "身强"
        elif score > 4: return "偏强"
        elif score > 2.5: return "中和"
        elif score > 1.5: return "偏弱"
        else: return "身弱"

    def _calc_xiyong(self):
        """喜用神/忌神。
        五行关系 (other - ri) % 5:
          0: 同我(比劫)  1: 我生(食伤)  2: 我克(财)
          3: 克我(官杀)  4: 生我(印)
        """
        sw = self.strong_weak
        ri = self.ri_wuxing_idx
        xiyong, ji = [], []

        if sw in ("身强", "偏强"):
            for wx_name in WU_XING:
                rel = (WU_XING.index(wx_name) - ri) % 5
                if rel == 3: xiyong.append((wx_name, "官杀", "压力即动力，规则和约束对你有利"))
                elif rel == 1: xiyong.append((wx_name, "食伤", "发挥才华，表达自我"))
                elif rel == 2: xiyong.append((wx_name, "财星", "求财的好时机"))
                if rel == 4: ji.append((wx_name, "印星", "避免过度依赖和保守"))
                elif rel == 0: ji.append((wx_name, "比劫", "注意竞争和资源分散"))
        else:
            for wx_name in WU_XING:
                rel = (WU_XING.index(wx_name) - ri) % 5
                if rel == 4: xiyong.append((wx_name, "印星", "学习充电，寻求贵人帮助"))
                elif rel == 0: xiyong.append((wx_name, "比劫", "团结合作，借助他人之力"))
                if rel == 1: ji.append((wx_name, "食伤", "避免过度消耗精力"))
                elif rel == 3: ji.append((wx_name, "官杀", "注意压力和过度承担"))
                elif rel == 2: ji.append((wx_name, "财星", "谨慎理财，量力而行"))

        return {"喜用神": xiyong, "忌神": ji, "日主状态": sw}


def analyze_daily_interaction(chart, target_date):
    """分析当日干支与命局的交互关系"""
    year, month, day = target_date

    day_gz = get_day_ganzhi(year, month, day)
    day_gan = day_gz[0]
    day_zhi = day_gz[1]

    day_gan_idx = get_gan_index(day_gan)
    day_zhi_idx = get_zhi_index(day_zhi)

    day_wx_idx = GAN_WUXING[day_gan_idx]
    day_wx = get_wuxing_name(day_wx_idx)

    day_shishen = get_shishen(chart.ri_gan_idx, day_gan_idx)

    interactions = []
    zhi_labels = [("年支", chart.nian_zhi), ("月支", chart.yue_zhi),
                  ("日支", chart.ri_zhi), ("时支", chart.shi_zhi)]

    for label, zhi in zhi_labels:
        zhi_idx = get_zhi_index(zhi)
        if ZHI_CHONG.get(day_zhi_idx) == zhi_idx:
            interactions.append(f"今日{day_zhi}与命局{label}{zhi}相冲，情绪波动较大，宜静不宜动")
        if ZHI_HE.get((day_zhi_idx, zhi_idx)):
            interactions.append(f"今日{day_zhi}与命局{label}{zhi}相合，人缘佳，诸事顺遂")
        if ZHI_HAI.get(day_zhi_idx) == zhi_idx:
            interactions.append(f"今日{day_zhi}与命局{label}{zhi}相害，注意口舌是非和小人")
        if ZHI_XING.get(day_zhi_idx) == zhi_idx or (day_zhi_idx == zhi_idx and day_zhi_idx in ZHI_ZIXING):
            interactions.append(f"今日{day_zhi}与命局{label}{zhi}相刑，注意健康和法律相关事务")

    gan_interactions = []
    for label, gan in [("年干", chart.nian_gan), ("月干", chart.yue_gan), ("时干", chart.shi_gan)]:
        g_idx = get_gan_index(gan)
        if GAN_HE.get((day_gan_idx, g_idx)):
            gan_interactions.append(f"今日{day_gan}与命局{label}{gan}相合，有贵人相助或合作机会")

    xiyong_wxs = [x[0] for x in chart.xiyong["喜用神"]]
    ji_wxs = [x[0] for x in chart.xiyong["忌神"]]

    if day_wx in xiyong_wxs:
        wx_impact = "有利"
        wx_detail = f"今日{day_wx}是您的喜用神，整体运势向好"
    elif day_wx in ji_wxs:
        wx_impact = "不利"
        wx_detail = f"今日{day_wx}是您的忌神，遇事宜谨慎行事"
    else:
        wx_impact = "中性"
        wx_detail = "今日五行与命局无特殊冲合，平稳度过"

    return {
        "日期": f"{year}年{month}月{day}日",
        "日干支": day_gz,
        "日干五行": day_wx,
        "十神": day_shishen,
        "五行影响": wx_impact,
        "五行分析": wx_detail,
        "地支交互": interactions,
        "天干交互": gan_interactions,
    }
