from typing import Dict, List


def generate_outfit_advice(weather: Dict) -> Dict:
    """
    根据天气数据生成穿搭建议
    """
    temp = weather['temp']
    description = weather['description'].lower()
    main = weather['main'].lower()

    # 基础穿搭（根据温度）
    base_outfit = get_temp_based_outfit(temp)

    # 天气条件适配
    weather_adaptation = get_weather_adaptation(description, main)

    # 配件建议
    accessories = get_accessories(temp, description, main)

    # 组合完整建议
    full_advice = combine_advice(base_outfit, weather_adaptation, accessories)

    # AI润色（模拟）
    polished_advice = polish_advice(full_advice, temp, description)

    return {
        'base_outfit': base_outfit,
        'weather_adaptation': weather_adaptation,
        'accessories': accessories,
        'full_advice': full_advice,
        'polished_advice': polished_advice,
        'temperature_category': get_temperature_category(temp)
    }


def get_temp_based_outfit(temp: float) -> str:
    """根据温度返回基础穿搭建议"""
    if temp < 0:
        return "加厚羽绒服 + 保暖内衣 + 厚毛衣 + 加绒长裤"
    elif 0 <= temp < 10:
        return "厚外套/毛呢大衣 + 毛衣/卫衣 + 长裤 + 长袜"
    elif 10 <= temp < 20:
        return "薄外套/风衣 + 长袖T恤/针织衫 + 休闲裤/牛仔裤"
    elif 20 <= temp < 28:
        return "T恤/薄衫 + 轻薄外套（可选）+ 牛仔裤/休闲裤"
    elif 28 <= temp < 35:
        return "短袖/背心 + 短裤/薄长裤 + 防晒衣"
    else:  # temp >= 35
        return "透气短袖 + 超薄短裤 + 凉鞋 + 防晒帽"


def get_weather_adaptation(description: str, main: str) -> str:
    """根据天气条件返回穿搭调整建议"""
    adaptations = []

    if 'rain' in description or '雨' in description:
        adaptations.append("防水外套或雨衣")
    if 'snow' in description or '雪' in description:
        adaptations.append("防水防滑的鞋子")
    if 'cloud' in main:
        adaptations.append("可适当增加层次感")
    if 'clear' in main:
        adaptations.append("适合浅色系服装")

    return " | ".join(adaptations) if adaptations else "适合常规穿搭"


def get_accessories(temp: float, description: str, main: str) -> List[str]:
    """返回配件建议"""
    accessories = []

    # 温度相关配件
    if temp < 0:
        accessories.extend(["保暖帽", "围巾", "手套", "口罩"])
    elif temp < 10:
        accessories.extend(["帽子", "围巾"])
    elif temp < 20:
        accessories.append("薄围巾（可选）")

    # 天气相关配件
    if 'rain' in description or '雨' in description:
        accessories.append("雨伞")
    if 'snow' in description or '雪' in description:
        accessories.extend(["防水靴", "厚手套"])
    if 'wind' in description or 'wind' in main:
        accessories.append("防风帽")
    if 'clear' in main or '晴' in description:
        accessories.extend(["墨镜", "防晒霜", "遮阳帽"])

    return accessories


def combine_advice(base_outfit: str, weather_adaptation: str, accessories: List[str]) -> str:
    """组合穿搭建议"""
    advice = f"👔 服装: {base_outfit}\n"
    advice += f"🌤️ 调整: {weather_adaptation}\n"
    if accessories:
        advice += f"🎒 配件: {', '.join(accessories)}"
    return advice


def polish_advice(advice: str, temp: float, description: str) -> str:
    """
    AI润色建议（模拟）
    生成更自然的语言表达
    """
    category = get_temperature_category(temp)

    polished = f"🌡️ 当前气温 {temp}°C，属于{category}天气。\n\n"

    if temp < 10:
        polished += "❄️ 寒冷预警！请务必注意保暖。建议采用多层次穿搭，"
        polished += "内搭要足够厚实，外层选择防风保暖效果好的外套。"
    elif temp < 20:
        polished += "🍂 天气凉爽，是叠穿的绝佳时机！"
        polished += "可以尝试不同层次的搭配，既保暖又有型。"
    elif temp < 28:
        polished += "☀️ 温度舒适，穿着自由度很高！"
        polished += "可以尽情展现个人风格，记得带一件薄外套应对温差。"
    else:
        polished += "🔥 天气炎热，建议选择透气轻盈的材质。"
        polished += "尽量避免深色系服装，做好防晒措施。"

    if 'rain' in description or '雨' in description:
        polished += "\n\n🌧️ 今天有雨，记得带伞，注意防潮！"
    if 'snow' in description or '雪' in description:
        polished += "\n\n❄️ 下雪啦！注意路滑，保暖第一！"
    if 'clear' in description or '晴' in description:
        polished += "\n☀️ 阳光明媚，心情也要像阳光一样灿烂！"

    return polished


def get_temperature_category(temp: float) -> str:
    """返回温度分类"""
    if temp < 0:
        return "极寒"
    elif temp < 10:
        return "寒冷"
    elif temp < 20:
        return "凉爽"
    elif temp < 28:
        return "舒适"
    elif temp < 35:
        return "炎热"
    else:
        return "酷热"


# 预定义的快速建议模板（用于更快的响应）
QUICK_ADVICE_TEMPLATES = {
    '极寒_雨': "❄️ 极寒雨天！加厚羽绒服+保暖内衣+防水外层，务必戴帽子和手套，穿防滑防水靴。",
    '极寒_雪': "🌨️ 极寒雪天！全套保暖装备：羽绒服+保暖内衣+围巾帽子手套，穿防滑鞋注意安全。",
    '寒冷_雨': "🌧️ 寒冷雨天！厚外套+毛衣+雨衣，穿厚袜子保暖，记得带伞！",
    '寒冷_晴': "☀️ 寒冷晴天！厚外套+毛衣，阳光虽然好但风很冷，注意防风。",
    '凉爽_雨': "🌧️ 凉爽雨天！薄外套+长袖，带好雨具，注意防潮。",
    '舒适_晴': "☀️ 舒适晴天！T恤+薄外套，天气超好，适合户外活动！",
    '炎热_晴': "🔥 炎热晴天！短袖+短裤，防晒很重要，多喝水注意防暑！",
}


def get_quick_advice(weather: Dict) -> str:
    """
    快速获取建议（备用方法）
    """
    temp = weather['temp']
    desc = weather['description'].lower()

    category = get_temperature_category(temp)
    weather_type = '雨' if 'rain' in desc or '雨' in desc else '雪' if 'snow' in desc or '雪' in desc else '晴'

    key = f"{category}_{weather_type}"
    return QUICK_ADVICE_TEMPLATES.get(key, generate_outfit_advice(weather)['polished_advice'])
