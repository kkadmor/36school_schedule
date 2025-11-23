import os
import pandas as pd

teachers_list = []

def parse_excel_to_dict_list(filepath: str, sheet_name='Лист1'):
    df = pd.read_excel(filepath, sheet_name=sheet_name)

    dict_list = df.to_dict(orient='records')

    return dict_list

def get_data_to_exel(path:str):
    schedule = parse_excel_to_dict_list(path)
    teachers_dict = {}
    for teacher in schedule:
        if not pd.isna(teacher['Unnamed: 1']) and teacher['Unnamed: 1'] != 'Преподаватель':
            lessons = []
            for i in range(17):
                if i+1 not in [1, 2, 15, 16]:
                    if pd.isna(teacher[f'Unnamed: {i+1}']):
                        lessons.append('Окно')
                    else:
                        lessons.append(str(teacher[f'Unnamed: {i+1}']))
            teachers_dict[str(teacher['Unnamed: 1'])] = lessons
    return teachers_dict
    
        
if __name__ == "__main__":
    get_data_to_exel('src/23102025.xls')