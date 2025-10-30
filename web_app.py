#!/usr/bin/env python3
"""
Веб-інтерфейс для обробки фотографій лічильників
"""

from flask import Flask, render_template, request, jsonify, send_file
from meter_processor import MeterProcessor
import os
from werkzeug.utils import secure_filename
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/home/claude/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}

# Створюємо папку для завантажень
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Ініціалізуємо процесор
processor = MeterProcessor('lichilnyky.xlsx')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """Обробка завантаженого фото"""
    if 'file' not in request.files:
        return jsonify({'error': 'Файл не знайдено'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'Файл не вибрано'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Обробляємо фото
            data = processor.process_image(filepath)
            
            # Опціонально - видаляємо файл після обробки
            # os.remove(filepath)
            
            return jsonify({
                'success': True,
                'data': data,
                'message': 'Фото успішно оброблено!'
            })
        
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    return jsonify({'error': 'Недопустимий формат файлу'}), 400


@app.route('/update', methods=['POST'])
def update_data():
    """Оновлення даних вручну"""
    data = request.json
    filename = data.get('filename')
    
    if not filename:
        return jsonify({'error': 'Назва файлу не вказана'}), 400
    
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))
    
    manual_data = {
        'brand': data.get('brand', ''),
        'serial_number': data.get('serial_number', ''),
        'year': data.get('year', ''),
        'reading': data.get('reading', '')
    }
    
    try:
        result = processor.process_image(filepath, manual_data)
        return jsonify({
            'success': True,
            'data': result,
            'message': 'Дані оновлено!'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/download')
def download_excel():
    """Завантаження Excel файлу"""
    try:
        return send_file(
            processor.excel_file,
            as_attachment=True,
            download_name='lichilnyky.xlsx',
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    import socket
    
    # Отримуємо IP-адресу комп'ютера
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    print("\n" + "="*60)
    print("  🚀 ВЕБ-СЕРВЕР ЗАПУЩЕНО!")
    print("="*60)
    print(f"\n📱 Для доступу з телефону відкрийте в браузері:")
    print(f"   http://{local_ip}:5000")
    print(f"\n💻 Для доступу з цього комп'ютера:")
    print(f"   http://localhost:5000")
    print(f"   http://127.0.0.1:5000")
    print("\n⚠️  Переконайтесь, що телефон підключений до тієї ж Wi-Fi мережі!")
    print("\n🛑 Для зупинки: Ctrl+C")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
