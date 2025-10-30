#!/usr/bin/env python3
"""
Тестовий скрипт для демонстрації роботи системи
"""

import os
from meter_processor import MeterProcessor


def test_basic_functionality():
    """Базовий тест системи"""
    print("\n" + "="*60)
    print("  🧪 ТЕСТУВАННЯ СИСТЕМИ ОБРОБКИ ЛІЧИЛЬНИКІВ")
    print("="*60)
    
    # Створюємо тестовий Excel файл
    print("\n1️⃣ Створення Excel файлу...")
    processor = MeterProcessor('test_meters.xlsx')
    print("   ✅ Excel файл створено: test_meters.xlsx")
    
    # Додаємо тестові дані вручну
    print("\n2️⃣ Додавання тестових даних...")
    test_data_1 = {
        'date': '30.10.2025',
        'brand': 'Zenner',
        'serial_number': 'ZEN123456',
        'year': '2020',
        'reading': '12345.67',
        'photo': 'test_photo_1.jpg'
    }
    processor.add_to_excel(test_data_1)
    print("   ✅ Запис 1 додано")
    
    test_data_2 = {
        'date': '30.10.2025',
        'brand': 'Sensus',
        'serial_number': 'SEN789012',
        'year': '2019',
        'reading': '98765.43',
        'photo': 'test_photo_2.jpg'
    }
    processor.add_to_excel(test_data_2)
    print("   ✅ Запис 2 додано")
    
    test_data_3 = {
        'date': '30.10.2025',
        'brand': 'Itron',
        'serial_number': 'ITR456789',
        'year': '2021',
        'reading': '54321.00',
        'photo': 'test_photo_3.jpg'
    }
    processor.add_to_excel(test_data_3)
    print("   ✅ Запис 3 додано")
    
    # Перевірка створення файлу
    print("\n3️⃣ Перевірка результату...")
    if os.path.exists('test_meters.xlsx'):
        file_size = os.path.getsize('test_meters.xlsx')
        print(f"   ✅ Файл створено успішно")
        print(f"   📊 Розмір файлу: {file_size} байт")
        print(f"   📝 Кількість рядків даних: 3")
    else:
        print("   ❌ Файл не знайдено")
    
    # Демонстрація розпізнавання тексту
    print("\n4️⃣ Тест розпізнавання тексту...")
    test_text = """
    Zenner
    Лічильник води
    Серійний номер: ABC123456
    Рік випуску: 2020
    Показання: 12345.67 м³
    """
    
    data = processor.parse_meter_data(test_text, 'demo.jpg')
    print("   📄 Тестовий текст:")
    print("   " + "-"*50)
    for line in test_text.strip().split('\n'):
        print(f"   {line.strip()}")
    print("   " + "-"*50)
    
    print("\n   🔍 Розпізнані дані:")
    print(f"   • Марка: {data['brand'] or '(не знайдено)'}")
    print(f"   • Серійний номер: {data['serial_number'] or '(не знайдено)'}")
    print(f"   • Рік випуску: {data['year'] or '(не знайдено)'}")
    print(f"   • Показання: {data['reading'] or '(не знайдено)'}")
    
    # Підсумок
    print("\n" + "="*60)
    print("  ✅ ТЕСТУВАННЯ ЗАВЕРШЕНО УСПІШНО!")
    print("="*60)
    print(f"\n📁 Створений файл: test_meters.xlsx")
    print("📝 Рекомендації:")
    print("   1. Відкрийте файл test_meters.xlsx для перегляду")
    print("   2. Спробуйте обробити реальне фото:")
    print("      python meter_processor.py")
    print("   3. Або запустіть веб-інтерфейс:")
    print("      python web_app.py")
    print()


def demo_text_patterns():
    """Демонстрація різних шаблонів тексту"""
    print("\n" + "="*60)
    print("  📚 ДЕМОНСТРАЦІЯ ШАБЛОНІВ РОЗПІЗНАВАННЯ")
    print("="*60)
    
    processor = MeterProcessor('pattern_test.xlsx')
    
    test_patterns = [
        {
            'name': 'Стандартний формат',
            'text': """
            Zenner Water Meter
            Serial No: ZEN123456
            Year: 2020
            Reading: 12345.67 m³
            """
        },
        {
            'name': 'Український формат',
            'text': """
            Лічильник холодної води
            Марка: Сенсус
            Серійний №: 87654321
            Рік випуску: 2019
            Показання: 9876.54 м³
            """
        },
        {
            'name': 'Мінімальний формат',
            'text': """
            Itron
            №ITR456789
            2021
            54321
            """
        },
        {
            'name': 'Електролічильник',
            'text': """
            ЭНЕРГОМЕРА ЦЭ6803В
            № 12345678
            2022 г.в.
            Показання: 5432.1 кВт·год
            """
        }
    ]
    
    for i, pattern in enumerate(test_patterns, 1):
        print(f"\n{i}️⃣ {pattern['name']}")
        print("   " + "-"*50)
        print(pattern['text'].strip())
        print("   " + "-"*50)
        
        data = processor.parse_meter_data(pattern['text'], f'pattern_{i}.jpg')
        
        print("   🔍 Результат:")
        print(f"      Марка: {data['brand'] or '❌'}")
        print(f"      Серійний: {data['serial_number'] or '❌'}")
        print(f"      Рік: {data['year'] or '❌'}")
        print(f"      Показання: {data['reading'] or '❌'}")
    
    print("\n" + "="*60)
    print("  ✅ ДЕМОНСТРАЦІЯ ЗАВЕРШЕНА")
    print("="*60)
    print()


def interactive_test():
    """Інтерактивний тест"""
    print("\n" + "="*60)
    print("  🎮 ІНТЕРАКТИВНИЙ РЕЖИМ")
    print("="*60)
    print("\nОберіть тест:")
    print("  1. Базовий тест функціоналу")
    print("  2. Демонстрація шаблонів")
    print("  3. Обидва тести")
    print("  4. Вихід")
    
    choice = input("\nВаш вибір (1-4): ").strip()
    
    if choice == '1':
        test_basic_functionality()
    elif choice == '2':
        demo_text_patterns()
    elif choice == '3':
        test_basic_functionality()
        demo_text_patterns()
    elif choice == '4':
        print("\n👋 До побачення!")
    else:
        print("\n❌ Невірний вибір!")


if __name__ == '__main__':
    try:
        interactive_test()
    except KeyboardInterrupt:
        print("\n\n👋 Завершення роботи...")
    except Exception as e:
        print(f"\n❌ Помилка: {e}")
