# -*- coding: utf-8 -*-
"""运势生成引擎：将命理数据转化为自然语言运势分析"""

import random
from datetime import date, timedelta

from ganzhi import (
    TIAN_GAN, DI_ZHI, WU_XING, GAN_WUXING, ZHI_WUXING,
    get_day_ganzhi, get_year_ganzhi, get_month_ganzhi,
    get_gan_index, get_zhi_index, get_wuxing_name,
)
from bazi import BaziChart, analyze_daily_interaction


def generate_fortune(chart, target_date=None):
    """生成完整的每日运势分析"""
    if target_date is None:
        today = date.today()
        target_date = (today.year, today.month, today.day)
    else:
        today = date(*target_date)

    year, month, day = target_date
    day_of_week = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][today.weekday()]

    # 当日干支
    day_gz = get_day_ganzhi(year, month, day)
    year_gz = get_year_ganzhi(year)
    month_gz = get_month_ganzhi(year, month, day)

    # 命局交互分析
    interaction = analyze_daily_interaction(chart, target_date)

    # 生成各部分运势
    lines = []

    # === 标题 ===
    lines.append(f"每日运势 | {year}年{month}月{day}日 {day_of_week}")
    lines.append("=" * 50)
    lines.append("")

    # === 1. 整体运势概述 ===
    lines.append("一、整体运势概述")
    lines.append("-" * 30)
    lines.append(f"今日干支：{year_gz}年 {month_gz}月 {day_gz}日")
    lines.append(f"您的日主为{chart.ri_wuxing}（{chart.ri_gan}），命局状态：{chart.xiyong['日主状态']}")
    lines.append(f"今日日干{day_gz[0]}属{interaction['日干五行']}，为您的{interaction['十神']}日")
    lines.append(interaction["五行分析"])
    lines.append("")

    # 喜用神与忌神
    xiyong_text = "、".join([f"{x[0]}({x[1]})" for x in chart.xiyong["喜用神"]])
    ji_text = "、".join([f"{x[0]}({x[1]})" for x in chart.xiyong["忌神"]])
    lines.append(f"喜用神：{xiyong_text}")
    lines.append(f"忌神：{ji_text}")
    lines.append("")

    # 地支交互总结
    if interaction["地支交互"]:
        lines.append("【命局提示】")
        for di in interaction["地支交互"]:
            lines.append(f"  · {di}")
        lines.append("")

    if interaction["天干交互"]:
        for gi in interaction["天干交互"]:
            lines.append(f"  · {gi}")
        lines.append("")

    # === 2. 事业/学业运 ===
    lines.append("二、事业 / 学业运")
    lines.append("-" * 30)
    lines.append(_generate_career_fortune(chart, interaction))
    lines.append("")

    # === 3. 财运 ===
    lines.append("三、财运")
    lines.append("-" * 30)
    lines.append(_generate_wealth_fortune(chart, interaction))
    lines.append("")

    # === 4. 感情/人际 ===
    lines.append("四、感情 / 人际")
    lines.append("-" * 30)
    lines.append(_generate_relationship_fortune(chart, interaction))
    lines.append("")

    # === 5. 健康 ===
    lines.append("五、健康")
    lines.append("-" * 30)
    lines.append(_generate_health_fortune(chart, interaction))
    lines.append("")

    # === 6. 周末展望 ===
    lines.append("六、周末简要展望")
    lines.append("-" * 30)
    lines.append(_generate_weekend_outlook(chart, today))
    lines.append("")

    # === 7. 综合建议 ===
    lines.append("七、综合建议")
    lines.append("-" * 30)
    lines.append("")

    # 本周宜做
    lines.append("【本周宜做】")
    for item in _get_dos(chart, interaction):
        lines.append(f"  [+] {item}")
    lines.append("")

    # 本周不宜做
    lines.append("【本周不宜做】")
    for item in _get_donts(chart, interaction):
        lines.append(f"  [-] {item}")
    lines.append("")

    # 开运小建议
    lines.append("【开运锦囊】")
    for item in _get_lucky_tips(chart, interaction):
        lines.append(f"  > {item}")
    lines.append("")

    # 结尾
    lines.append("-" * 50)
    lines.append(f"生成时间：{today.isoformat()}  |  基于命理算法自动生成，仅供娱乐参考")
    lines.append("")

    return "\n".join(lines)


