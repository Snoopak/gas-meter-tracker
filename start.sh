#!/bin/bash
# Скрипт швидкого запуску системи обробки лічильників

echo "=================================="
echo "  📷 Система обробки лічильників"
echo "=================================="
echo ""

# Перевірка Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 не знайдено. Встановіть Python 3.8 або новіше."
    exit 1
fi

echo "✅ Python знайдено: $(python3 --version)"

# Перевірка Tesseract
if ! command -v tesseract &> /dev/null; then
    echo "⚠️  Tesseract OCR не знайдено."
    echo "   Встановіть командою:"
    echo "   Ubuntu/Debian: sudo apt-get install tesseract-ocr tesseract-ocr-ukr"
    echo "   macOS: brew install tesseract tesseract-lang"
    echo "   Windows: завантажте з https://github.com/UB-Mannheim/tesseract/wiki"
    read -p "Продовжити без Tesseract? (y/n): " continue
    if [ "$continue" != "y" ]; then
        exit 1
    fi
else
    echo "✅ Tesseract знайдено: $(tesseract --version | head -n1)"
fi

# Перевірка залежностей
echo ""
echo "Перевірка Python залежностей..."

if ! python3 -c "import cv2" 2>/dev/null; then
    echo "⚠️  Не всі залежності встановлено."
    read -p "Встановити залежності зараз? (y/n): " install
    if [ "$install" = "y" ]; then
        echo "Встановлення..."
        pip3 install -r requirements.txt
        if [ $? -eq 0 ]; then
            echo "✅ Залежності встановлено"
        else
            echo "❌ Помилка встановлення залежностей"
            exit 1
        fi
    fi
else
    echo "✅ Залежності встановлено"
fi

# Меню вибору
echo ""
echo "=================================="
echo "Оберіть режим роботи:"
echo "=================================="
echo "1. Веб-інтерфейс (рекомендовано)"
echo "2. Обробка одного фото"
echo "3. Пакетна обробка папки"
echo "4. Тестування системи"
echo "5. Згенерувати QR-код для телефону"
echo "6. Вихід"
echo ""

read -p "Ваш вибір (1-6): " choice

case $choice in
    1)
        echo ""
        echo "🚀 Запуск веб-інтерфейсу..."
        echo "📱 Для доступу з телефону дивіться адресу в консолі"
        echo "Для зупинки: Ctrl+C"
        echo ""
        python3 web_app.py
        ;;
    2)
        echo ""
        python3 meter_processor.py
        ;;
    3)
        echo ""
        python3 batch_processor.py
        ;;
    4)
        echo ""
        python3 test_system.py
        ;;
    5)
        echo ""
        python3 generate_qr.py
        echo ""
        read -p "Натисніть Enter для продовження..."
        ;;
    6)
        echo ""
        echo "👋 До побачення!"
        exit 0
        ;;
    *)
        echo ""
        echo "❌ Невірний вибір"
        exit 1
        ;;
esac
