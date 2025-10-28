import services

if __name__ == "__main__":
    services.set_schedule_path('src/23102025.xls')
    services.send_shcedule()
    services.DB.close_db()