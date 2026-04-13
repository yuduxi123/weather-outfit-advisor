import requests
import os
from dotenv import load_dotenv, find_dotenv

# 加载环境变量
dotenv_path = find_dotenv(usecwd=True)
if dotenv_path:
    load_dotenv(dotenv_path)

API_KEY = os.getenv('OPENWEATHER_API_KEY', '')
print(f"API Key: {API_KEY[:20]}..." if len(API_KEY) > 20 else f"API Key: {API_KEY}")

BASE_URL = 'https://api.openweathermap.org/data/2.5'

# 测试当前天气 API
print("\n=== 测试当前天气 API ===")
city = 'Chongqing'
url = f"{BASE_URL}/weather"
params = {
    'q': city,
    'appid': API_KEY,
    'units': 'metric',
    'lang': 'zh_cn'
}

try:
    print(f"请求 URL: {url}")
    print(f"参数: {params}")
    response = requests.get(url, params=params, timeout=10)
    print(f"状态码: {response.status_code}")
    response.raise_for_status()
    data = response.json()
    print(f"城市: {data.get('name')}")
    print(f"温度: {data['main']['temp']}°C")
    print(f"天气: {data['weather'][0]['description']}")
except Exception as e:
    print(f"错误: {type(e).__name__}: {e}")
    if hasattr(e, 'response') and e.response:
        print(f"响应内容: {e.response.text}")

# 测试预报 API
print("\n=== 测试预报 API ===")
url = f"{BASE_URL}/forecast"
params = {
    'q': city,
    'appid': API_KEY,
    'units': 'metric',
    'cnt': 40  # 5天 * 8个时间点
}

try:
    print(f"请求 URL: {url}")
    response = requests.get(url, params=params, timeout=10)
    print(f"状态码: {response.status_code}")
    response.raise_for_status()
    data = response.json()
    print(f"数据条目数: {len(data.get('list', []))}")
    if 'list' in data and data['list']:
        first_item = data['list'][0]
        print(f"第一条数据时间: {first_item.get('dt')}")
        print(f"第一条数据温度: {first_item['main']['temp']}°C")
except Exception as e:
    print(f"错误: {type(e).__name__}: {e}")
    if hasattr(e, 'response') and e.response:
        print(f"响应内容: {e.response.text}")
