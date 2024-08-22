import tkinter as tk
import time
import random

import threading 


class TypeSpeedGUI:

    def __init__(self):

# GUI inits
        self.root = tk.Tk()
        self.root.title("Typing Speed Test")
        self.root.geometry("1000x600")

# Get Text from txt file
        self.texts = open("texts.txt", "r").read().split("\n")

# Make a Frame
        self.frame = tk.Frame(self.root)

# GUI Items
# Sentence to be typed by user
        self.text_label = tk.Label(self.frame, 
                                   text=random.choice(self.texts), 
                                   font=("Helvetica", 18))
        self.text_label.grid(row=0, 
                             column=0, 
                             columnspan=2, 
                             padx=5, 
                             pady=10)
        
# Sentence typed by user
        self.user_input = tk.Entry(self.frame, 
                                   width=50, 
                                   font=("Helvetica", 24))
        self.user_input.grid(row=1, 
                             column=0, 
                             columnspan=2, 
                             padx=5, 
                             pady=10)
        self.user_input.bind("<KeyRelease>", 
                             self.start)

# User speed label        
        self.speed_label = tk.Label(self.frame, 
                                   text="Speed: \n0.00 CPS \n0.00 CPM\n0.00 WPS \n0.00 WPM", 
                                   font=("Helvetica", 18))
        self.speed_label.grid(row=2, 
                             column=0, 
                             padx=5, 
                             pady=10)

# User mistake label        
        self.mistake_label = tk.Label(self.frame, 
                                   text="Mistakes: 0", 
                                   font=("Helvetica", 18))
        self.mistake_label.grid(row=2, 
                             column=1, 
                             padx=5, 
                             pady=10)
        
# Reset Button
        self.reset_button = tk.Button(self.frame, text="RESET", 
                                      command=self.reset, 
                                      font=("Helvetica", 14))
        self.reset_button.grid(row=3, 
                             column=0, 
                             columnspan=2, 
                             padx=5, 
                             pady=10)

# Pack Items in Frame        
        self.frame.pack(expand=True)

# Init Game
        self.counter = 0
        self.mistake_count = 0
        self.game_on = False

# Init Mainloop
        self.root.mainloop()

# Start Function
    def start(self, event):
        if not self.game_on: # check to see if game is already running
            if not event.keycode in [16, 17, 18]:
                self.game_on = True
                t = threading.Thread(target=self.time_thread)
                t.start()
# check to see if user got a letter wrong and add to the mistake count
        if not self.text_label.cget('text').startswith(self.user_input.get()):
            self.user_input.config(fg = "red")
            self.mistake_count += 1
            self.mistake_label.config(text=f"Mistakes: {self.mistake_count}")
        else:
            self.user_input.config(fg = "black")

# check to see if user got the text correct        
        if self.user_input.get() == self.text_label.cget('text'): 
            self.game_on = False  
            self.user_input.config(fg="green")
            self.reset_button.focus_set()
            


# Init Threading
    def time_thread(self):
        while self.game_on:
            time.sleep(0.1)
            self.counter += 0.1

            cps = len(self.user_input.get()) / self.counter
            cpm = cps * 60

            wps = len(self.user_input.get().split(" ")) / self.counter
            wpm = wps * 60

            self.speed_label.config(text=f"Speed:\n{cps:.2f} CPS\n{cpm:.2f} CPM\n{wps:.2f} WPS\n{wpm:.2f} WPM")

# Reset Function
    def reset(self):
        self.game_on = False

        self.counter = 0
        self.mistake_count = 0

        self.speed_label.config(text="Speed: \n0.00 WPS \n0.00WPM")
        self.text_label.config(text=random.choice(self.texts))

        self.user_input.delete(0, tk.END)

        self.mistake_label.config(text="Mistakes: 0")

TypeSpeedGUI()
