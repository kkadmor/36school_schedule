import os
from dotenv import load_dotenv

import Exel
import Email
import DB

load_dotenv()

schedule_path = ''

def set_schedule_path(path:str):
    global schedule_path
    schedule_path=path

def get_schedule_path():
    return schedule_path

def get_schedule_by_teacher(teacher:str):
    teacher_dict = Exel.get_data_to_exel(schedule_path)
    try:
        return teacher_dict[teacher]
    except:
        return -1
    
def schedule_to_html(schedule:list):
    if schedule == -1:
        return "<p>Расписание не найдено</p>"
    
    list_of_lessons_time = ['8:00 - 8:40', '8:50 - 9:30', '9:50 - 10:30', 
                            '10:45 - 11:25', '11:40 - 12:20', '12:30 - 13:10', 
                            '13:15 - 13:55', '14:00 - 14:40', '14:50 - 15:30',
                            '15:45 - 16:25', '16:40 - 17:20', '17:30 - 18:10', 
                            '18:20 - 19:00']
    
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {
                font-family: 'Arial', sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #ffffff;
            }
            .schedule-table {
                width: 100%;
                border-collapse: collapse;
                font-size: 14px;
            }
            .schedule-table th {
                background-color: #f8f9fa;
                padding: 12px 8px;
                text-align: left;
                border-bottom: 2px solid #dee2e6;
                color: #495057;
                font-weight: 600;
            }
            .schedule-table td {
                padding: 10px 8px;
                border-bottom: 1px solid #e9ecef;
            }
            .lesson-number {
                font-weight: bold;
                color: #495057;
                width: 30px;
            }
            .lesson-time {
                color: #6c757d;
                font-size: 12px;
                width: 100px;
            }
            .lesson-content {
                color: #212529;
            }
            .window {
                color: #6c757d;
                font-style: italic;
            }
            .lesson-row:hover {
                background-color: #f8f9fa;
            }
            .subject {
                font-weight: 500;
                color: #2c3e50;
            }
            .classroom {
                color: #e74c3c;
                font-size: 11px;
                margin-top: 2px;
            }
        </style>
    </head>
    <body>
        <table class="schedule-table">
            <thead>
                <tr>
                    <th>№</th>
                    <th>Время</th>
                    <th>Занятие</th>
                </tr>
            </thead>
            <tbody>
    """
    
    for i, lesson in enumerate(schedule):
        lesson = lesson.replace('\n', '').strip()
        lesson_number = i + 1
        lesson_time = list_of_lessons_time[i]
        
        is_window = lesson.lower() in ['окно', '']
        
        subject, classroom = parse_lesson_info(lesson)
        
        row_class = "window" if is_window else "lesson-row"
        lesson_display = "Окно" if is_window else lesson
        
        html += f"""
                <tr class="{row_class}">
                    <td class="lesson-number">{lesson_number}</td>
                    <td class="lesson-time">{lesson_time}</td>
                    <td class="lesson-content">{lesson if lesson else 'Окно'}</td>
                </tr>
        """
    
    html += """
            </tbody>
        </table>
    </body>
    </html>
    """
    
    return html


def parse_lesson_info(lesson_text):
    """
    Парсит текст урока и разделяет на предмет и аудиторию
    Пример: "8а,8б,8в,8ж(2-403(инф))" -> ("8а,8б,8в,8ж", "2-403(инф)")
    """
    if not lesson_text or lesson_text.lower() == 'окно':
        return "Окно", ""
    
    # Ищем последнюю открывающую скобку для разделения
    last_open_bracket = lesson_text.rfind('(')
    
    if last_open_bracket != -1:
        subject = lesson_text[:last_open_bracket].strip()
        classroom = lesson_text[last_open_bracket:].strip('()')
        
        # Если в названии аудитории есть внутренние скобки, убираем их
        classroom = classroom.replace('(', '').replace(')', '')
    else:
        subject = lesson_text
        classroom = ""
    
    return subject, classroom


def get_current_date():
    from datetime import datetime
    months = {
        1: 'января', 2: 'февраля', 3: 'марта', 4: 'апреля',
        5: 'мая', 6: 'июня', 7: 'июля', 8: 'августа',
        9: 'сентября', 10: 'октября', 11: 'ноября', 12: 'декабря'
    }
    days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    
    now = datetime.now()
    day_name = days[now.weekday()]
    day = now.day
    month = months[now.month]
    year = now.year
    
    return f"{day_name}, {day} {month} {year} года"


def parse_lesson_info(lesson_text):
    if not lesson_text or lesson_text.lower() == 'окно':
        return "Окно", ""
    
    last_open_bracket = lesson_text.rfind('(')
    
    if last_open_bracket != -1:
        subject = lesson_text[:last_open_bracket].strip()
        classroom = lesson_text[last_open_bracket:].strip('()')
        
        classroom = classroom.replace('(', '').replace(')', '')
    else:
        subject = lesson_text
        classroom = "Аудитория не указана"
    
    return subject, classroom

    
    
def send_shedule_to_teacher(name:str, email:str):

    html = schedule_to_html(get_schedule_by_teacher(name))

    login = os.getenv('LOGIN')
    password = os.getenv('PASSWORD')
    from_addr = os.getenv('FROM_ADDR')
    port = os.getenv('PORT')

    Email.send_simple_email(
        smtp_server='smtp.gmail.com',
        port=port,
        login=login,
        password=password,
        from_addr=from_addr,
        to_addr=email,
        subject='Расписание',
        body=html
    )
    
def send_shedule_to_teacher_by_name(name:str):
    try:
        # Эта функция создает свое соединение с БД
        email = DB.get_email_by_name(name)
        if email is None:
            print(f'Отсутствует почта для: {name}')
            return False, name  # Возвращаем статус и имя преподавателя

        success = send_shedule_to_teacher(name, email)
        return success, None
    except Exception as e:
        print(f"Ошибка отправки письма для {name}: {e}")
        return False, name

def send_shcedule():
    try:
        if not schedule_path:
            print("Ошибка: путь к расписанию не установлен")
            return {"success": False, "error": "Путь к расписанию не установлен", "missing_emails": []}
        
        print("Начало рассылки...")
        teachers_dict = Exel.get_data_to_exel(schedule_path)
        
        success_count = 0
        total_count = len(teachers_dict)
        missing_emails = []  # Список преподавателей без email
        
        for teacher in teachers_dict:
            success, missing_teacher = send_shedule_to_teacher_by_name(teacher)
            if success:
                success_count += 1
            elif missing_teacher:
                missing_emails.append(missing_teacher)
        
        result = {
            "success": True,
            "sent_count": success_count,
            "total_count": total_count,
            "missing_emails": missing_emails
        }
        
        print(f"Рассылка завершена. Успешно отправлено: {success_count}/{total_count}")
        if missing_emails:
            print(f"Отсутствуют email для: {', '.join(missing_emails)}")
        
        return result
        
    except Exception as e:
        print(f"Ошибка в процессе рассылки: {e}")
        return {"success": False, "error": str(e), "missing_emails": []}



if __name__ == '__main__':
    set_schedule_path('src/23102025.xls')
    send_shcedule()