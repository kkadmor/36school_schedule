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
    html = ''
    list_of_lessons_time = ['8:00 - 8:40', '8:50 - 9:30', '9:50 - 10:30', 
                            '10:45 - 11:25', '11:40 - 12:20', '12:30 - 13:10', 
                            '13:15 - 13:55', '14:00 - 14:40', '14:50 - 15:30',
                            '15:45 - 16:25', '16:40 - 17:20', '17:30 - 18:10', 
                            '18:20 - 19:00']
    number_of_lesson = 1
    for lesson in schedule:
        lesson = lesson.replace('\n', '')
        html += f'''
        <b>{number_of_lesson} <small>[{list_of_lessons_time[number_of_lesson-1]}]:</small></b> {lesson}<br>
        '''

        number_of_lesson += 1

    html += f'''
    </tbody>
    </table>
    '''
    return html

    
    
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
    if DB.get_email_by_name(name) == None:
        print('Отсутствует почта!', name)
        return

    login = os.getenv('LOGIN')
    password = os.getenv('PASSWORD')
    from_addr = os.getenv('FROM_ADDR')
    port = os.getenv('PORT')

    html = schedule_to_html(get_schedule_by_teacher(name))

    Email.send_simple_email(
        smtp_server='smtp.gmail.com',
        port=port,
        login=login,
        password=password,
        from_addr=from_addr,
        to_addr=DB.get_email_by_name(name),
        subject='Расписание',
        body=html
    )



def send_shcedule():
    teachers_dict = Exel.get_data_to_exel(schedule_path)
    for teacher in teachers_dict:
        send_shedule_to_teacher_by_name(teacher)


if __name__ == '__main__':
    set_schedule_path('src/23102025.xls')
    send_shcedule()