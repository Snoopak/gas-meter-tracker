@echo off
chcp 65001 >nul
REM Скрипт швидкого запуску для Windows

echo ==================================
echo   📷 Система обробки лічильників
echo ==================================
echo.

REM Перевірка Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python не знайдено. Встановіть Python 3.8 або новіше з https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python знайдено
python --version

REM Перевірка Tesseract
tesseract --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Tesseract OCR не знайдено.
    echo    Завантажте з: https://github.com/UB-Mannheim/tesseract/wiki
    echo    Після встановлення додайте до PATH або вкажіть шлях в коді
    echo.
    set /p continue="Продовжити без Tesseract? (y/n): "
    if /i not "%continue%"=="y" exit /b 1
) else (
    echo ✅ Tesseract знайдено
    tesseract --version 2>&1 | findstr "tesseract"
)

REM Перевірка залежностей
echo.
echo Перевірка Python залежностей...
python -c "import cv2" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Не всі залежності встановлено.
    set /p install="Встановити залежності зараз? (y/n): "
    if /i "%install%"=="y" (
        echo Встановлення...
        pip install -r requirements.txt
        if errorlevel 0 (
            echo ✅ Залежності встановлено
        ) else (
            echo ❌ Помилка встановлення залежностей
            pause
            exit /b 1
        )
    )
) else (
    echo ✅ Залежності встановлено
)

REM Меню вибору
echo.
echo ==================================
echo Оберіть режим роботи:
echo ==================================
echo 1. Веб-інтерфейс (рекомендовано)
echo 2. Обробка одного фото
echo 3. Пакетна обробка папки
echo 4. Тестування системи
echo 5. Згенерувати QR-код для телефону
echo 6. Вихід
echo.

set /p choice="Ваш вибір (1-6): "

if "%choice%"=="1" (
    echo.
    echo 🚀 Запуск веб-інтерфейсу...
    echo 📱 Для доступу з телефону дивіться адресу в консолі
    echo Для зупинки: Ctrl+C
    echo.
    python web_app.py
) else if "%choice%"=="2" (
    echo.
    python meter_processor.py
    pause
) else if "%choice%"=="3" (
    echo.
    python batch_processor.py
    pause
) else if "%choice%"=="4" (
    echo.
    python test_system.py
    pause
) else if "%choice%"=="5" (
    echo.
    python generate_qr.py
    echo.
    pause
) else if "%choice%"=="6" (
    echo.
    echo 👋 До побачення!
    exit /b 0
) else (
    echo.
    echo ❌ Невірний вибір
    pause
    exit /b 1
)
