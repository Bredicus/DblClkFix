from typing import Any
import os.path
import json
import base64
import b64_icon

path = os.path.join('C:' + os.sep, 'Users', os.getlogin(), 'AppData', 'Roaming', 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup', 'dblclkfix_start.bat')
settings_path = 'dblclkfix.json'

def get_win_startup() -> bool:
    return os.path.exists(path)


def set_win_startup(set: bool = True) -> None:
    if False == set:
        os.remove(path)
    else:
        file_name = 'DblClkFix.exe'
        output = os.popen('wmic process get description, processid').read()
        output = output.splitlines()

        for line in output:
            line = ' '.join(line.split())

            if len(line) > 0 and line.startswith(file_name):
                file_path = os.popen('wmic process where "ProcessId=' + line.split()[1] + '" get ExecutablePath').read()
                for ch in ["b'ExecutablePath", "ExecutablePath", "\\r\\n", "\\" + file_name]:
                    if ch in file_path:
                        file_path = file_path.replace(ch, '')

                file_path = file_path[:-1]
                file_path = file_path.strip()
                            
                with open(path, 'w') as f:
                    f.write(r'cd %s' % file_path)
                    f.write('\n')
                    f.write(r'start "" "%s"' % file_name)
                
                break


def toggle_win_startup() -> None:
    is_set = get_win_startup()
    set = True

    if is_set:
        set = False

    set_win_startup(set)


def represents_int(str: str) -> bool:
    try: 
        int(str)
        return True
    except ValueError:
        return False


def get_valid_time_limit(time_limit: Any, default: int) -> int:
    if represents_int(time_limit):
        time_limit = int(time_limit)
        if time_limit > 0 and time_limit < 250:
            return time_limit
    return default


def get_valid_check_value(check_value: Any) -> bool:
    if True == check_value or False == check_value:
        return check_value
    return True


def get_settings() -> dict:
    settings = {
        'mouse_check_l': True,
        'mouse_check_r' : True,
        'time_limit_l': 50,
        'time_limit_r': 50,
        'time_limit_mouse_up_l': 50,
        'time_limit_mouse_up_r': 50
    }

    if os.path.exists(settings_path):
        with open(settings_path) as f:
            try:
                data = json.load(f)
            except ValueError as e:
                return settings

        settings['mouse_check_l'] = get_valid_check_value(data.get('mouse_check_l', True))
        settings['mouse_check_r'] = get_valid_check_value(data.get('mouse_check_r', True))
        settings['time_limit_l'] = get_valid_time_limit(data.get('time_limit_l', 50), settings['time_limit_l'])
        settings['time_limit_r'] = get_valid_time_limit(data.get('time_limit_r', 50), settings['time_limit_r'])
        settings['time_limit_mouse_up_l'] = get_valid_time_limit(data.get('time_limit_mouse_up_l', 50), settings['time_limit_mouse_up_l'])
        settings['time_limit_mouse_up_r'] = get_valid_time_limit(data.get('time_limit_mouse_up_r', 50), settings['time_limit_mouse_up_r'])
    
    return settings


def json_write_to_file(data: dict) -> None:
    with open(settings_path, 'w') as f:
        json.dump(data, f, indent=4)


def check_icon_file() -> None:
    if not os.path.exists('dblclkfix.ico'):
        icon_data = base64.b64decode(b64_icon.dcf_icon)
        new_icon_file = open('dblclkfix.ico', 'wb')
        new_icon_file.write(icon_data)
        new_icon_file.close()

    del b64_icon.dcf_icon 
