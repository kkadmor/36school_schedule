import os
from dotenv import load_dotenv

import Exel
import Email
from DB import DB

PATH_TO_EXEL = 'src/23102025.xls'

load_dotenv()

db = DB()

def get_schedule_by_teacher(teacher:str):
    teacher_dict = Exel.get_data_to_exel(PATH_TO_EXEL)
    try:
        return teacher_dict[teacher]
    except:
        return -1
    
def send_shedule_to_teacher(name:str, email:str):
    list_of_lessons_time = ['8:00 - 8:40', '8:50 - 9:30', '9:50 - 10:30', 
                            '10:45 - 11:25', '11:40 - 12:20', '12:30 - 13:10', 
                            '13:15 - 13:55', '14:00 - 14:40', '14:50 - 15:30',
                            '15:45 - 16:25', '16:40 - 17:20', '17:30 - 18:10', 
                            '18:20 - 19:00']

    text = name + '\n'
    number_of_lesson = 1
    for lesson in get_schedule_by_teacher(name):
        lesson = lesson.replace('\n', ' ')

        text += str(number_of_lesson) + f' [{list_of_lessons_time[number_of_lesson-1]}]: ' + lesson + '\n'

        number_of_lesson += 1

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
        body=text
    )
    
def send_shedule_to_teacher_by_name(name:str):
    list_of_lessons_time = ['8:00 - 8:40', '8:50 - 9:30', '9:50 - 10:30', 
                            '10:45 - 11:25', '11:40 - 12:20', '12:30 - 13:10', 
                            '13:15 - 13:55', '14:00 - 14:40', '14:50 - 15:30',
                            '15:45 - 16:25', '16:40 - 17:20', '17:30 - 18:10', 
                            '18:20 - 19:00']

    text = name + '\n'
    number_of_lesson = 1
    for lesson in get_schedule_by_teacher(name):
        lesson = lesson.replace('\n', '')

        text += str(number_of_lesson) + f' [{list_of_lessons_time[number_of_lesson-1]}]: ' + lesson + '\n'

        number_of_lesson += 1

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
        to_addr=db.get_email_by_name(name),
        subject='Расписание',
        body=text
    )

if __name__ == "__main__":

    send_shedule_to_teacher_by_name('Карач В.А.')