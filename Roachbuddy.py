import pyautogui
import random
import tkinter as tk
from tkinter import messagebox

screen_width = pyautogui.size()[0]
screen_height = pyautogui.size()[1]

x = 1400
y = 1050
cycle = 0
check = 1
speed = 3
idle_num = [1, 2, 3, 4]
sleep_num = [10, 11, 12, 13, 15]
walk_left = [6, 7]
walk_right = [8, 9]

impath = 'RoachMove/'

phrases = [
    "Hello there!",
    "I'm your roach buddy!",
    "Having a good day?",
    "Need any help?",
    "Click me again!"
]

def get_random_event():
    """Simple random event selection - favors walking"""
    
    events = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 6, 7, 8, 9, 6, 7, 8, 9]
    return random.choice(events)

def check_boundaries():
    """Keep pet on screen"""
    global x, y
    if x < 0:
        x = 0
    elif x > screen_width - 100:  # 100 is pet width
        x = screen_width - 100
    
    if y < 0:
        y = 0
    elif y > screen_height - 100:  # 100 is pet height
        y = screen_height - 100

def event(cycle, check, event_number, x):
    global speed
    
    if event_number in idle_num:
        check = 0
        delay = 400
        print('idle')
    elif event_number == 5:
        check = 1
        delay = 100
        print('from idle to sleep')
    elif event_number in walk_left:
        check = 4
        delay = 80 
        print('walking towards left')
    elif event_number in walk_right:
        check = 5
        delay = 80
        print('walking towards right')
    elif event_number in sleep_num:
        check = 2
        delay = 1000
        print('sleep')
    elif event_number == 14:
        check = 3
        delay = 100
        print('from sleep to idle')
    else:
        check = 0
        delay = 400
    
    window.after(delay, update, cycle, check, event_number, x)

def gif_work(cycle, frames, event_number, first_num, last_num):
    if cycle < len(frames) - 1:
        cycle += 1
    else:
        cycle = 0
        event_number = random.randrange(first_num, last_num + 1, 1)
    return cycle, event_number

def update(cycle, check, event_number, x):
    global speed
    
    if check == 0:
        frame = idle[cycle]
        cycle, event_number = gif_work(cycle, idle, event_number, 1, 9)
    elif check == 1:
        frame = idle_to_sleep[cycle]
        cycle, event_number = gif_work(cycle, idle_to_sleep, event_number, 10, 10)
    elif check == 2:
        frame = sleep[cycle]
        cycle, event_number = gif_work(cycle, sleep, event_number, 10, 15)
    elif check == 3:
        frame = sleep_to_idle[cycle]
        cycle, event_number = gif_work(cycle, sleep_to_idle, event_number, 1, 1)
    elif check == 4: 
        frame = walk_positive[cycle]
        cycle, event_number = gif_work(cycle, walk_positive, event_number, 6, 9)
        x -= speed
  
        if x <= 0:
            event_number = random.choice(walk_right)  
    elif check == 5:  
        frame = walk_negative[cycle]
        cycle, event_number = gif_work(cycle, walk_negative, event_number, 6, 9)  
        x += speed
        
        if x >= screen_width - 100:
            event_number = random.choice(walk_left)  
    
    check_boundaries()
    
    window.geometry('100x100+' + str(x) + '+' + str(y))
    label.configure(image=frame)
    window.after(1, event, cycle, check, event_number, x)

def on_pet_click(event):
    """Handle clicking on the pet"""
    action = random.randrange(1, 3)
    
    if action == 1:
        show_speech_bubble()



def show_speech_bubble():
    """Show speech bubble above pet"""
    phrase = random.choice(phrases)
    
    bubble = tk.Toplevel(window)
    bubble.overrideredirect(True)
    bubble.wm_attributes('-topmost', True)
    
    bubble_label = tk.Label(bubble, text=phrase, bg='yellow', fg='black', 
                           font=('Arial', 9), padx=8, pady=4, 
                           relief='solid', borderwidth=1)
    bubble_label.pack()
    
    bubble_x = x
    bubble_y = y - 40
    bubble.geometry(f"+{bubble_x}+{bubble_y}")
    
    bubble.after(2000, bubble.destroy)

def on_right_click(event):
    """Simple right-click menu"""
    menu = tk.Menu(window, tearoff=0)
    menu.add_command(label="Speed Up", command=speed_up)
    menu.add_command(label="Slow Down", command=slow_down)
    menu.add_command(label="Feed Roach", command=feed_roach)
    menu.add_separator()
    menu.add_command(label="Exit", command=window.quit)
    
    try:
        menu.tk_popup(event.x_root, event.y_root)
    finally:
        menu.grab_release()

def speed_up():
    global speed
    if speed < 8:
        speed += 1
    show_speech_bubble_text(f"Speed: {speed}")

def slow_down():
    global speed
    if speed > 1:
        speed -= 1
    show_speech_bubble_text(f"Speed: {speed}")

def feed_roach():
    show_speech_bubble_text("Yummy! Thanks!")

def show_speech_bubble_text(text):
    """Show custom text in speech bubble"""
    bubble = tk.Toplevel(window)
    bubble.overrideredirect(True)
    bubble.wm_attributes('-topmost', True)
    
    bubble_label = tk.Label(bubble, text=text, bg='lightgreen', fg='black', 
                           font=('Arial', 9), padx=8, pady=4, 
                           relief='solid', borderwidth=1)
    bubble_label.pack()
    
    bubble_x = x
    bubble_y = y - 40
    bubble.geometry(f"+{bubble_x}+{bubble_y}")
    bubble.after(1500, bubble.destroy)

window = tk.Tk()

idle = [tk.PhotoImage(file=impath+'roachidle.gif', format='gif -index %i' % (i)) for i in range(6)]
idle_to_sleep = [tk.PhotoImage(file=impath+'roachidle.gif', format='gif -index %i' % (i)) for i in range(6)]
sleep = [tk.PhotoImage(file=impath+'roachidle.gif', format='gif -index %i' % (i)) for i in range(6)]
sleep_to_idle = [tk.PhotoImage(file=impath+'roachidle.gif', format='gif -index %i' % (i)) for i in range(6)]
walk_positive = [tk.PhotoImage(file=impath+'roachwalk.gif', format='gif -index %i' % (i)) for i in range(3)]
walk_negative = [tk.PhotoImage(file=impath+'roachwalk.gif', format='gif -index %i' % (i)) for i in range(3)]

window.config(highlightbackground='black')
label = tk.Label(window, bd=0, bg='black', cursor='hand2') 
window.overrideredirect(True)
window.wm_attributes('-transparentcolor', 'black')
window.wm_attributes('-topmost', True)  
label.pack()

label.bind('<Button-1>', on_pet_click)
label.bind('<Button-3>', on_right_click)  

event_number = get_random_event()
window.after(1, update, cycle, check, event_number, x)
window.mainloop()