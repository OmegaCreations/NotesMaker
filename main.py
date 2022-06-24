# coding: utf8

# imports
from tkinter import *
from tkinter import filedialog, messagebox
import pyglet
import time
import os
import pyautogui
import threading
import pyperclip
import keyboard
from pathlib import Path  
import fpdf


def handle_selection(text_area):
    pyautogui.hotkey('ctrl', 'c')
    s = pyperclip.paste() # get text from clipboard
    text_area.insert(INSERT, f'\n\n{s}') # add text to textbox

# check shortcut pressed TODO could add more shortcuts in future
def _shortcut_used(text_area):
    while True:
        if keyboard.is_pressed('ctrl+q'):
            handle_selection(text_area)
        time.sleep(0.1) # seconds    

# main app logic ----------------------------------------------------------------
def app_main_logic(text_area):
    # Create another thread that monitors the keyboard
    kb_input_thread = threading.Thread(target=_shortcut_used, args=(text_area,))
    kb_input_thread.daemon = True
    kb_input_thread.start()


class App():
    def __init__(self):
        # initial vars -----------------------------------
        # styling
        self.apptext_color = "#8c8c8e"  
        pyglet.font.add_file('./font/Roboto-Regular.ttf') 

        # saves
        self.save_location = ""
        self.save_modified = False
        
    
    # moving the window
    def move_window(self, event):
        x, y = self.root.winfo_pointerxy()
        self.root.geometry(f"+{x-640}+{y}") # TODO solve problem with moving window
             
    # new file setup
    def new_file(self):
        answer = messagebox.askquestion("Update TextBox",
                "Are you sure you want to create a new file? Any unsaved changed will be lost!")
        if answer != "yes":
            return
        
        else:  
            if not self.save_modified:
                self.save_location = ""
                
                self.text_area.delete('1.0', END)
            else:
                self.save_file()
                
        
    def open_file(self):
        if not self.save_modified:       
            try:            
                self.save_location = filedialog.askopenfile(filetypes = (("Text files", "*.txt"), ("All files", "*.*"))).name      
                
                with open(self.save_location, mode='r', encoding='utf-8') as f:             
                    content = f.read()
                    self.text_area.delete('1.0', END)
                    self.text_area.insert('1.0', content)
                    
                    self.save_modified = False                
                    
                
            except Exception as e:
                print(e)   
        
        # if text is not saved then save
        else:       
            self.save_file()              
            self.open_file()
    
    # save to existing file 
    def save_file(self):
        # check if file exists
        if self.save_location != '':
            try:
                with open(self.save_location, mode='w', encoding='utf-8') as f:
                    content = self.text_area.get('1.0', END)
                    f.write(content)
                
                self.save_modified = False
            except Exception as e:
                print(e)
                self.save_file_as()
        
        else:
            self.save_file_as()    
    
    # save file to new location
    def save_file_as(self):
        try:
            self.save_location = filedialog.asksaveasfile(filetypes = (("Text files", "*.txt"), ("All files", "*.*"))).name
            self.save_modified = False
        except Exception as e:
            print(e)
        
        with open(self.save_location, mode='w', encoding='utf-8') as f:
            f.write(self.text_area.get('1.0', END))
    
    # export file as pdf     
    def export_pdf(self):
        self.save_file()
        
        pdf = fpdf.FPDF()  
  
        # Add a page
        pdf.add_page()
        
        # set style and size of font
        pdf.add_font('Roboto', fname='./font/Roboto-Regular.ttf', uni=True)
        pdf.set_font("Roboto", size = 12)
        
        f = open(self.save_location, mode="r", encoding="utf-8")
        
        # insert the texts in pdf
        for x in f:
            pdf.cell(200, 10, txt = x, ln = 1, align = 'L')
        
        # save the pdf
        pdf.output(f"{Path(self.save_location).name}.pdf")
        Path(f"{Path(self.save_location).name}.pdf").rename(f"{self.save_location}.pdf") # move file
    
    # main UI setup
    def uiSetup(self):
        self.root = Tk()
        self.root.overrideredirect(1)
        self.root.eval('tk::PlaceWindow . center') # Placing the window in the center of the screen
        self.root.title("Note Taker")
        self.root.geometry('1280x720') # resolution of screen
        self.root.config(background='#f8f9fa')

        canvas = Canvas(self.root, highlightthickness=0)
        canvas.pack(fill=BOTH, expand=1)

        #creates menubar -------------------------
        menubar = Canvas(canvas, 
                        highlightthickness=0, 
                        bg="white", 
                        bd=0,
                        height=40,
                        )
        menubar.pack(fill='x')
        menubar.bind("<B1-Motion>", self.move_window) # window moving
        
        # menu buttons ---------------------------------
        # new text button
        button_new = Button(menubar, 
                            bd = 0, 
                            bg = "white",
                            fg = self.apptext_color,
                            highlightcolor = "#f1f3f4",
                            padx = 10,
                            pady = 5,
                            height = 2,
                            justify= CENTER,
                            text = "New",
                            font = ('Roboto', 12),
                            command=self.new_file
                            )
        button_new.pack(side=LEFT)
        
        # open file button
        button_open = Button(menubar, 
                            bd = 0, 
                            bg = "white",
                            fg = self.apptext_color,
                            highlightcolor = "#f1f3f4",
                            padx = 10,
                            pady = 5,
                            height = 2,
                            justify= CENTER,
                            text = "Open",
                            font = ('Roboto', 12),
                            command=self.open_file
                            )
        button_open.pack(side=LEFT)
        
        # save as button
        button_save_as = Button(menubar, 
                            bd = 0, 
                            bg = "white",
                            fg = self.apptext_color,
                            highlightcolor = "#f1f3f4",
                            padx = 10,
                            pady = 5,
                            height = 2,
                            justify= CENTER,
                            text = "Save as",
                            font = ('Roboto', 12),
                            command=self.save_file_as
                            )
        button_save_as.pack(side=LEFT)
        
        # save to text file button
        button_save = Button(menubar, 
                            bd = 0, 
                            bg = "white",
                            fg = self.apptext_color,
                            highlightcolor = "#f1f3f4",
                            padx = 10,
                            pady = 5,
                            height = 2,
                            justify= CENTER,
                            text = "Save",
                            font = ('Roboto', 12),
                            command=self.save_file
                            )
        button_save.pack(side=LEFT)
        
        # export to pdf button
        button_pdf = Button(menubar, 
                            bd = 0, 
                            bg = "white",
                            fg = self.apptext_color,
                            highlightcolor = "#f1f3f4",
                            padx = 10,
                            pady = 5,
                            height = 2,
                            justify= CENTER,
                            text = "Export to PDF",
                            font = ('Roboto', 12),
                            command=self.export_pdf
                            )
        button_pdf.pack(side=LEFT)

        # exit button
        button_exit = Button(menubar, 
                            bd = 0, 
                            bg = "white",
                            fg = self.apptext_color,
                            highlightcolor = "#f1f3f4",
                            padx = 30,
                            pady = 5,
                            height = 2,
                            justify= CENTER,
                            text = "Exit",
                            font = ('Roboto', 12),
                            command=self.root.destroy, # close window
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

        self.text_area = Text(
            textplain, 
            bg = "white", 
            fg = self.apptext_color, 
            bd = 0,
            font = ('Roboto', 12),
            width="700",
            height="600"
            )
        self.text_area.pack(
            padx = 10,
            pady = 10,
            )
        self.text_area.pack_propagate(0)



app = App()

# main loop -------------------------------------------------------------------------------
if __name__ == "__main__":
    # ui
    app.uiSetup()
    
    # another thread with main logics
    main_loop_thread = threading.Thread(target=app_main_logic, args=(app.text_area, ))
    main_loop_thread.daemon = True
    main_loop_thread.start()
    
    
    app.root.mainloop()
    