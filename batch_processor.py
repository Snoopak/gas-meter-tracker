#!/usr/bin/env python3
"""
Скрипт для пакетної обробки фотографій лічильників
"""

from meter_processor import MeterProcessor
import os
import glob
from pathlib import Path


def process_folder(folder_path, excel_file='lichilnyky.xlsx'):
    """Обробляє всі фото лічильників в папці"""
    
    # Підтримувані формати зображень
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff', '*.tif']
    
    # Знаходимо всі фото в папці
    image_files = []
    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join(folder_path, ext)))
        image_files.extend(glob.glob(os.path.join(folder_path, ext.upper())))
    
    if not image_files:
        print(f"❌ У папці '{folder_path}' не знайдено фотографій")
        return
    
    print(f"\n{'='*60}")
    print(f"Знайдено {len(image_files)} фото для обробки")
    print(f"{'='*60}")
    
    # Створюємо процесор
    processor = MeterProcessor(excel_file)
    
    # Обробляємо кожне фото
    successful = 0
    failed = 0
    
    for i, image_path in enumerate(image_files, 1):
        print(f"\n[{i}/{len(image_files)}]", end=" ")
        try:
            processor.process_image(image_path)
            successful += 1
        except Exception as e:
            print(f"❌ Помилка при обробці {os.path.basename(image_path)}: {e}")
            failed += 1
    
    # Підсумок
    print(f"\n{'='*60}")
    print(f"✅ Обробка завершена!")
    print(f"{'='*60}")
    print(f"  Успішно оброблено: {successful}")
    print(f"  Помилки: {failed}")
    print(f"  Дані збережено в: {excel_file}")


def interactive_mode():
    """Інтерактивний режим з меню"""
    print("\n" + "="*60)
    print("  📷 ОБРОБКА ФОТОГРАФІЙ ЛІЧИЛЬНИКІВ")
    print("="*60)
    print("\nОберіть режим роботи:")
    print("  1. Обробити одне фото")
    print("  2. Обробити всі фото в папці")
    print("  3. Вихід")
    
    choice = input("\nВаш вибір (1-3): ").strip()
    
    if choice == '1':
        image_path = input("\nВведіть шлях до фото: ").strip()
        if os.path.exists(image_path):
            excel_file = input("Назва Excel файлу (Enter для 'lichilnyky.xlsx'): ").strip() or 'lichilnyky.xlsx'
            processor = MeterProcessor(excel_file)
            processor.process_image(image_path)
        else:
            print(f"❌ Файл не знайдено: {image_path}")
    
    elif choice == '2':
        folder_path = input("\nВведіть шлях до папки з фото: ").strip()
        if os.path.isdir(folder_path):
            excel_file = input("Назва Excel файлу (Enter для 'lichilnyky.xlsx'): ").strip() or 'lichilnyky.xlsx'
            process_folder(folder_path, excel_file)
        else:
            print(f"❌ Папку не знайдено: {folder_path}")
    
    elif choice == '3':
        print("\n👋 До побачення!")
        return
    
    else:
        print("❌ Невірний вибір!")


if __name__ == '__main__':
    interactive_mode()
