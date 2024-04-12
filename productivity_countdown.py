import tkinter as tk
from tkinter import ttk
import time
import datetime
from threading import Thread
import win32api
import sqlite3


WINDOW_WIDTH = 200
WINDOW_HEIGHT = 150
PROGRESSBAR_THICKNESS = 10
WORKING_TIME_LIMIT_IN_SECONDS = 8 * 3600
DB_FILE = "data.db"

# window
window = tk.Tk()
window.title("Count Down")
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x_cordinate = int(screen_width - WINDOW_WIDTH)
y_cordinate = int(25)
window.geometry('{}x{}+{}+{}'.format(WINDOW_WIDTH, WINDOW_HEIGHT, x_cordinate, y_cordinate))
window.resizable(False, False)
window.minsize(WINDOW_WIDTH, WINDOW_HEIGHT)
window.attributes("-topmost", True)
window.overrideredirect(True)


class AppState:
    timer_is_running = False
    timer_thread = None
    reset_thread = None
    animation_thread = None
    speed_thread = None
    drag_start_x = None
    drag_start_y = None
    activity_done = 0 # in seconds


# functions
def create_database():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS work (
                        id INTEGER PRIMARY KEY,
                        date TEXT,
                        work_completed INTEGER
                    )''')
    conn.commit()
    conn.close()


def get_today_work():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    c.execute("SELECT work_completed FROM work WHERE date=?", (today,))
    result = c.fetchone()
    conn.close()
    if result:
        print(result[0])
        return result[0]
    else:
        return 0


def update_today_work(work_completed):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    c.execute("SELECT * FROM work WHERE date=?", (today,))
    result = c.fetchone()
    if result:
        # Update existing entry
        c.execute("UPDATE work SET work_completed=? WHERE date=?", (work_completed, today))
    else:
        # Insert new entry
        c.execute("INSERT INTO work (date, work_completed) VALUES (?, ?)", (today, work_completed))
    conn.commit()
    conn.close()


def get_mouse_pos():
    x, y = win32api.GetCursorPos()
    return x, y


def calculate_speed(last_pos, current_pos, last_time, current_time):
    distance = ((current_pos[0] - last_pos[0]) ** 2 + (current_pos[1] - last_pos[1]) ** 2) ** 0.5
    time_difference = current_time - last_time
    speed = distance / time_difference
    return speed


def normalize_speed(speed, min_speed, max_speed, min_range, max_range):
    return ((speed - min_speed) / (max_speed - min_speed)) * (max_range - min_range) + min_range


def update_timer(remaining_time):
    text_hour.delete(0, tk.END)
    text_minute.delete(0, tk.END)
    text_second.delete(0, tk.END)
    text_hour.insert(0, str(remaining_time).split(":")[0])
    text_minute.insert(0, str(remaining_time).split(":")[1])
    text_second.insert(0, str(remaining_time).split(":")[2])


def update_activity_bar():
    # update activity progressbar
    result = (AppState.activity_done / WORKING_TIME_LIMIT_IN_SECONDS) * 100
    progressbar_activity["value"] = result
    if 50 < result <= 90:
        progressbar_activity["style"] = "blue.Horizontal.TProgressbar"
    elif result > 90:
        progressbar_activity["style"] = "red.Horizontal.TProgressbar"
    else:
        progressbar_activity["style"] = "green.Horizontal.TProgressbar"
    # update percentage label
    label_percentage.configure(text=str(round(progressbar_activity["value"], 1)) + "%")


def count_down():
    try:
        h = int(text_hour.get())
        m = int(text_minute.get())
        s = int(text_second.get())
    except ValueError:
        reset_timer()
        return
    total_seconds = h * 3600 + m * 60 + s
    if total_seconds == 0:
        reset_timer()
        return
    while total_seconds > 0 and AppState.timer_is_running:
        timer = datetime.timedelta(seconds=total_seconds)
        print(timer, end="\r")
        time.sleep(1)
        # Reduces total time by one second
        total_seconds -= 1
        remaining_time = datetime.timedelta(seconds=total_seconds)
        if AppState.timer_is_running:
            update_timer(remaining_time)
            AppState.activity_done += 1
            update_activity_bar()
    reset_timer()
    update_today_work(AppState.activity_done)
    if total_seconds < 1:
        # if finished completely (without reset), show break screen
        finish_work_screen()


def finish_work_screen():
    def exit_end_screen(event):
        end_screen.destroy()

    end_screen = tk.Tk()
    end_screen.config(bg=black)
    end_screen.attributes("-fullscreen", True)
    end_screen.attributes("-topmost", True)
    main_frame = tk.Frame(end_screen, bg=black)
    main_frame.pack(pady=window.winfo_screenheight() / 4)
    label_message = tk.Label(main_frame, text="Work Completed. \n\nPress 'ESC' to continue...",
                             font=large_font, bg=black, fg=orange)
    label_message.grid(row=0, column=0)
    end_screen.bind('<Escape>', exit_end_screen)
    end_screen.mainloop()


def info_animation():
    chars = ["--", "\\", "|", "/"]
    i = 0
    while AppState.timer_is_running:
        label_info.configure(text="Working... " + chars[i])
        time.sleep(0.1)
        i += 1
        if i == 4:
            i = 0
    label_info.configure(text="Ready.")


def speed_animation():
    last_mouse_pos = get_mouse_pos()
    last_time = time.time()
    progressbar_speed.start()
    while AppState.timer_is_running:
        time.sleep(0.1)
        current_mouse_pos = get_mouse_pos()
        current_time = time.time()
        speed = calculate_speed(last_mouse_pos, current_mouse_pos, last_time, current_time)
        normalized_speed = normalize_speed(speed, 0, 8000, 0, 100)
        progressbar_speed["value"] = normalized_speed
        if 50 < normalized_speed <= 90:
            progressbar_speed["style"] = "blue.Horizontal.TProgressbar"
        elif normalized_speed > 90:
            progressbar_speed["style"] = "red.Horizontal.TProgressbar"
        else:
            progressbar_speed["style"] = "green.Horizontal.TProgressbar"
        last_mouse_pos = current_mouse_pos
        last_time = current_time
    progressbar_speed.stop()


def start_timer():
    if not AppState.timer_is_running:
        AppState.timer_is_running = True
        AppState.timer_thread = Thread(target=count_down)
        AppState.animation_thread = Thread(target=info_animation)
        AppState.speed_thread = Thread(target=speed_animation)
        AppState.timer_thread.start()
        AppState.animation_thread.start()
        AppState.speed_thread.start()


def reset_timer():
    AppState.timer_is_running = False
    if AppState.timer_thread:
        AppState.timer_thread = None
    if AppState.animation_thread:
        AppState.animation_thread = None
    text_hour.delete(0, tk.END)
    text_hour.insert(0, "0")
    text_minute.delete(0, tk.END)
    text_minute.insert(0, "0")
    text_second.delete(0, tk.END)
    text_second.insert(0, "0")
    label_info.configure(text="Ready.")


def close_app(event):
    window.destroy()


def toggle_always_on_top():
    if checkbox_ontop_value.get() == 1:
        window.attributes("-topmost", True)
    else:
        window.attributes("-topmost", False)


def start_move(event):
    AppState.drag_start_x = event.x
    AppState.drag_start_y = event.y


def stop_move(event):
    AppState.drag_start_x = None
    AppState.drag_start_y = None


def on_move(event):
    dx = event.x - AppState.drag_start_x
    dy = event.y - AppState.drag_start_y
    x = window.winfo_x() + dx
    y = window.winfo_y() + dy
    window.geometry(f"+{x}+{y}")


# fonts and colors
main_font = ('SimSun', 12)
large_font = ("Trebuchet MS", 46)
black = "#010101"
orange = "#fb7e14"
window.config(bg=black)

# styles for progressbar
style = ttk.Style()
style.theme_use("default")
style.configure("green.Horizontal.TProgressbar", foreground="green", background="green",
                thickness=PROGRESSBAR_THICKNESS)
style.configure("blue.Horizontal.TProgressbar", foreground="blue", background="blue", thickness=PROGRESSBAR_THICKNESS)
style.configure("red.Horizontal.TProgressbar", foreground="red", background="red", thickness=PROGRESSBAR_THICKNESS)

# window layout
frame_countdown = tk.Frame(window, bg=black)
frame_info = tk.Frame(window, bg=black)
frame_buttons = tk.Frame(window, bg=black)
frame_speed = tk.Frame(window, bg=black)
frame_activity = tk.Frame(window, bg=black)
frame_settings = tk.Frame(window, bg=black)
frame_countdown.grid(row=0, column=1, pady=10)
frame_info.grid(row=1, column=1)
frame_buttons.grid(row=2, column=1, pady=5)
frame_speed.grid(row=0, column=0, rowspan=3, sticky="ns", padx=4)
frame_activity.grid(row=0, column=2, rowspan=3, sticky="ns", padx=4)
frame_settings.grid(row=3, columnspan=3, sticky="ew", padx=10)

# timer boxes
text_hour = tk.Entry(frame_countdown, width=3, font=main_font, bg=black, fg=orange, justify="center")
text_minute = tk.Entry(frame_countdown, width=3, font=main_font, bg=black, fg=orange, justify="center")
text_second = tk.Entry(frame_countdown, width=3, font=main_font, bg=black, fg=orange, justify="center")
text_hour.grid(row=0, column=0, padx=5)
text_minute.grid(row=0, column=1, padx=5)
text_second.grid(row=0, column=2, padx=5)

# info label
label_info = tk.Label(frame_info, text="Ready.", bg=black, fg=orange)
label_info.grid(row=0, column=0)
label_percentage = tk.Label(frame_info, text="0.0%", bg=black, fg=orange)
label_percentage.grid(row=1, column=0)
# work and reset buttons
button_work = tk.Button(frame_buttons, text="Work", bg=orange, command=start_timer)
button_work.grid(row=0, column=0, padx=(0, 5))
button_reset = tk.Button(frame_buttons, text="Reset", bg=orange, command=reset_timer)
button_reset.grid(row=0, column=1, padx=(5, 0))

# speed progressbar
progressbar_speed = ttk.Progressbar(frame_speed, orient="vertical", mode="determinate",
                                    style="green.Horizontal.TProgressbar")
progressbar_speed.grid(row=0, column=0, rowspan=3, padx=10, pady=10)

# activity progressbar
progressbar_activity = ttk.Progressbar(frame_activity, orient="vertical", mode="determinate",
                                       style="green.Horizontal.TProgressbar")
progressbar_activity.grid(row=0, column=2, padx=10, pady=10)

# always on top checkbox
checkbox_ontop_value = tk.IntVar()
checkbox_ontop = tk.Checkbutton(frame_settings, text='On Top', variable=checkbox_ontop_value,
                                command=toggle_always_on_top, bg=black, fg=orange)
checkbox_ontop.select()
checkbox_ontop.pack(side=tk.LEFT)

# close button
label_close = tk.Label(frame_settings, text="Close", bg=black, fg=orange)
label_close.pack(side=tk.RIGHT)
label_close.bind("<Button-1>", close_app)

# run reset timer
reset_timer()

# bind drag and drop feature to the main window
window.bind("<ButtonPress-1>", start_move)
window.bind("<ButtonRelease-1>", stop_move)
window.bind("<B1-Motion>", on_move)

# create database
create_database()
# get today's work
work_completed_today = get_today_work()
AppState.activity_done = work_completed_today
# update activity progressbar
update_activity_bar()

window.mainloop()
