# 智能天气穿搭助手

一个基于 Flask 的 Web 应用，通过天气数据为用户提供智能穿搭建议。

## 功能特点
- 查询实时天气
- 5天天气预报
- 智能穿搭建议
- 天气数据可视化图表

## 部署到 Render

### 1. 推送代码到 GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/您的用户名/weather-outfit-advisor.git
git push -u origin main
```

### 2. 在 Render 上部署

1. 访问 [render.com](https://render.com/) 并登录
2. 点击 "New +" → "Web Service"
3. 选择您的 GitHub 仓库
4. 填写配置信息：
   - Name: `weather-outfit-advisor`
   - Root Directory: `/`
   - Runtime: `Python 3`
   
5. Build Command:
   ```bash
   pip install -r requirements.txt
   ```

6. Start Command:
   ```bash
   gunicorn app:app -b 0.0.0.0:$PORT
   ```

7. 环境变量：
   ```bash
   OPENWEATHER_API_KEY=your-openweather-api-key
   SECRET_KEY=您的生产密钥
   ```

7. 点击 "Create Web Service"

### 3. 部署成功后
您的应用将在类似 `https://weather-outfit-advisor.onrender.com` 的地址访问

## 开发环境运行

```bash
# 安装依赖
pip install -r requirements.txt

# 运行开发服务器
python app.py
```

访问 http://localhost:5000