def _generate_career_fortune(chart, interaction):
    """生成事业学业运势"""
    shi_shen = interaction["十神"]
    wx_impact = interaction["五行影响"]
    ri_wx = chart.ri_wuxing

    parts = []

    if wx_impact == "有利":
        parts.append(f"今日整体运势对您有利。")

    if shi_shen in ("正官", "七杀"):
        parts.append(f"今日为{shi_shen}日，事业压力感上升，但也是展现能力和责任心的好时机。工作上可能有领导交代的任务，需要认真对待。适合处理积压的行政事务和需要纪律性完成的工作。")
        if wx_impact == "有利":
            parts.append("压力就是动力，今天的努力会被看到。建议主动承担有挑战性的任务，有望获得上级认可。")
        else:
            parts.append("注意不要同时揽太多事情，合理分配精力，避免因压力过大影响判断。")
    elif shi_shen in ("正印", "偏印"):
        parts.append(f"今日为{shi_shen}日，适合学习充电和深度思考。工作中的决策需要更多信息支撑，不妨多查阅资料、咨询前辈。适合处理需要专业知识和经验积累的事务。")
        parts.append("学生党今日学习效率较高，适合攻克难点。工作中则适合做规划和长远布局。")
    elif shi_shen in ("食神", "伤官"):
        parts.append(f"今日为{shi_shen}日，创造力充沛，思维活跃。适合头脑风暴、创意设计、写作表达等需要灵感的工作。但需注意言辞，避免过于直接而得罪人。")
        if shi_shen == "伤官":
            parts.append("伤官日尤需注意职场沟通方式，有话好好说，避免顶撞上级。")
        else:
            parts.append("食神日心情愉悦，适合与同事轻松交流，可能会有意外收获的灵感。")
    elif shi_shen in ("正财", "偏财"):
        parts.append(f"今日为{shi_shen}日，务实导向明显。工作上适合处理与数据、财务、商务相关的事务。做生意的朋友今日可积极开拓客户。")
        parts.append("做事讲究效率，避免空谈，结果导向会让你更有成就感。")
    elif shi_shen in ("比肩", "劫财"):
        parts.append(f"今日为{shi_shen}日，团队协作是重点。单打独斗效率不高，多与同事沟通合作能事半功倍。但也要注意竞争关系，升职或项目争取中可能会遇到势均力敌的对手。")
        if shi_shen == "劫财":
            parts.append("劫财日需留心他人抢功或剽窃创意，重要文档做好备份。")

    if chart.ri_wuxing == "土":
        parts.append("土性日主的您踏实稳重，今日宜发挥务实本色，把基础工作做扎实。")
    elif chart.ri_wuxing == "火":
        parts.append("火性日主的您热情积极，今日宜保持这份冲劲，但勿急躁冒进。")
    elif chart.ri_wuxing == "金":
        parts.append("金性日主的您果断利落，今日适合做决策和推动事情落地。")
    elif chart.ri_wuxing == "水":
        parts.append("水性日主的您思维灵活，今日适合处理需要变通和沟通的工作。")
    elif chart.ri_wuxing == "木":
        parts.append("木性日主的您有进取心和成长欲，今日适合推进新项目和长期规划。")

    return " ".join(parts)


