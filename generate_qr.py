#!/usr/bin/env python3
"""
Генерація QR-коду для швидкого підключення з телефону
"""

import socket
import sys

def get_local_ip():
    """Отримує локальну IP-адресу"""
    try:
        # Створюємо сокет для визначення IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return socket.gethostbyname(socket.gethostname())


def generate_qr_code(url):
    """Генерує QR-код для URL"""
    try:
        import qrcode
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        # Створюємо зображення
        img = qr.make_image(fill_color="black", back_color="white")
        img.save('qr_code.png')
        
        # Виводимо в консоль (ASCII арт)
        qr_ascii = qrcode.QRCode()
        qr_ascii.add_data(url)
        qr_ascii.make()
        qr_ascii.print_ascii()
        
        return True
    except ImportError:
        return False


def main():
    print("\n" + "="*60)
    print("  📱 ПІДКЛЮЧЕННЯ З ТЕЛЕФОНУ - QR КОД")
    print("="*60)
    
    # Отримуємо IP-адресу
    local_ip = get_local_ip()
    url = f"http://{local_ip}:5000"
    
    print(f"\n🌐 URL для підключення:")
    print(f"   {url}")
    print(f"\n📋 IP-адреса вашого комп'ютера: {local_ip}")
    
    # Спроба згенерувати QR-код
    print(f"\n📊 Генерація QR-коду...")
    
    if generate_qr_code(url):
        print(f"\n✅ QR-код створено!")
        print(f"   📁 Файл збережено: qr_code.png")
        print(f"\n📱 Відскануйте QR-код камерою телефону для швидкого доступу")
    else:
        print(f"\n⚠️  Модуль qrcode не встановлено")
        print(f"   Встановіть: pip install qrcode[pil]")
        print(f"\n📱 Відкрийте на телефоні вручну:")
        print(f"   {url}")
    
    print("\n" + "="*60)
    print("  🔧 ІНСТРУКЦІЯ:")
    print("="*60)
    print("""
1. Переконайтесь, що телефон і комп'ютер в одній Wi-Fi мережі
2. Запустіть веб-сервер: python web_app.py
3. На телефоні:
   • Відскануйте QR-код камерою
   • АБО введіть URL в браузері
4. Готово! Можна фотографувати лічильники
    """)
    
    print("="*60 + "\n")


if __name__ == '__main__':
    main()
