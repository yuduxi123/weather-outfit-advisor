# Weather Outfit Advisor · 天气穿搭助手

`Python` · `Flask` · `OpenWeather` · `Matplotlib`

查询城市天气与未来预报，并生成穿搭建议和图表。适合作为天气 API 接入与 Flask Web 开发的学习项目。

[项目导航](https://github.com/yuduxi123) · [中文补充说明](README_CN.md) · [数据与依赖来源](ATTRIBUTION.md)

## 功能与结构

| 模块 | 作用 |
|---|---|
| `weather_api.py` | OpenWeather 当前天气和预报接入 |
| `outfit_advisor.py` | 穿搭建议逻辑 |
| `chart_generator.py` | 天气图表 |
| `app.py` / `templates/` | Flask 服务与页面 |

## 本地运行

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.template .env
# 在本地 .env 填写自己的 OPENWEATHER_API_KEY 和 SECRET_KEY
python app.py
```

访问 `http://localhost:5000`。不要把真实 Key 写入 README、提交记录或截图。API可用性、额度和条款以 OpenWeather 为准。

## Render 部署

新建 Web Service，选择本仓库，构建命令使用 `pip install -r requirements.txt`，启动命令使用 `gunicorn app:app -b 0.0.0.0:$PORT`。在平台设置 `OPENWEATHER_API_KEY`、`SECRET_KEY`，不要上传 `.env`。

## 当前边界

天气和预报依赖外部服务；穿搭建议仅供参考。这里的部署步骤不代表当前存在已验证的在线演示。本次只整理文档，未重新部署或运行真实天气API测试。

## 来源与许可

天气数据来自 [OpenWeather](https://openweathermap.org/)。主要运行依赖见 [ATTRIBUTION.md](ATTRIBUTION.md) 与 `requirements.txt`。第三方服务和依赖分别适用其条款及许可证；不因本仓库展示而改变授权。