def _generate_wealth_fortune(chart, interaction):
    """生成财运分析"""
    shi_shen = interaction["十神"]
    wx_impact = interaction["五行影响"]

    parts = []

    if shi_shen in ("正财", "偏财"):
        parts.append(f"今日为{shi_shen}日，财运主题突出。正财运平稳，适合处理日常收支、理财规划。")
        if shi_shen == "偏财":
            parts.append("偏财日有意外之财的可能，但投资需谨慎，勿被高风险高回报的项目诱惑。小赌怡情，大赌伤身。")
        else:
            parts.append("正财日宜脚踏实地，通过劳动付出获取合理回报。今日适合谈薪资、签合同。")
    elif shi_shen in ("食神", "伤官"):
        parts.append("今日食伤生财，通过创意和技能赚钱的机会较多。适合接私活、做副业、发挥专长变现。但需注意开源也要节流。")
    elif shi_shen in ("比肩", "劫财"):
        if shi_shen == "劫财":
            parts.append("劫财日财运偏弱，注意不必要的开支和冲动消费。借钱给别人要三思，投资也需保守。")
        else:
            parts.append("比肩日财运平稳，无大起大落。适合整理账目、制定预算，但不宜做大额投资决策。")
    elif shi_shen in ("正官", "七杀"):
        parts.append("今日财星不显，正财为主。不建议主动冒险投资，守成为上。工作收入稳定即可。")
    elif shi_shen in ("正印", "偏印"):
        parts.append("今日印星当令，为学习投资（购买书籍、课程等）是值得的。但在物质消费上宜理性克制。")

    if wx_impact == "不利":
        parts.append("今日忌神当令，财务决策请格外谨慎，避免被情绪驱使做冲动决定。")
    elif wx_impact == "有利":
        parts.append("今日喜用神到位，财路较顺，小额投资或商务谈判可适当推进。")

    parts.append("总体而言，不贪不赌，量入为出，是今日财运的稳赢策略。")
    return " ".join(parts)


def _generate_relationship_fortune(chart, interaction):
    """生成感情人际运势"""
    shi_shen = interaction["十神"]
    wx_impact = interaction["五行影响"]

    parts = []

    if shi_shen in ("正官", "七杀"):
        if chart.gender == "女":
            parts.append(f"今日{shi_shen}日，女性朋友的桃花运有所提升。单身的女士可能在职场或正式场合邂逅有缘人。有伴侣者可能因工作压力影响心情，注意不要把工作中的情绪带回家。")
        else:
            parts.append(f"今日{shi_shen}日，男性朋友的人际关系需多用心。工作上与上级和同事的相处是重点，私下则适合与老友联络感情。")
    elif shi_shen in ("正财", "偏财"):
        if chart.gender == "男":
            parts.append(f"今日{shi_shen}日，男性朋友的桃花运走高。单身男士有机会通过工作或社交认识心仪对象。有伴侣的男士今日适合为对方准备小惊喜。")
        else:
            parts.append(f"今日{shi_shen}日，女性朋友在社交中魅力增加，但需分辨真心与套路。")
    elif shi_shen in ("食神", "伤官"):
        parts.append("今日社交氛围轻松，适合朋友聚会、约饭聊天。你的幽默感和表达能力在今日格外突出，人缘不错。但伤官日需注意言辞分寸，别因一时口快惹人不快。")
    elif shi_shen in ("比肩", "劫财"):
        parts.append("今日适合团队活动和朋友聚会。")
        if shi_shen == "劫财":
            parts.append("但劫财日需注意朋友间可能因利益产生摩擦，涉及金钱往来要明确。感情上也要留心第三方的干扰。")
        else:
            parts.append("比肩日利于拓展人脉，认识志同道合的新朋友。")
    elif shi_shen in ("正印", "偏印"):
        parts.append("今日适合与家人、长辈相处。不妨给父母打个电话，或在家享受安静时光。社交欲望不强时不必勉强自己，独处充电也是一种滋养。")

    if interaction["地支交互"]:
        for di in interaction["地支交互"]:
            if "合" in di:
                parts.append("今日地支相合，人缘佳，适合主动联系朋友和拓展社交。")
            if "冲" in di:
                parts.append("今日地支相冲，感情上可能有小摩擦，遇事多沟通少争执。")

    return " ".join(parts)


