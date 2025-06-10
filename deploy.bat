@echo off
chcp 65001 > nul
setlocal

echo ===============================
echo 🧹 正在执行 Python 预处理脚本...
echo ===============================
python preprocess.py
if errorlevel 1 (
    echo ❌ Python 脚本执行失败，请检查错误。
    pause
    exit /b
)

echo.
echo ===============================
echo 🚀 正在构建 Jekyll 网站...
echo ===============================
call bundle exec jekyll build
if errorlevel 1 (
    echo ❌ Jekyll 构建失败，请检查错误。
    pause
    exit /b
)

echo.
echo ===============================
echo ☁️ 正在增量上传至阿里云 OSS（不会删除远程文件）...
echo ===============================
ossutil64 sync _site/ oss://zr-picture/ --force
if errorlevel 1 (
    echo ❌ OSS 上传失败，请检查配置或网络。
    pause
    exit /b
)

echo.
echo 🔄 正在刷新阿里云 CDN 缓存...
aliyun cdn RefreshObjectCaches --ObjectPath https://www.wuzhixiaojiu.com/ --ObjectType Directory > nul
if errorlevel 1 (
    echo ❌ CDN 缓存刷新失败，请检查 aliyun CLI 登录状态。
    pause
    exit /b
)

echo.
echo 🌐 正在打开博客首页...
start https://www.wuzhixiaojiu.com

echo.
echo ✅ 博客部署完成！
pause
endlocal
