@echo off
title STREET LA Verification Bot
color 0A

cd /d C:\Users\ramon\Desktop\blood bot

echo ========================================
echo    STREET LA BOT DE VERIFICACION
echo ========================================
echo.

:: Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no esta instalado
    pause
    exit /b 1
)

:: Instalar dependencias
echo Instalando dependencias...
pip install discord.py flask gunicorn requests
echo.

:: Iniciar el bot
echo Iniciando bot...
python bot.py

pause