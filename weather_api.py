import requests
import os
import time
from dotenv import load_dotenv, find_dotenv
from datetime import datetime
from typing import Dict, Optional

# 使用 find_dotenv() 查找 .env 文件
dotenv_path = find_dotenv(usecwd=True)
if dotenv_path:
    load_dotenv(dotenv_path)

API_KEY = os.getenv('OPENWEATHER_API_KEY', '')
BASE_URL = 'https://api.openweathermap.org/data/2.5'
REQUEST_TIMEOUT = 30  # 增加超时时间到30秒
MAX_RETRIES = 3  # 最多重试3次

# 中英文城市名映射表
CITY_NAME_MAP = {
    '北京': 'Beijing',
    '上海': 'Shanghai',
    '广州': 'Guangzhou',
    '深圳': 'Shenzhen',
    '杭州': 'Hangzhou',
    '南京': 'Nanjing',
    '武汉': 'Wuhan',
    '成都': 'Chengdu',
    '重庆': 'Chongqing',
    '西安': 'Xian',
    '天津': 'Tianjin',
    '苏州': 'Suzhou',
    '长沙': 'Changsha',
    '郑州': 'Zhengzhou',
    '东莞': 'Dongguan',
    '青岛': 'Qingdao',
    '沈阳': 'Shenyang',
    '宁波': 'Ningbo',
    '昆明': 'Kunming',
    '合肥': 'Hefei',
    '福州': 'Fuzhou',
    '厦门': 'Xiamen',
    '哈尔滨': 'Harbin',
    '济南': 'Jinan',
    '大连': 'Dalian',
    '长春': 'Changchun',
    '太原': 'Taiyuan',
    '南宁': 'Nanning',
    '贵阳': 'Guiyang',
    '南昌': 'Nanchang',
    '兰州': 'Lanzhou',
    '海口': 'Haikou',
    '三亚': 'Sanya',
    '拉萨': 'Lhasa',
    '乌鲁木齐': 'Urumqi',
    '呼和浩特': 'Hohhot',
    '银川': 'Yinchuan',
    '西宁': 'Xining',
    '石家庄': 'Shijiazhuang',
    '唐山': 'Tangshan',
    '吉林': 'Jilin',
    '鞍山': 'Anshan',
    '齐齐哈尔': 'Qiqihar',
    '大庆': 'Daqing',
    '佳木斯': 'Jiamusi',
    '牡丹江': 'Mudanjiang',
    '鸡西': 'Jixi',
    '鹤岗': 'Hegang',
    '双鸭山': 'Shuangyashan',
    '伊春': 'Yichun',
    '七台河': 'Qitaihe',
    '黑河': 'Heihe',
    '大兴安岭': 'Daxinganling',
    '延吉': 'Yanji',
    '通化': 'Tonghua',
    '白山': 'Baishan',
    '松原': 'Songyuan',
    '白城': 'Baicheng',
    '承德': 'Chengde',
    '张家口': 'Zhangjiakou',
    '秦皇岛': 'Qinhuangdao',
    '廊坊': 'Langfang',
    '保定': 'Baoding',
    '沧州': 'Cangzhou',
    '衡水': 'Hengshui',
    '邢台': 'Xingtai',
    '邯郸': 'Handan',
    '德州': 'Dezhou',
    '滨州': 'Binzhou',
    '东营': 'Dongying',
    '潍坊': 'Weifang',
    '烟台': 'Yantai',
    '威海': 'Weihai',
    '临沂': 'Linyi',
    '日照': 'Rizhao',
    '枣庄': 'Zaozhuang',
    '济宁': 'Jining',
    '泰安': 'Taian',
    '莱芜': 'Laiwu',
    '聊城': 'Liaocheng',
    '菏泽': 'Heze',
    '开封': 'Kaifeng',
    '洛阳': 'Luoyang',
    '平顶山': 'Pingdingshan',
    '安阳': 'Anyang',
    '鹤壁': 'Hebi',
    '新乡': 'Xinxiang',
    '焦作': 'Jiaozuo',
    '濮阳': 'Puyang',
    '许昌': 'Xuchang',
    '漯河': 'Luohe',
    '三门峡': 'Sanmenxia',
    '南阳': 'Nanyang',
    '商丘': 'Shangqiu',
    '信阳': 'Xinyang',
    '周口': 'Zhoukou',
    '驻马店': 'Zhumadian',
    '香港': 'Hong Kong',
    '澳门': 'Macau',
    '台北': 'Taipei',
    '伦敦': 'London',
    '纽约': 'New York',
    '东京': 'Tokyo',
    '巴黎': 'Paris',
    '悉尼': 'Sydney',
    '新加坡': 'Singapore'
}


def make_request_with_retry(url: str, params: dict) -> requests.Response:
    """
    带重试机制的请求函数
    """
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            return response
        except requests.exceptions.Timeout:
            print(f"请求超时 (尝试 {attempt + 1}/{MAX_RETRIES})")
            if attempt < MAX_RETRIES - 1:
                time.sleep(2 ** attempt)  # 指数退避
            else:
                raise
        except requests.exceptions.ConnectionError:
            print(f"连接错误 (尝试 {attempt + 1}/{MAX_RETRIES})")
            if attempt < MAX_RETRIES - 1:
                time.sleep(2 ** attempt)
            else:
                raise
        except Exception as e:
            print(f"请求失败: {type(e).__name__}: {e}")
            raise


