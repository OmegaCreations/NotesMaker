# coding: utf8

# imports
from tkinter import *
from tkinter import filedialog, messagebox, font, ttk, font
import pyglet
import time
import os
import pyautogui
import threading
import pyperclip
import keyboard
from pathlib import Path  
from PIL import Image, ImageTk
import fpdf 

# main app logic ----------------------------------------------------------------
def app_main_logic(text_area):
    # Create another thread that monitors the keyboard
    # it might be useful later to use this app_main_logic thread
    kb_input_thread = threading.Thread(target=_shortcut_used, args=(text_area,))
    kb_input_thread.daemon = True
    kb_input_thread.start()

# insert note
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
        



# main app class
class App():
    def __init__(self):
        
        self.root = Tk()
        self.attributes()
        self.generalSetup()
        self.binds()
        self.canvases()
        self.frames()
        self.widgets()
        self.textBox()
        self.buttons()
        self.set_tracing()
    
    # main variables
    def attributes(self):
        # styling
        self.apptext_color = "#8c8c8e"  
        pyglet.font.add_file('./font/Roboto-Regular.ttf') 
        
        self.font_family = StringVar()
        self.font_family.set("Arial")
        self.font_size = IntVar()
        self.font_size.set(12)
        
        # window properties
        self.isfullscreen = False
        self.map = 0

        # saves
        self.save_location = ""
        self.save_modified = False
    
    # window root setup
    def generalSetup(self):
        self.root.overrideredirect(True)
        self.root.eval('tk::PlaceWindow . center') # Placing the window in the center of the screen
        self.root.title("Note Taker")
        self.root.geometry('1280x720') # resolution of screen
        self.root.config(background='#f8f9fa')
    
    # binds 
    def binds(self):
        self.root.bind("<Map>", self.frame_mapped)
    
    # create canvases
    def canvases(self):
        self.canvas = Canvas(self.root, highlightthickness=0)
        self.canvas.pack(fill=BOTH, expand=1)

        # menu
        self.menubar = Canvas(self.canvas, 
                        highlightthickness=0,
                        bg="white",
                        bd=0,
                        height=40,
                        )
        self.menubar.pack(fill='x')
        self.menubar.bind("<B1-Motion>", self.move_window) # window moving
        
        # style menu
        self.style_menubar = Canvas(self.canvas, 
                        highlightthickness=0, 
                        bg="white",
                        bd=2,
                        height=40,
                        relief=RIDGE
                        )
        self.style_menubar.pack(fill='x')
    
    # create frames
    def frames(self):
        # text area frame
        self.textplain = Frame(
            self.canvas,
            highlightthickness=0, 
            bg="white",
            bd=0,
            width="700",
            height="600"
        )
        self.textplain.pack(
            pady = 10,
            fill = 'y'
            )
        self.textplain.pack_propagate(0)

    # main text box
    def textBox(self):
        self.text_area = Text(
            self.textplain, 
            bg = "white", 
            fg = self.apptext_color, 
            bd = 0,
            wrap="word",
            undo = True,
            autoseparators= True,
            maxundo= -1,
            font = (self.font_combo.get(), self.font_size.get()),
            width="700",
            height="600"
            )
        self.text_area.pack(
            padx = 10,
            pady = 10,
            )
        self.text_area.pack_propagate(0)
    
    # text edit widgets
    def widgets(self):
        # font box
        self.font_tuple = font.families()
        self.font_combo = ttk.Combobox(self.style_menubar, width=28, textvariable=self.font_family, state='readonly')
        self.font_combo['values'] = self.font_tuple
        self.font_combo.current(self.font_tuple.index(self.font_family.get()))
        print(self.font_combo['values'])
        self.font_combo.grid(row=0, column=0, padx=2, pady=8)
        
        self.size_tuple = tuple(range(8,80,4))
        self.size_combo = ttk.Combobox(self.style_menubar, width=20, textvariable=self.font_size, state='readonly')
        self.size_combo['values'] = self.size_tuple
        self.size_combo.current(self.size_tuple.index(self.font_size.get()))
        self.size_combo.grid(row=0, column=1, padx=5, pady=8)
    
    # buttons
    def buttons(self):
        # new text button
        button_new = Button(self.menubar, 
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
        button_open = Button(self.menubar, 
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
        button_save_as = Button(self.menubar, 
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
        button_save = Button(self.menubar, 
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
        button_pdf = Button(self.menubar, 
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
        
        # TODO take icons to other function ============================================================================= TODO
        im1 = Image.open('./img/exit.png').convert('RGBA')
        exit_img = ImageTk.PhotoImage(image = im1, master = self.canvas)
        
        im2 = Image.open('./img/fullscreen.png').convert("RGBA")
        fullscreen_img = ImageTk.PhotoImage(image = im2, master = self.canvas)
        
        im3 = Image.open('./img/minimize.png').convert("RGBA")
        minimize_img = ImageTk.PhotoImage(image = im3, master = self.canvas)

        # exit button
        button_exit = Button(self.menubar, 
                            bd = 0, 
                            bg = "white",
                            highlightcolor = "white",
                            justify= CENTER,
                            image = exit_img,
                            command=self.exit, # close window
                            )
        button_exit.pack(side=RIGHT, pady=5, padx = 15)
        button_exit.image = exit_img
        
        # fullscreen window button
        button_fullscreen = Button(self.menubar, 
                            bd = 0, 
                            bg = "white",
                            highlightcolor = "white",
                            justify= CENTER,
                            image = fullscreen_img,
                            command=self.fullscreen, # close window
                            )
        button_fullscreen.image = fullscreen_img
        button_fullscreen.pack(side=RIGHT, pady=5, padx = 15)
        
        # minimize window button
        button_minimize = Button(self.menubar, 
                            bd = 0, 
                            bg = "white",
                            highlightcolor = "white",
                            justify= CENTER,
                            image = minimize_img,
                            command=self.minimize, # close window
                            )
        button_minimize.image = minimize_img
        button_minimize.pack(side=RIGHT, pady=5, padx = 15)
        
        

    # functions -----------------------------------------------------------------------
    
    # check if size or font is going to change
    def set_tracing(self):
        self.font_family.trace_add('write', self.change_font)
        self.font_size.trace_add('write', self.change_font)
    
    # change font
    def change_font(self, var, indx, mode):
        self.text_area.configure(font=(self.font_family.get(), self.font_size.get())) # TODO dont change whole text globally!!!
    
    # change font style
    def change_font_style(self, type):
        self.text_area.configure(font=(self.font_family.get(), self.font_size.get(), type))
    
    # moving the window
    def move_window(self, event):
        x, y = self.root.winfo_pointerxy()
        self.root.geometry(f"+{x-640}+{y}") # TODO solve problem with moving window
    
    # logic for minimizing and showing window
    def frame_mapped(self, event=None):
        if self.map == 5:
            self.root.update_idletasks()
            self.root.deiconify()
            self.root.overrideredirect(True)
            self.map = 0
        else:
            self.map += 1
    
    # minimize window
    def minimize(self):
        self.map = 0
        self.root.update_idletasks()
        self.root.overrideredirect(False)
        self.root.iconify()
    
    # fullscreen
    def fullscreen(self):
        if self.isfullscreen:  
            # make the window normal
            self.root.state(newstate='normal')
            self.root.geometry('1280x720')
            self.isfullscreen = False
        else:
            # for make the window fullsreen
            self.root.state(newstate='zoomed')
            self.isfullscreen = True
             
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
                
    # open existing txt file TODO dont open other extensions
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
    
    # exit window
    def exit(self):
        if not self.save_modified:
            self.root.destroy()

        else:
            answer = messagebox.askquestion("Exit NoteMaker",
                "Do you want to save file before exit?")
     
            if answer != "yes":
                self.root.destroy()
            else:
                self.save_file()
                self.root.destroy()
        



# main loop -------------------------------------------------------------------------------
if __name__ == "__main__":
    app = App()
    
    # another thread with main logics
    main_loop_thread = threading.Thread(target=app_main_logic, args=(app.text_area, ))
    main_loop_thread.daemon = True
    main_loop_thread.start()
    
    app.root.mainloop()
    