# importing all recuared libraries
import src.Globals as Globals
import random
import threading
import time
import tkinter as tk
from tkinter import filedialog as fd


globals = Globals.Globals()
class TypeTrainingGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Typing speed tester")
        # creating a full-screen window
        self.root.geometry(
            str(self.root.winfo_screenwidth())
            + "x"
            + str(self.root.winfo_screenheight())
        )

        self.text = open("text.txt", "r").read().split("\n")
        self.counter = 1
        self.characters_counter = 0
        self.words_counter = 0
        self.wrong_types_counter = 0
        with open("save.txt", "r") as f:
            s = f.read()
            lines = s.split("\n")
            self.characters_counter = int(lines[0])
            self.words_counter = int(lines[1])
            self.counter = float(lines[2])
            self.wrong_types_counter = int(lines[3])
        # adding the boolean to know that the app is started or not
        self.running = False
        self.start()
        self.root.mainloop()

    def start(self):
        # creating a main frame
        self.frame = tk.Frame(self.root)

        # creating a lable
        self.line = random.choice(self.text)
        self.sample_label = tk.Label(
            self.frame, text=self.line, font=("Helventica", 18)
        )
        self.sample_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        # creating a text box
        self.check = (self.root.register(self.is_valid), "%P")
        self.input_entry = tk.Entry(
            self.frame,
            width=40,
            font=("Helventica", 24),
            validate="key",
            validatecommand=self.check,
        )
        self.input_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=10)

        # creating a label for the timer
        self.speed_label = tk.Label(
            self.frame,
            text=f"Speed: \n{(self.characters_counter)* globals.seconds_in_minute / self.counter:.2f} Charecters per minute\n{(self.words_counter)* globals.seconds_in_minute / self.counter:.2f} Words per minute\n{self.wrong_types_counter} MISTAKES",
            font=("Helventica", 18),
        )
        self.speed_label.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

        # creating a reset button
        self.reset_button = tk.Button(
            self.frame, text="Reset", command=self.reset, font=("Helventica", 24)
        )
        self.reset_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

        # creating a exit button
        self.exit_button = tk.Button(
            self.frame,
            text="EXIT",
            command=self.exit,
            font=("Helventica", 24),
            bg="Red",
        )
        self.exit_button.grid(row=5, column=0, columnspan=2, padx=5, pady=10)
        # creating a reset button
        self.chosee_button = tk.Button(
            self.frame,
            command=self.choose_file,
            text="Choose source file",
            font=("Helventica", 24),
        )
        self.chosee_button.grid(row=4, columnspan=2, padx=5, pady=10)

        self.frame.pack(expand=True)
        self.input_entry.focus()

    # function that checks typed text every time button pressed
    def is_valid(self, newval):
        # starting timer when first button pressed
        if not self.running:
            self.running = True
            self.char_number = 0
            self.t = threading.Thread(target=self.time_thread)
            self.t.start()
        n = len(newval)

        # calculation of cmp and wpm based on time left and characters and words counters
        result = self.line.startswith(newval)
        if not result:
            self.wrong_types_counter += 1
        if newval == self.line:
            self.save()
            self.reset()
        return result

    # creating destroing fuction
    def destroy(self):
        self.input_entry.destroy()
        self.speed_label.destroy()
        self.reset_button.destroy()
        self.exit_button.destroy()
        self.sample_label.destroy()
        self.chosee_button.destroy()
        self.frame.destroy()

    # timer and words and characters counter
    def time_thread(self):
        while self.running:
            time.sleep(0.1)
            self.counter += 0.1
            # symbols per minute
            cpm = (
                (self.characters_counter + len(self.input_entry.get()))
                * globals.seconds_in_minute
                / self.counter
            )
            # words per minute
            wpm = (
                (self.words_counter + len(self.input_entry.get().split(" ")))
                * globals.seconds_in_minute
                / self.counter
            )
            self.speed_label.config(
                text=f"Speed: \n{cpm:.2f} Charecters per minute\n{wpm:.2f} Words per minute\n{self.wrong_types_counter} MISTAKES"
            )

    #  reset function that
    def reset(self):
        self.running = False
        self.characters_counter += len(self.input_entry.get())
        self.words_counter += (
            len(self.input_entry.get().split(" "))
            if self.input_entry.get().split(" ")[0] != ""
            else 0
        )
        self.destroy()
        self.start()

    # exit function saves words and charecters counters and stops the program
    def exit(self):
        self.save()
        raise SystemExit

    # just save functionn that saves time, mistakes, words and characters counters to txt file named save.txt
    def save(self):
        with open("save.txt", "w") as f:
            f.write(
                f"{self.characters_counter}\n{self.words_counter}\n{self.counter}\n{self.wrong_types_counter}"
            )

    # function of choosing sourse file for input text
    def choose_file(self):
        self.file_selection = fd.askopenfilename()
        self.text = open(self.file_selection, "r").read().split("\n")


# starting the main loop
TypeTrainingGUI()