def _generate_health_fortune(chart, interaction):
    """生成健康运势"""
    shi_shen = interaction["十神"]
    ri_wx = chart.ri_wuxing

    parts = []

    # 五行与身体对应
    wx_health = {
        "木": "肝胆、筋骨。注意用眼疲劳和颈椎问题，适当拉伸，避免久坐。",
        "火": "心脏、血液循环。保持情绪平稳，避免急躁动怒，午后可小憩片刻。",
        "土": "脾胃、消化系统。饮食规律，少吃生冷，注意腹部保暖。",
        "金": "肺、呼吸道、皮肤。多喝水，保持空气流通，注意皮肤保湿。",
        "水": "肾、泌尿系统。保证充足睡眠，不要熬夜，适量饮水。",
    }

    parts.append(f"作为{ri_wx}性日主，您的薄弱环节在{wx_health[ri_wx]}")

    if shi_shen in ("七杀", "伤官", "劫财"):
        parts.append("今日能量消耗较大，避免过度劳累。建议适当放慢节奏，确保充足睡眠。")
    elif shi_shen in ("正官", "正印"):
        parts.append("今日精神状态较稳定，适合做一些舒缓的运动，如散步、瑜伽、太极。")
    elif shi_shen in ("食神",):
        parts.append("食神日心情愉悦，注意不要暴饮暴食，饮食清淡为宜。")
    elif shi_shen in ("偏财",):
        parts.append("偏财日容易熬夜刷手机或应酬，注意节制，保证作息规律。")

    parts.append("今日建议：保持心情愉快，适当运动，饮食清淡。身体是革命的本钱，照顾好自己。")

    return " ".join(parts)


def _generate_weekend_outlook(chart, today):
    """生成周末展望"""
    weekday = today.weekday()
    days_to_sat = 5 - weekday
    days_to_sun = 6 - weekday

    if weekday >= 5:  # 已经是周末
        return "今日就是周末，好好享受当下吧！参考上述运势分析即可。"

    sat = today + timedelta(days=days_to_sat)
    sun = today + timedelta(days=days_to_sun)

    sat_gz = get_day_ganzhi(sat.year, sat.month, sat.day)
    sun_gz = get_day_ganzhi(sun.year, sun.month, sun.day)

    sat_interaction = analyze_daily_interaction(chart, (sat.year, sat.month, sat.day))
    sun_interaction = analyze_daily_interaction(chart, (sun.year, sun.month, sun.day))

    parts = []
    parts.append(f"周六（{sat.month}月{sat.day}日）干支为{sat_gz}，{sat_interaction['十神']}日。")

    if sat_interaction["五行影响"] == "有利":
        parts.append("运势较好，适合安排重要活动或出行。")
    else:
        parts.append("运势平稳，适合居家休息或处理杂务。")

    parts.append(f"周日（{sun.month}月{sun.day}日）干支为{sun_gz}，{sun_interaction['十神']}日。")

    if sun_interaction["五行影响"] == "有利":
        parts.append("运势不错，适合为下周做准备和规划。")
    else:
        parts.append("运势一般，适合充电放松，调整状态。")

    return " ".join(parts)


