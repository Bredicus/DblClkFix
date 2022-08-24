from functions import get_win_startup, set_win_startup, toggle_win_startup, get_settings, json_write_to_file, check_icon_file
from pynput import mouse
from PIL import Image
from pystray import MenuItem as item
import pystray

check_icon_file()
run_on_win_startup = get_win_startup()
if True == run_on_win_startup:
    set_win_startup(False)
    set_win_startup(True)

settings = get_settings()
mouse_check_l = settings['mouse_check_l']
mouse_check_r = settings['mouse_check_r']
time_limit_l = settings['time_limit_l']
time_limit_r = settings['time_limit_r']
time_limit_mouse_up_l = settings['time_limit_mouse_up_l']
time_limit_mouse_up_r = settings['time_limit_mouse_up_r']
settings.clear()
del settings

# type_1: double click caused by multiple mouse down and mouse up events
last_time_l_t1 = 0
last_time_r_t1 = 0

# type_2: double click caused by multiple mouse down events
last_time_l_t2 = 0
last_time_r_t2 = 0

# type_3: double click caused by multiple mouse up events
last_time_l_t3 = 0
last_time_r_t3 = 0

def win32_event_filter(msg: int, data: dict) -> None:
    global mouse_check_l
    global mouse_check_r
    global time_limit_l
    global time_limit_r
    global time_limit_mouse_up_l
    global time_limit_mouse_up_r

    global last_time_l_t1
    global last_time_r_t1

    global last_time_l_t2
    global last_time_r_t2

    global last_time_l_t3
    global last_time_r_t3

    suppress = False

    ### left click start
    # left down
    if True == mouse_check_l:
        if 513 == msg:
            # type_1
            if time_limit_l >= data.time - last_time_l_t1:
                suppress = True

            # type_2
            if time_limit_l >= data.time - last_time_l_t2:
                suppress = True
            last_time_l_t2 = data.time
        # left up
        if 514 == msg:
            # type_1
            last_time_l_t1 = data.time

            # type_3
            if time_limit_mouse_up_l >= data.time - last_time_l_t3:
                suppress = True
            last_time_l_t3 = data.time
    ### left click end

    ### right click start
    # right down
    if True == mouse_check_r:
        if 516 == msg:
            # type_1
            if time_limit_r >= data.time - last_time_r_t1:
                suppress = True

            # type_2
            if time_limit_r >= data.time - last_time_r_t2:
                suppress = True
            last_time_r_t2 = data.time
        # right up
        if 517 == msg:
            # type_1
            last_time_r_t1 = data.time

            # type_3
            if time_limit_mouse_up_r >= data.time - last_time_r_t3:
                suppress = True
            last_time_r_t3 = data.time
    ### right click end

    if True == suppress:
        listener.suppress_event()

listener = mouse.Listener(win32_event_filter=win32_event_filter)
listener.start()


def win_start_up_toggle() -> None:
    global run_on_win_startup
    toggle_win_startup()
    run_on_win_startup = get_win_startup()

def set_mouse_check_l() -> None:
    global mouse_check_l
    mouse_check_l = not mouse_check_l
    settings = get_settings()
    settings['mouse_check_l'] = mouse_check_l
    json_write_to_file(settings)


def set_mouse_check_r() -> None:
    global mouse_check_r
    mouse_check_r = not mouse_check_r
    settings = get_settings()
    settings['mouse_check_r'] = mouse_check_r
    json_write_to_file(settings)


def exit_app() -> None:
    listener.stop()
    icon.stop()

menu = (
    item('Run on Windows Startup', win_start_up_toggle, checked=lambda item: run_on_win_startup),
    item('Left Click', set_mouse_check_l, checked=lambda item: mouse_check_l),
    item('Right Click', set_mouse_check_r, checked=lambda item: mouse_check_r),
    item('Exit', exit_app)
)
icon = pystray.Icon('DoubleClickFix', Image.open('dblclkfix.ico'), 'DoubleClickFix', menu)
icon.run()