def get_current_weather(city: str) -> Optional[Dict]:
    """获取指定城市的当前天气数据"""
    url = f"{BASE_URL}/weather"

    # 如果是中文城市名，转换为英文名
    query_city = CITY_NAME_MAP.get(city, city)

    params = {
        'q': query_city,
        'appid': API_KEY,
        'units': 'metric',
        'lang': 'zh_cn'
    }

    try:
        response = make_request_with_retry(url, params)
        data = response.json()
        return {
            'city': city,  # 使用原始城市名
            'country': data['sys']['country'],
            'temp': round(data['main']['temp'], 1),
            'feels_like': round(data['main']['feels_like'], 1),
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'description': data['weather'][0]['description'],
            'main': data['weather'][0]['main'],
            'wind_speed': data['wind'].get('speed', 0),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            raise ValueError(f"城市 '{city}' 未找到，请检查城市名称")
        elif response.status_code == 401:
            raise ValueError("API密钥无效，请检查.env文件中的OPENWEATHER_API_KEY")
        elif response.status_code == 429:
            raise ValueError("API请求次数超限，请稍后重试")
        else:
            raise ValueError(f"天气API错误: {e}")
    except requests.exceptions.Timeout:
        raise ValueError("网络请求超时，请检查网络连接后重试")
    except requests.exceptions.ConnectionError:
        raise ValueError("无法连接到天气API服务器，请检查网络连接")
    except requests.exceptions.RequestException as e:
        raise ValueError(f"网络请求失败: {e}")


def get_forecast(city: str, days: int = 5) -> Optional[list]:
    """获取指定城市的未来天气预报数据"""
    url = f"{BASE_URL}/forecast"

    # 如果是中文城市名，转换为英文名
    query_city = CITY_NAME_MAP.get(city, city)

    params = {
        'q': query_city,
        'appid': API_KEY,
        'units': 'metric',
        'cnt': days * 8  # 每天8个时间点（每3小时一个）
    }

    try:
        response = make_request_with_retry(url, params)
        data = response.json()

        # 检查API是否返回了数据
        if 'list' not in data or not data['list']:
            print(f"警告: API未返回预报数据, city={query_city}")
            return []

        forecasts = []

        # 首先收集所有数据，按日期分组
        daily_data = {}  # {date_str: [items]}
        for item in data['list']:
            dt = datetime.fromtimestamp(item['dt'])
            date_str = dt.strftime('%Y-%m-%d')
            time_str = dt.strftime('%H:%M')

            if date_str not in daily_data:
                daily_data[date_str] = []
            daily_data[date_str].append({
                'dt': dt,
                'time_str': time_str,
                'temp': round(item['main']['temp'], 1),
                'temp_min': round(item['main']['temp_min'], 1),
                'temp_max': round(item['main']['temp_max'], 1),
                'description': item['weather'][0]['description'],
                'main': item['weather'][0]['main'],
                'humidity': item['main']['humidity']
            })

        # 从每天的多个时间点中选择最合适的一个
        # 优先级: 12:00 > 15:00 > 09:00 > 其他
        priority_times = ['12:00', '15:00', '09:00']

        for date_str in sorted(daily_data.keys()):
            day_items = daily_data[date_str]
            selected_item = None

            # 按优先级查找
            for priority_time in priority_times:
                for item in day_items:
                    if item['time_str'] == priority_time:
                        selected_item = item
                        break
                if selected_item:
                    break

            # 如果没有找到优先时间点，取第一个
            if not selected_item and day_items:
                selected_item = day_items[0]

            if selected_item:
                forecasts.append({
                    'date': date_str,
                    'date_display': selected_item['dt'].strftime('%m/%d'),
                    'temp': selected_item['temp'],
                    'temp_min': selected_item['temp_min'],
                    'temp_max': selected_item['temp_max'],
                    'description': selected_item['description'],
                    'main': selected_item['main'],
                    'humidity': selected_item['humidity']
                })

            if len(forecasts) >= days:
                break

        return forecasts[:days]
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            raise ValueError(f"城市 '{city}' 未找到，请检查城市名称")
        elif response.status_code == 401:
            raise ValueError("API密钥无效，请检查.env文件中的OPENWEATHER_API_KEY")
        elif response.status_code == 429:
            raise ValueError("API请求次数超限，请稍后重试")
        else:
            raise ValueError(f"天气API错误: {e}")
    except requests.exceptions.Timeout:
        raise ValueError("网络请求超时，请检查网络连接后重试")
    except requests.exceptions.ConnectionError:
        raise ValueError("无法连接到天气API服务器，请检查网络连接")
    except requests.exceptions.RequestException as e:
        raise ValueError(f"网络请求失败: {e}")
    except Exception as e:
        # 捕获所有其他异常，避免应用崩溃
        print(f"get_forecast 异常: {type(e).__name__}: {e}")
        raise ValueError(f"获取天气预报失败: {str(e)}")
