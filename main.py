# imports
from tkinter import *
from scripts.get_selection import *
import pyglet
import time
import os
import pyautogui
import threading
import pyperclip
import keyboard


def handle_selection(text_area):
    pyautogui.hotkey('ctrl', 'c')
    s = pyperclip.paste() # get text from clipboard
    text_area.insert(INSERT, f'\n\n{s}') # add text to textbox


# moving the window
def move_window(event):
    x, y = root.winfo_pointerxy()
    root.geometry(f"+{x-640}+{y}") # TODO solve problem with moving window


# clear box
def clear(): # Clear
    text_area.delete('1.0', END)


# check shortcut pressed TODO could add more shortcuts in future
def _check_esc_pressed(text_area):
    while True:
        if keyboard.is_pressed('esc'):
            handle_selection(text_area)
        time.sleep(0.1) # seconds    
        
        
def app_main_loop(text_area):
    # Create another thread that monitors the keyboard
    kb_input_thread = threading.Thread(target=_check_esc_pressed, args=(text_area,))
    kb_input_thread.daemon = True
    kb_input_thread.start()


# initial vars
apptext_color = "#8c8c8e"  
pyglet.font.add_file('./font/Roboto-Regular.ttf') 

if __name__ == "__main__":
    # app UI setup
    root = Tk()
    root.overrideredirect(1)
    root.eval('tk::PlaceWindow . center') # Placing the window in the center of the screen
    root.title("Note Taker")
    root.geometry('1280x720') # resolution of screen
    root.config(background='#f8f9fa')

    canvas = Canvas(root, highlightthickness=0)
    canvas.pack(fill=BOTH, expand=1)

    #creates menubar -------------------------
    menubar = Canvas(canvas, 
                    highlightthickness=0, 
                    bg="white", 
                    bd=0,
                    height=40,
                    )
    menubar.pack(fill='x')
    menubar.bind("<B1-Motion>", move_window) # window moving
    # menu buttons
    button_clean = Button(menubar, 
                        bd = 0, 
                        bg = "white",
                        fg = apptext_color,
                        highlightcolor = "#f1f3f4",
                        padx = 5,
                        pady = 5,
                        height = 2,
                        justify= CENTER,
                        text = "Clean",
                        font = ('Roboto', 12),
                        command=clear
                        )
    button_clean.pack(side=LEFT)

    # exit
    button_exit = Button(menubar, 
                        bd = 0, 
                        bg = "white",
                        fg = apptext_color,
                        highlightcolor = "#f1f3f4",
                        padx = 30,
                        pady = 5,
                        height = 2,
                        justify= CENTER,
                        text = "Exit",
                        font = ('Roboto', 12),
                        command=root.destroy,
                        )
    button_exit.pack(side=RIGHT)

    # text frame ----------------------------
    textplain = Frame(
        canvas,
        highlightthickness=0, 
        bg="white", 
        bd=0,
        width="700",
        height="600"
    )
    textplain.pack(
        pady = 10,
        fill = 'y'
        )
    textplain.pack_propagate(0)

    text_area = Text(
        textplain, 
        bg = "white", 
        fg = apptext_color, 
        bd = 0,
        font = ('Roboto', 12),
        width="700",
        height="600"
        )
    text_area.pack(
        padx = 10,
        pady = 10,
        )
    text_area.pack_propagate(0)
    
    # another thread with logics
    main_loop_thread = threading.Thread(target=app_main_loop, args=(text_area, ))
    main_loop_thread.daemon = True
    main_loop_thread.start()
    
    
    root.mainloop()
    