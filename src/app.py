from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
import threading
from services import set_schedule_path, send_shcedule
import DB

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/db-management')
def db_management():
    teachers = DB.get_all_teachers()
    return render_template('db_management.html', teachers=teachers)

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'schedule_file' not in request.files:
            return jsonify({"success": False, "message": "Файл не выбран"})
        
        file = request.files['schedule_file']
        
        if file.filename == '':
            return jsonify({"success": False, "message": "Файл не выбран"})
        
        if not file.filename.lower().endswith(('.xlsx', '.xls')):
            return jsonify({"success": False, "message": "Только Excel файлы (.xlsx, .xls)"})
        
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        
        set_schedule_path(file_path)
        
        return jsonify({"success": True, "message": f"Файл {file.filename} успешно загружен! Теперь можно запустить рассылку."})
    
    except Exception as e:
        return jsonify({"success": False, "message": f"Ошибка загрузки: {str(e)}"})

@app.route('/send_schedule', methods=['POST'])
def send_schedule():
    try:
        # Запускаем рассылку и получаем результат
        result = send_shcedule()
        
        if result["success"]:
            message = f"Рассылка завершена! Успешно отправлено: {result['sent_count']}/{result['total_count']}"
            
            # Если есть преподаватели без email, добавляем информацию о них
            if result['missing_emails']:
                message += f". Отсутствуют email для {len(result['missing_emails'])} преподавателей."
            
            return jsonify({
                "success": True, 
                "message": message,
                "details": result
            })
        else:
            return jsonify({
                "success": False, 
                "message": f"Ошибка рассылки: {result.get('error', 'Неизвестная ошибка')}",
                "details": result
            })
    
    except Exception as e:
        return jsonify({"success": False, "message": f"Ошибка рассылки: {str(e)}"})

@app.route('/add_teacher', methods=['POST'])
def add_teacher():
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        
        if not name or not email:
            return jsonify({"success": False, "message": "Заполните все поля"})
        
        DB.add_teacher(name, email)
        return jsonify({"success": True, "message": f"Преподаватель {name} успешно добавлен!"})
    
    except Exception as e:
        return jsonify({"success": False, "message": f"Ошибка добавления: {str(e)}"})

@app.route('/delete_teacher', methods=['POST'])
def delete_teacher():
    try:
        name = request.form.get('name')
        
        if not name:
            return jsonify({"success": False, "message": "Имя преподавателя не указано"})
        
        DB.delete_teacher_by_name(name)
        return jsonify({"success": True, "message": f"Преподаватель {name} успешно удален!"})
    
    except Exception as e:
        return jsonify({"success": False, "message": f"Ошибка удаления: {str(e)}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)