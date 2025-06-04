from datetime import datetime

def check_current_time():
    return datetime.now().strftime('%Y-%m-%d %H-%M-%S')