def _get_dos(chart, interaction):
    """获取宜做事项"""
    shi_shen = interaction["十神"]
    wx_impact = interaction["五行影响"]

    dos = []

    if wx_impact == "有利":
        dos.append("推进重要项目和工作决策，今日运势助你事半功倍")
        dos.append("主动联络朋友或客户，人际关系运较好")

    if shi_shen in ("正官", "七杀"):
        dos.append("制定工作计划，把待办事项按优先级排序")
        dos.append("向领导汇报工作进展，主动展示成果")
    elif shi_shen in ("正印", "偏印"):
        dos.append("花时间学习新知识，阅读专业书籍或优质文章")
        dos.append("记录心得体会，反思近期工作和生活")
    elif shi_shen in ("食神", "伤官"):
        dos.append("进行创意工作，写下灵感和想法")
        dos.append("约朋友吃饭，轻松社交")
    elif shi_shen in ("正财", "偏财"):
        dos.append("整理财务账目，做好收支记录")
        dos.append("谈薪资、谈合作、谈商务条款")
    elif shi_shen in ("比肩", "劫财"):
        dos.append("团队合作，多与同事交流协作")
        dos.append("参加行业交流活动，拓展人脉")

    # 通用建议
    dos.append("保持积极心态，遇到问题先冷静思考再行动")
    return dos[:5]


def _get_donts(chart, interaction):
    """获取不宜做的事项"""
    shi_shen = interaction["十神"]
    wx_impact = interaction["五行影响"]

    donts = []

    if wx_impact == "不利":
        donts.append("避免冲动做重大决策，忌神当令时宜稳不宜急")

    if shi_shen in ("劫财",):
        donts.append("避免大额消费和非必要借贷")
        donts.append("不要轻易相信他人承诺的高回报投资")
    elif shi_shen in ("七杀",):
        donts.append("避免与上级正面冲突，以柔克刚更好")
        donts.append("不宜熬夜加班过度消耗精力")
    elif shi_shen in ("伤官",):
        donts.append("注意言辞，不要口无遮拦得罪人")
        donts.append("不宜背后议论他人")
    elif shi_shen in ("偏印",):
        donts.append("避免钻牛角尖，想不通的事先放一放")
    elif shi_shen in ("正财", "偏财"):
        donts.append("不宜参与高风险投机活动")

    donts.append("不要忽视身体发出的疲劳信号，适时休息")
    return donts[:5]


def _get_lucky_tips(chart, interaction):
    """开运小建议"""
    ri_wx = chart.ri_wuxing
    xiyong_wxs = [x[0] for x in chart.xiyong["喜用神"]]

    # 幸运色映射
    wx_colors = {
        "木": "绿色、青色系",
        "火": "红色、紫色系",
        "土": "黄色、棕色系",
        "金": "白色、银色系",
        "水": "黑色、蓝色系",
    }

    # 方位映射
    wx_directions = {
        "木": "东方",
        "火": "南方",
        "土": "中央/西南方",
        "金": "西方",
        "水": "北方",
    }

    tips = []

    # 幸运色
    lucky_colors = [wx_colors[wx] for wx in xiyong_wxs if wx in wx_colors]
    if lucky_colors:
        tips.append(f"幸运色：{'、'.join(lucky_colors)}，今日穿搭可适当加入这些颜色元素")

    # 吉位
    lucky_dir = [wx_directions[wx] for wx in xiyong_wxs if wx in wx_directions]
    if lucky_dir:
        tips.append(f"吉位：{'、'.join(lucky_dir[:2])}，办公或洽谈可面朝此方位")

    # 助运习惯
    if "水" in xiyong_wxs:
        tips.append("多喝水，佩戴黑色或蓝色饰品有助于增强运势")
    if "金" in xiyong_wxs:
        tips.append("佩戴金属饰品，使用白色系物品有助于增强运势")
    if "木" in xiyong_wxs:
        tips.append("办公桌上摆放绿色植物，多接触自然有助于增强运势")
    if "火" in xiyong_wxs:
        tips.append("保持热情积极的心态，穿红色或暖色系衣物有助于增强运势")
    if "土" in xiyong_wxs:
        tips.append("佩戴黄水晶或棕色系饰品，脚踏实地做好每件小事有助于增强运势")

    tips.append("早晨起床后喝一杯温水，深呼吸三次，以积极的姿态开启新的一天")
    return tips[:5]

