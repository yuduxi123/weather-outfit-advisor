# 智能天气穿搭助手 - Render 部署指南

## 准备工作

### 1. 安装 Git（如果尚未安装）
访问 https://git-scm.com/downloads 下载并安装 Git

### 2. 创建 GitHub 仓库
1. 访问 https://github.com
2. 登录您的账号
3. 点击 "New"
4. 填写仓库名称：`weather-outfit-advisor`
5. 选择 Public（公开）
6. 点击 "Create repository"

### 3. 初始化 Git 并推送代码

打开命令提示符，进入项目目录：

```bash
# 进入项目目录
cd C:\Users\Windows\Desktop\practice2

# 初始化 Git 仓库
git init

# 添加所有文件
git add .

# 提交代码
git commit -m "Initial commit - Smart Weather Outfit Advisor"

# 将本地仓库与 GitHub 关联
git remote add origin https://github.com/您的用户名/weather-outfit-advisor.git

# 推送到 GitHub
git push -u origin main
```

## 在 Render 部署

### 1. 创建 Render 账号
访问 https://render.com 并注册账号

### 2. 创建 Web Service
1. 登录 Render 后，点击 "New +" → "Web Service"
2. 选择您的 GitHub 仓库
3. 填写以下配置信息：

**基础信息：**
- Name: `weather-outfit-advisor`
- Region: 选择离您最近的区域（如 Oregon）
- Branch: `main`

**构建命令：**
```bash
pip install -r requirements.txt
```

**启动命令：**
```bash
gunicorn app:app -b 0.0.0.0:$PORT
```

### 3. 添加环境变量
点击 "Advanced Settings" → "Environment Variables"，添加：

```
OPENWEATHER_API_KEY=your-openweather-api-key
SECRET_KEY=your-secret-key-here
```

### 4. 部署
点击 "Create Web Service" 开始部署

## 部署成功

部署完成后，您的应用将在类似以下地址访问：
`https://weather-outfit-advisor.onrender.com`

## 常见问题

### 1. Git 命令提示符找不到
- 确保 Git 已正确安装
- 重新打开命令提示符

### 2. Push 失败
- 检查 GitHub 用户名和仓库 URL
- 确认已在 GitHub 设置 SSH 密钥或使用 HTTPS

### 3. Render 部署失败
- 检查构建命令是否正确
- 确认 requirements.txt 文件存在
- 检查环境变量是否正确设置

### 4. 获取新的 API 密钥
建议使用自己的 API 密钥：
1. 访问 https://openweathermap.org/api
2. 注册账号
3. 在 API Keys 页面创建新密钥
4. 更新 Render 环境变量中的值

## 注意事项

- Render 免费版有 30 分钟休眠机制
- 首次部署需要 2-5 分钟
- 定期访问防止休眠