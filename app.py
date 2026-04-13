from flask import Flask, render_template, request, jsonify
from weather_api import get_current_weather, get_forecast
from outfit_advisor import generate_outfit_advice, get_quick_advice
from chart_generator import generate_combined_chart, cleanup_old_charts
import os

app = Flask(__name__)

# 配置
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')


@app.route('/')
def home():
    """首页 - 显示城市输入表单"""
    return render_template('index.html')


@app.route('/result', methods=['POST'])
def result():
    """结果页 - 显示天气、穿搭建议和图表"""
    city = request.form.get('city', '').strip()

    if not city:
        return render_template('result.html', error='请输入城市名称')

    try:
        # 获取天气数据
        current_weather = get_current_weather(city)
        forecast = get_forecast(city, days=5)

        # 生成穿搭建议
        outfit_advice = generate_outfit_advice(current_weather)

        # 检查是否有预报数据
        charts = None
        if forecast and len(forecast) > 0:
            try:
                charts = generate_combined_chart(forecast, city)
            except Exception as e:
                print(f"图表生成错误: {type(e).__name__}: {e}")
                # 即使图表生成失败，也继续显示其他信息
        else:
            print(f"警告: 城市 {city} 没有获取到预报数据")

        # 清理旧图表（可选，每小时执行一次）
        # cleanup_old_charts(max_age_hours=1)

        return render_template('result.html',
                             weather=current_weather,
                             forecast=forecast,
                             advice=outfit_advice,
                             charts=charts)

    except ValueError as e:
        print(f"ValueError: {e}")
        return render_template('result.html', error=str(e))
    except Exception as e:
        print(f"Unexpected error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return render_template('result.html', error=f'服务器错误: {str(e)}')


@app.route('/api/weather', methods=['GET'])
def api_weather():
    """API接口 - 获取天气数据"""
    city = request.args.get('city', '').strip()

    if not city:
        return jsonify({'error': '请输入城市名称'}), 400

    try:
        current_weather = get_current_weather(city)
        forecast = get_forecast(city, days=5)
        advice = generate_outfit_advice(current_weather)

        return jsonify({
            'weather': current_weather,
            'forecast': forecast,
            'advice': advice
        })
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'服务器错误: {str(e)}'}), 500


@app.errorhandler(404)
def not_found(e):
    """404错误处理"""
    return render_template('result.html', error='页面未找到'), 404


@app.errorhandler(500)
def server_error(e):
    """500错误处理"""
    return render_template('result.html', error='服务器内部错误'), 500


if __name__ == '__main__':
    # 确保必要的目录存在
    os.makedirs('static/charts', exist_ok=True)
    os.makedirs('templates', exist_ok=True)

    # 检查API密钥
    api_key = os.getenv('OPENWEATHER_API_KEY')
    if api_key == 'your_api_key_here':
        print("⚠️  警告: 请在.env文件中设置有效的OPENWEATHER_API_KEY!")
        print("   访问 https://openweathermap.org/api 获取免费API密钥")
        print()

    print("🌤️  智能天气穿搭助手启动中...")
    print("   请访问: http://localhost:5000")
    print()

    app.run(debug=True, host='0.0.0.0', port=5000)
