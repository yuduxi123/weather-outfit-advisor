@echo off
echo 正在准备部署到 Render...
echo ==========================

echo 1. 初始化 git 仓库...
git init

echo 2. 添加所有文件到 git...
git add .

echo 3. 创建第一次提交...
git commit -m "Initial commit - Smart Weather Outfit Advisor"

echo 4. 创建并切换到 main 分支...
git branch -M main

echo ==========================
echo.
echo ✅ Git 仓库准备完成！
echo.
echo 接下来需要将代码推送到 GitHub：
echo 1. 访问 https://github.com 并创建新仓库
echo 2. 使用以下命令推送：
echo    git remote add origin https://github.com/您的用户名/weather-outfit-advisor.git
echo    git push -u origin main
echo.
echo 然后在 Render 网站导入您的 GitHub 仓库部署
echo.
pause