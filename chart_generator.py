import matplotlib.pyplot as plt
import matplotlib
import os
from datetime import datetime
from typing import List, Dict, Optional
import random

# 设置中文字体支持
matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
matplotlib.rcParams['axes.unicode_minus'] = False

# 确保图表目录存在
CHART_DIR = os.path.join(os.path.dirname(__file__), 'static', 'charts')
os.makedirs(CHART_DIR, exist_ok=True)


def generate_temperature_chart(forecast_data: List[Dict], city: str) -> str:
    """
    生成温度趋势折线图

    Args:
        forecast_data: 天气预报数据列表
        city: 城市名称

    Returns:
        图表文件路径
    """
    if not forecast_data:
        raise ValueError("没有可用的预报数据")

    # 提取数据
    dates = [item['date_display'] for item in forecast_data]
    temps = [item['temp'] for item in forecast_data]
    temp_mins = [item['temp_min'] for item in forecast_data]
    temp_maxs = [item['temp_max'] for item in forecast_data]

    # 创建图表
    plt.figure(figsize=(10, 6))

    # 绘制温度范围填充
    plt.fill_between(range(len(dates)), temp_mins, temp_maxs,
                     alpha=0.2, color='skyblue', label='温度范围')

    # 绘制温度折线
    plt.plot(range(len(dates)), temps, marker='o', linewidth=2,
             markersize=8, color='#FF6B6B', label='平均温度')

    # 绘制最高温和最低温
    plt.plot(range(len(dates)), temp_maxs, marker='^', linewidth=1,
             linestyle='--', markersize=6, color='#FF9F43', alpha=0.7)
    plt.plot(range(len(dates)), temp_mins, marker='v', linewidth=1,
             linestyle='--', markersize=6, color='#54A0FF', alpha=0.7)

    # 设置图表标题和标签
    plt.title(f'{city} 未来{len(dates)}天温度趋势', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('日期', fontsize=12)
    plt.ylabel('温度 (°C)', fontsize=12)

    # 设置x轴刻度
    plt.xticks(range(len(dates)), dates)

    # 添加网格
    plt.grid(True, alpha=0.3, linestyle='--')

    # 添加图例
    plt.legend(loc='upper right', fontsize=10)

    # 设置y轴范围，留出一些空间
    all_temps = temp_mins + temp_maxs + temps
    plt.ylim(min(all_temps) - 2, max(all_temps) + 2)

    # 调整布局
    plt.tight_layout()

    # 生成唯一的文件名
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    chart_filename = f'temp_trend_{timestamp}_{random.randint(1000, 9999)}.png'
    chart_path = os.path.join(CHART_DIR, chart_filename)

    # 保存图表
    plt.savefig(chart_path, dpi=100, bbox_inches='tight', facecolor='white')
    plt.close()

    return f'/static/charts/{chart_filename}'


def generate_weather_pie_chart(forecast_data: List[Dict], city: str) -> str:
    """
    生成天气类型分布饼图

    Args:
        forecast_data: 天气预报数据列表
        city: 城市名称

    Returns:
        图表文件路径
    """
    if not forecast_data:
        raise ValueError("没有可用的预报数据")

    # 统计天气类型
    weather_counts = {}
    for item in forecast_data:
        weather_type = item['description']
        weather_counts[weather_type] = weather_counts.get(weather_type, 0) + 1

    # 准备饼图数据
    labels = list(weather_counts.keys())
    sizes = list(weather_counts.values())
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']

    # 创建饼图
    plt.figure(figsize=(8, 8))
    wedges, texts, autotexts = plt.pie(
        sizes,
        labels=labels,
        autopct='%1.1f%%',
        colors=colors[:len(labels)],
        startangle=90,
        textprops={'fontsize': 11}
    )

    # 设置百分比文字颜色为白色
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')

    plt.title(f'{city} 天气分布', fontsize=16, fontweight='bold', pad=20)
    plt.axis('equal')
    plt.tight_layout()

    # 生成唯一的文件名
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    chart_filename = f'weather_pie_{timestamp}_{random.randint(1000, 9999)}.png'
    chart_path = os.path.join(CHART_DIR, chart_filename)

    # 保存图表
    plt.savefig(chart_path, dpi=100, bbox_inches='tight', facecolor='white')
    plt.close()

    return f'/static/charts/{chart_filename}'


def generate_combined_chart(forecast_data: List[Dict], city: str) -> Dict[str, str]:
    """
    生成组合图表（温度趋势 + 天气分布）

    Args:
        forecast_data: 天气预报数据列表
        city: 城市名称

    Returns:
        包含两个图表路径的字典
    """
    try:
        temp_chart = generate_temperature_chart(forecast_data, city)
    except Exception as e:
        print(f"生成温度图表失败: {e}")
        temp_chart = None

    try:
        weather_chart = generate_weather_pie_chart(forecast_data, city)
    except Exception as e:
        print(f"生成天气饼图失败: {e}")
        weather_chart = None

    return {
        'temperature_chart': temp_chart,
        'weather_pie_chart': weather_chart
    }


def cleanup_old_charts(max_age_hours: int = 1):
    """
    清理旧的图表文件

    Args:
        max_age_hours: 最大保留时间（小时）
    """
    try:
        now = datetime.now()
        for filename in os.listdir(CHART_DIR):
            filepath = os.path.join(CHART_DIR, filename)
            if os.path.isfile(filepath) and filename.endswith('.png'):
                # 获取文件修改时间
                mod_time = datetime.fromtimestamp(os.path.getmtime(filepath))
                age = now - mod_time

                # 如果超过指定时间，删除文件
                if age.total_seconds() > max_age_hours * 3600:
                    os.remove(filepath)
    except Exception as e:
        print(f"清理图表文件时出错: {e}")
