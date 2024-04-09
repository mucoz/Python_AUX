import tkinter as tk
import time
import datetime
from threading import Thread

WINDOW_WIDTH = 200
WINDOW_HEIGHT = 150

# window
window = tk. Tk()
window.title("Count Down")
window.iconbitmap("xpsp2res.dll_14_6105_1025.ico")
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x_cordinate = int(screen_width - WINDOW_WIDTH)
y_cordinate = int(25)
window.geometry('{}x{}+{}+{}'.format(WINDOW_WIDTH, WINDOW_HEIGHT, x_cordinate, y_cordinate))
window.resizable(False, False)
window.minsize(WINDOW_WIDTH, WINDOW_HEIGHT)
window.attributes("-topmost", True)


class AppState:
    timer_is_running = False
    timer_thread = None
    reset_thread = None
    animation_thread = None


# functions
def countdown():
    h = int(text_hour.get())
    m = int(text_minute.get())
    s = int(text_second.get())
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
        text_hour.delete(0, tk. END)
        text_minute.delete(0, tk.END)
        text_second.delete(0, tk.END)
        remaining_time = datetime.timedelta(seconds=total_seconds)
        text_hour.insert(0, str(remaining_time).split(":")[0])
        text_minute.insert(0, str(remaining_time).split(":")[1])
        text_second.insert(0, str(remaining_time).split(":")[2])

    reset_timer()
    if total_seconds < 1:
        finish_work_screen()


def finish_work_screen():

    def exit_end_screen(e):
        end_screen.destroy()

    end_screen = tk.Tk()
    end_screen.config(bg=black)
    end_screen.attributes("-fullscreen", True)
    end_screen.attributes("-topmost", True)
    main_frame = tk.Frame(end_screen, bg=black)
    main_frame.pack(pady=window.winfo_screenheight() / 4)
    label_close = tk.Label(main_frame, text="Work Completed. \n\nPress 'ESC' to continue...",
                           font=large_font, bg=black, fg=orange)
    label_close.grid(row=0, column=0)
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


def start_timer():
    if not AppState.timer_is_running:
        AppState.timer_is_running = True
        AppState.timer_thread = Thread(target=countdown)
        AppState.animation_thread = Thread(target=info_animation)
        AppState.timer_thread.start()
        AppState.animation_thread.start()


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


def toggle_always_on_top():
    if checkbox_ontop_value.get() == 1:
        window.attributes("-topmost", True)
    else:
        window.attributes("-topmost", False)


# fonts and colors
main_font = ('SimSun', 12)
large_font = ("Trebuchet MS", 46)
black = "#010101"
orange = "#fb7e14"
window.config(bg=black)

# window layout
frame_text = tk.Frame(window, bg=black)
frame_info = tk.Frame(window, bg=black)
frame_buttons = tk.Frame(window, bg=black)
frame_settings = tk.Frame(window, bg=black)
frame_text.pack()
frame_info.pack()
frame_buttons.pack()
frame_settings.pack()

# timer boxes
text_hour = tk.Entry(frame_text, width=3, font=main_font, bg=black, fg=orange)
text_minute = tk.Entry(frame_text, width=3, font=main_font, bg=black, fg=orange)
text_second = tk.Entry(frame_text, width=3, font=main_font, bg=black, fg=orange)
text_hour.grid(row=0, column=0, padx=5, pady=15)
text_minute.grid(row=0, column=1, padx=5, pady=15)
text_second.grid(row=0, column=2, padx=5, pady=15)

# info label
label_info = tk.Label(frame_info, text="Ready.", bg=black, fg=orange)
label_info.grid(row=0, column=0)

# work and reset buttons
button_work = tk.Button(frame_buttons, text="Work", bg=orange, command=start_timer)
button_work.grid(row=0, column=0, padx=5, pady=10)
button_reset = tk.Button(frame_buttons, text="Reset", bg=orange, command=reset_timer)
button_reset.grid(row=0, column=1, padx=5, pady=10)

# always on top checkbox
checkbox_ontop_value = tk.IntVar()
checkbox_ontop = tk.Checkbutton(frame_settings, text='Always On Top', variable=checkbox_ontop_value,
                                command=toggle_always_on_top, bg=black, fg=orange)
checkbox_ontop.select()
checkbox_ontop.grid(row=0, column=0)

# run reset timer
reset_timer()
window.mainloop()
