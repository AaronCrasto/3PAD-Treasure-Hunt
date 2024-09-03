import tkinter as tk
from tkinter import messagebox
import random
import json
import os
import re

class TimeTracker:
    def __init__(self, root, label):
        self.root = root
        self.label = label
        self.time_elapsed = 0
        self.timer_running = False

    def start(self):
        self.timer_running = True
        self.update_timer()

    def stop(self):
        self.timer_running = False

    def reset(self):
        self.time_elapsed = 0
        self.update_label()

    def update_timer(self):
        if self.timer_running:
            self.time_elapsed += 1
            self.update_label()
            self.root.after(1000, self.update_timer)

    def update_label(self):
        self.label.config(text=f"Time: {self.time_elapsed}s")

    def get_time(self):
        return self.time_elapsed

class MathGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Treasure")
        self.root.protocol("WM_DELETE_WINDOW", self.confirm_close)
        self.window_width = 1920
        self.window_height = 1080
        self.root.geometry(f"{self.window_width}x{self.window_height}")

        self.difficulty = "Easy"
        self.mode = None

        self.CELL_SIZE = 60
        self.ROWS = 16
        self.COLS = 30

        self.wall_image = tk.PhotoImage(file="wall.png").subsample(1)
        self.player_image = self.resize_image(tk.PhotoImage(file="wizard.png"), self.CELL_SIZE, self.CELL_SIZE)
        self.red_box_image = self.resize_image(tk.PhotoImage(file="goblin1.png"), self.CELL_SIZE, self.CELL_SIZE)
        self.green_box_image = self.resize_image(tk.PhotoImage(file="dirt .png"), self.CELL_SIZE, self.CELL_SIZE)
        self.empty_space_image = self.resize_image(tk.PhotoImage(file="dirt .png"), self.CELL_SIZE, self.CELL_SIZE)
        self.exit_image = self.resize_image(tk.PhotoImage(file="treasure.png"), self.CELL_SIZE, self.CELL_SIZE)
        self.addition_image = tk.PhotoImage(file="Addition 1.png")
        self.subtraction_image = tk.PhotoImage(file="Subtraction .png")
        self.multiplication_image = tk.PhotoImage(file="Multiplication .png")
        self.division_image = tk.PhotoImage(file="Division .png")

        self.maze = []
        self.player_pos = [1, 1]
        self.math_question_active = False
        self.red_boxes = set()
        self.solved_boxes = set()

        self.time_elapsed = 0
        self.timer_label = tk.Label(self.root, text="Time: 0s", font=("Times New Roman", 24))
        self.timer_running = False

        self.feedback_label = tk.Label(self.root, text="", font=("Times New Roman", 18))

        self.user_data_file = "user_data.json"
        self.load_user_data()

        self.correct_answers = 0
        self.incorrect_answers = 0

        self.show_login_window()

    def confirm_close(self):
        if messagebox.askokcancel("Quit", "Do you really want to quit?"):
            self.root.destroy()

    def on_enter(self, event):
        event.widget.config(relief=tk.RAISED)

    def on_leave(self, event):
        event.widget.config(relief=tk.FLAT)

    def load_user_data(self):
        if os.path.exists(self.user_data_file):
            with open(self.user_data_file, 'r') as file:
                self.user_data = json.load(file)
        else:
            self.user_data = {}

    def save_user_data(self):
        with open(self.user_data_file, 'w') as file:
            json.dump(self.user_data, file, indent=4)

    def show_login_window(self):
        self.login_canvas = tk.Canvas(self.root, width=self.window_width, height=self.window_height)
        self.login_canvas.pack(fill="both", expand=True)

        self.additional_image = tk.PhotoImage(file="Treasure Hunt.png")
        self.login_canvas.create_image(self.window_width // 2, self.window_height * 0.15, image=self.additional_image, anchor=tk.N)

        username_label = tk.Label(self.login_canvas, text="Username", font=("Times New Roman", 18), bg="#1D0200", fg="white")
        self.login_canvas.create_window(self.window_width // 2, self.window_height * 0.4, window=username_label)

        self.username_entry = tk.Entry(self.login_canvas, font=("Times New Roman", 18))
        self.login_canvas.create_window(self.window_width // 2, self.window_height * 0.45, window=self.username_entry)

        password_label = tk.Label(self.login_canvas, text="Password", font=("Times New Roman", 18), bg="#1D0200", fg="white")
        self.login_canvas.create_window(self.window_width // 2, self.window_height * 0.5, window=password_label)

        self.password_entry = tk.Entry(self.login_canvas, show="*", font=("Times New Roman", 18))
        self.login_canvas.create_window(self.window_width // 2, self.window_height * 0.55, window=self.password_entry)

        login_button = tk.Button(self.login_canvas, text="Login", height=1, width=20, font=("Times New Roman", 18), bg="#BB9351", command=self.check_login)
        self.login_canvas.create_window(self.window_width // 2, self.window_height * 0.65, window=login_button)

        leaderboard_button = tk.Button(self.login_canvas, text="Leaderboard",height=1, width=20, font=("Times New Roman", 18), bg="#BB9351", command=self.show_leaderboard)
        self.login_canvas.create_window(self.window_width // 2, self.window_height * 0.75, window=leaderboard_button)

        create_account_button = tk.Button(self.login_canvas, text="Create Account",height=1, width=20, font=("Times New Roman", 18), bg="#BB9351", command=self.show_create_account_window)
        self.login_canvas.create_window(self.window_width // 2, self.window_height * 0.85, window=create_account_button)

        how_to_play_button = tk.Button(self.login_canvas, text="How to Play ?", height=1, width=20, font=("Times New Roman", 18), bg="#BB9351", command=self.show_how_to_play)
        self.login_canvas.create_window(self.window_width // 2, self.window_height * 0.95, window=how_to_play_button)

    def show_how_to_play(self):
        how_to_play_window = tk.Toplevel(self.root)
        how_to_play_window.title("How to Play")
        how_to_play_window.geometry("900x700")
        how_to_play_window.configure(bg="#1D0200")

        tk.Label(how_to_play_window, text="How to Play", font=("Times New Roman", 24), bg="#1D0200", fg="white").pack(pady=10)

        instructions = (
            "Welcome to the Treasure Hunt !\n\n"
            "1. Login into an existing account or create a new one using the Create Account Button\n" 
            "    - Make sure to remember your details\n\n"
            "2. Once you have sucessfully logged in choose the maths operation you'd like to improve your skills in\n\n"
            "3. When you have chosen your game mode you'll enter the maze\n\n "
            "4. **Controls**:\n"
            "    - Use the arrow keys to move the wizard around the maze.\n\n"
            "5. **Math Questions**:\n"
            "   - When you encounter a goblin, a math question will appear.\n"
            "   - You can either use the number '1,2,3 and 4' or use your mouse to answer the question\n"
            "   - Solve the question and select the correct answer from the options.\n\n"
            "6. **Winning**:\n"
            "   - Once all the goblins have been defeated, you can access the treasure .\n\n"
            "7. **Leaderboard**:\n"
            "   - Check the leaderboard to see how you rank against other players in terms of time.\n\n"
            "                                       GOOD LUCK AND HAVE FUN!"
    )

        tk.Label(how_to_play_window, text=instructions, font=("Times New Roman", 16), bg="#1D0200", fg="white", justify=tk.LEFT).pack(pady=20, padx=20)

    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not self.validate_username(username):
            messagebox.showerror("Error", "Invalid username. Must be 1-15 characters long and contain only letters, numbers, or underscores.")
            return

        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password.")
        else:
            self.username = username
            if self.username not in self.user_data:
                messagebox.showerror("Error", "Username not found. Please create an account.")
                return
            elif self.user_data[self.username]["password"] != password:
                messagebox.showerror("Error", "Incorrect password.")
                return

            self.save_user_data()

            self.login_canvas.destroy()
            self.show_setup_controls()

    def show_create_account_window(self):
        self.create_account_window = tk.Toplevel(self.root)
        self.create_account_window.title("Create Account")
        self.create_account_window.geometry("400x300")
        self.create_account_window.configure(bg="#1D0200")

        tk.Label(self.create_account_window, text="Create a New Account", font=("Times New Roman", 18), bg="#1D0200", fg="white").pack(pady=10)

        tk.Label(self.create_account_window, text="Username", font=("Times New Roman", 14), bg="#1D0200", fg="white").pack()
        self.new_username_entry = tk.Entry(self.create_account_window, font=("Times New Roman", 14))
        self.new_username_entry.pack(pady=5)

        tk.Label(self.create_account_window, text="Password", font=("Times New Roman", 14), bg="#1D0200", fg="white").pack()
        self.new_password_entry = tk.Entry(self.create_account_window, show="*", font=("Times New Roman", 14))
        self.new_password_entry.pack(pady=5)

        tk.Button(self.create_account_window, text="Create Account", font=("Times New Roman", 14), command=self.create_account, bg="#BB9351").pack(pady=20)

    def create_account(self):
        new_username = self.new_username_entry.get()
        new_password = self.new_password_entry.get()

        if not self.validate_username(new_username):
            messagebox.showerror("Error", "Invalid username. Must be 1-15 characters long and contain only letters, numbers, or underscores.")
            return

        if not new_username or not new_password:
            messagebox.showerror("Error", "Please fill in both fields.")
            return

        if new_username in self.user_data:
            messagebox.showerror("Error", "Username already exists. Please choose a different one.")
            return


        self.user_data[new_username] = {"password": new_password, "times": {}}
        self.save_user_data()
        messagebox.showinfo("Success", "Account created successfully!")
        self.create_account_window.destroy()

    def validate_username(self, username):
        return re.match(r'^[A-Za-z0-9_]{1,15}$', username) is not None

    def show_setup_controls(self):
        self.canvas = tk.Canvas(self.root, width=self.root.winfo_width(), height=self.root.winfo_height())
        self.canvas.pack(fill="both", expand=True)

        button_width = 800
        button_height = 400

        self.addition_button = tk.Button(self.root, image=self.addition_image, width=button_width, height=button_height,
                                         command=lambda: self.start_game("Addition"))
        self.addition_button_window = self.canvas.create_window(100, 100, window=self.addition_button, anchor="nw")
        self.addition_button.bind("<Enter>", self.on_enter)
        self.addition_button.bind("<Leave>", self.on_leave)

        self.subtraction_button = tk.Button(self.root, image=self.subtraction_image, width=button_width, height=button_height,
                                            command=lambda: self.start_game("Subtraction"))
        self.subtraction_button_window = self.canvas.create_window(1000, 100, window=self.subtraction_button, anchor="nw")
        self.subtraction_button.bind("<Enter>", self.on_enter)
        self.subtraction_button.bind("<Leave>", self.on_leave)

        self.multiplication_button = tk.Button(self.root, image=self.multiplication_image, width=button_width, height=button_height,
                                               command=lambda: self.start_game("Multiplication"))
        self.multiplication_button_window = self.canvas.create_window(100, 550, window=self.multiplication_button, anchor="nw")
        self.multiplication_button.bind("<Enter>", self.on_enter)
        self.multiplication_button.bind("<Leave>", self.on_leave)

        self.division_button = tk.Button(self.root, image=self.division_image, width=button_width, height=button_height,
                                         command=lambda: self.start_game("Division"))
        self.division_button_window = self.canvas.create_window(1000, 550, window=self.division_button, anchor="nw")
        self.division_button.bind("<Enter>", self.on_enter)
        self.division_button.bind("<Leave>", self.on_leave)

    def start_game(self, mode):
        self.mode = mode

        for widget in self.root.winfo_children():
            widget.pack_forget()

        self.initialize_maze()

        self.player_pos = [1, 1]

        self.canvas = tk.Canvas(self.root, width=self.COLS * self.CELL_SIZE, height=self.ROWS * self.CELL_SIZE, bg='white')
        self.canvas.pack(pady=20)

        self.timer_label.place(x=1600, y=1000)

        self.feedback_label.pack(pady=10)

        self.draw_maze()
        self.draw_player()

        self.timer_running = True
        self.time_elapsed = 0
        self.correct_answers = 0
        self.incorrect_answers = 0
        self.update_timer()

        self.bind_keys()

    def bind_keys(self):
        self.root.bind("<Left>", lambda event: self.move_player(-1, 0))
        self.root.bind("<Right>", lambda event: self.move_player(1, 0))
        self.root.bind("<Up>", lambda event: self.move_player(0, -1))
        self.root.bind("<Down>", lambda event: self.move_player(0, 1))

    def unbind_keys(self):
        self.root.unbind("<Left>")
        self.root.unbind("<Right>")
        self.root.unbind("<Up>")
        self.root.unbind("<Down>")

    def initialize_maze(self):
        mazes = {            "Addition": [ # The rows of numbers below this are the preset maze for the Addition game mode
                    # 1 = wall
                    # 2 = goblin
                    # 3 = the cell of the goblin after dissappearance
                    # 4 = the treasure chest 
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  
                [1, 0, 0, 0, 1, 2, 1, 2, 0, 0, 1, 1, 1, 1, 1, 0, 0, 2, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 4, 1],
                [1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 2, 0, 1, 0, 1],
                [1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 2, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1],
                [1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1], 
                [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1], 
                [1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 2, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 2, 0, 1, 1, 0, 1, 0, 1],
                [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1],
                [1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1],
                [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
                [1, 2, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            ],

            "Subtraction": [ # The rows of numbers below this are the preset maze for the Subtraction game mode
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 2, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1],
                [1, 1, 0, 0, 1, 0, 1, 0, 0, 2, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 2, 0, 0, 0, 1],
                [1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
                [1, 0, 1, 0, 1, 0, 0, 2, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1], 
                [1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 2, 0, 0, 0, 0, 1], 
                [1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1],
                [1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1],
                [1, 2, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1],
                [1, 2, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 2, 1],
                [1, 4, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 2, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            ],

            
            "Multiplication": [ # The rows of numbers below this are the preset maze for the Multiplication game mode
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 2, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1],
                [1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 2, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 2, 1, 0, 0, 1],
                [1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                [1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1],
                [1, 0, 1, 0, 0, 0, 1, 2, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 2, 1, 0, 0, 1, 1, 0, 1, 1],
                [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 4, 1],
                [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 2, 1],
                [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 2, 0, 1, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 2, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
                [1, 2, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            ],


            
            "Division": [# The rows of numbers below this are the preset maze for the Division game mode
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 2, 1, 2, 0, 0, 1, 1, 1, 1, 1, 1],
                [1, 0, 1, 0, 1, 0, 0, 2, 1, 2, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1],
                [1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1],
                [1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1],
                [1, 2, 1, 0, 1, 1, 1, 1, 1, 0, 1, 2, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 2, 0, 0, 1, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1],
                [1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1],
                [1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 2, 0, 0, 0, 1, 1, 0, 0, 1],
                [1, 1, 1, 1, 0, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1],
                [1, 2, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 4, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            ]}
        self.maze = mazes[self.mode]

    def update_timer(self):
        if self.timer_running:
            self.time_elapsed += 1
            self.timer_label.config(text=f"Time: {self.time_elapsed}s")
            self.root.after(1000, self.update_timer)

    def resize_image(self, image, width, height):
        return image.subsample(int(image.width() // width), int(image.height() // height))

    def draw_maze(self):
        self.canvas.delete("all")
        for row in range(self.ROWS):
            for col in range(self.COLS):
                cell_value = self.maze[row][col]
                x = col * self.CELL_SIZE
                y = row * self.CELL_SIZE

                self.canvas.create_image(x, y, anchor=tk.NW, image=self.empty_space_image)

                if cell_value == 1:
                    self.canvas.create_image(x, y, anchor=tk.NW, image=self.wall_image)
                elif cell_value == 3:
                    self.canvas.create_image(x, y, anchor=tk.NW, image=self.green_box_image)
                elif cell_value == 4:
                    self.canvas.create_image(x, y, anchor=tk.NW, image=self.exit_image)

                if cell_value == 2:
                    self.canvas.create_image(x, y, anchor=tk.NW, image=self.red_box_image)
                    self.red_boxes.add((row, col))

    def draw_player(self):
        x = self.player_pos[1] * self.CELL_SIZE
        y = self.player_pos[0] * self.CELL_SIZE
        self.canvas.create_image(x, y, anchor=tk.NW, image=self.player_image)

    def move_player(self, dx, dy):
        new_row = self.player_pos[0] + dy
        new_col = self.player_pos[1] + dx

        if 0 <= new_row < self.ROWS and 0 <= new_col < self.COLS:
            cell_value = self.maze[new_row][new_col]

            if cell_value == 1:
                return
            elif cell_value == 4:
                if len(self.red_boxes) > 0:
                    self.feedback_label.config(text="Not all goblins have been defeated yet.")
                    return

            self.player_pos = [new_row, new_col]
            self.draw_maze()
            self.draw_player()
            self.check_for_events()

    def check_for_events(self):
        current_pos = tuple(self.player_pos)
        if current_pos in self.red_boxes:
            self.display_math_question()
        elif self.maze[self.player_pos[0]][self.player_pos[1]] == 4:
            if len(self.red_boxes) == 0:
                self.show_win_message()
            else:
                self.feedback_label.config(text="Not all goblins have been defeated yet.")

    def display_math_question(self):
        if not self.math_question_active:
            self.math_question_active = True
            self.unbind_keys()

            self.question_window = tk.Toplevel(self.root)
            self.question_window.title("Math Question")
            self.question_window.geometry("800x700")
            self.question_window.configure(bg="#1D0200")

            self.center_window(self.question_window, 800, 700)

            self.question_window.attributes("-toolwindow", 1)
            self.question_window.protocol("WM_DELETE_WINDOW", lambda: None)

            question, self.correct_answer = self.generate_question()
            self.question_label = tk.Label(self.question_window, text=question, font=("Times New Roman", 18), bg="#1D0200", fg="white")
            self.question_label.pack(pady=10)

            self.answer_buttons = []
            answers = self.generate_answers(self.correct_answer)

            for i, answer in enumerate(answers):
                button = tk.Button(self.question_window, text=answer, 
                                command=lambda a=answer: self.check_answer(a), 
                                height=2, width=15, 
                                font=("Times New Roman", 16),
                                bg="#BB9351", fg="white",
                                relief="raised", bd=3)
                button.pack(pady=10)
                self.answer_buttons.append(button)

            self.root.bind("1", lambda event: self.check_answer(answers[0]))
            self.root.bind("2", lambda event: self.check_answer(answers[1]))
            self.root.bind("3", lambda event: self.check_answer(answers[2]))
            self.root.bind("4", lambda event: self.check_answer(answers[3]))

    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        position_x = (screen_width // 2) - (width // 2)
        position_y = (screen_height // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{position_x}+{position_y}')

    def generate_question(self):
        if self.mode == "Addition":
            a, b = random.randint(1, 10), random.randint(1, 10)
            return f"{a} + {b} =", a + b
        elif self.mode == "Subtraction":
            a, b = random.randint(1, 10), random.randint(1, 10)
            return f"{a} - {b} =", a - b
        elif self.mode == "Multiplication":
            a, b = random.randint(1, 10), random.randint(1, 10)
            return f"{a} x {b} =", a * b
        elif self.mode == "Division":
            b = random.randint(1, 10)
            a = b * random.randint(1, 10)
            return f"{a} ÷ {b} =", a // b
        else:
            return "Error", 0

    def generate_answers(self, correct_answer):
        answers = [correct_answer]
        while len(answers) < 4:
            wrong_answer = random.randint(1, 20)
            if wrong_answer != correct_answer:
                answers.append(wrong_answer)
        random.shuffle(answers)
        return answers

    def check_answer(self, user_answer):
        if user_answer == self.correct_answer:
            self.feedback_label.config(text="Correct!")
            self.correct_answers += 1

            current_pos = tuple(self.player_pos)
            if current_pos in self.red_boxes:
                self.red_boxes.remove(current_pos)
                self.solved_boxes.add(current_pos)
                self.maze[self.player_pos[0]][self.player_pos[1]] = 3

                self.draw_maze()
                self.draw_player()

        else:
            self.feedback_label.config(text="Incorrect!")
            self.incorrect_answers += 1
            self.time_elapsed += 1
            self.timer_label.config(text=f"Time: {self.time_elapsed}s")

        self.question_window.destroy()
        self.math_question_active = False
        self.bind_keys()

        self.root.unbind("1")
        self.root.unbind("2")
        self.root.unbind("3")
        self.root.unbind("4")

        self.check_for_events()

    def show_win_message(self):
        self.timer_running = False
        self.update_best_time()
        self.save_user_data()

        win_window = tk.Toplevel(self.root)
        win_window.title("Congratulations!")
        win_window.geometry("400x300")
        win_window.configure(bg="#1D0200")

        tk.Label(win_window, text=f"You've completed the level in {self.time_elapsed} seconds!\n"
                                f"Correct Answers: {self.correct_answers}, Incorrect Answers: {self.incorrect_answers}",
                font=("Times New Roman", 16), bg="#1D0200", fg="white").pack(pady=20)

        tk.Button(win_window, text="Return to Login", font=("Times New Roman", 14), bg="#BB9351", command=lambda: [win_window.destroy(), self.return_to_login()]).pack(pady=10)

        tk.Button(win_window, text="Return to Game Modes", font=("Times New Roman", 14), bg="#BB9351", command=lambda: [win_window.destroy(), self.show_setup_controls()]).pack(pady=10)

        tk.Button(win_window, text="Play Again", font=("Times New Roman", 14), bg="#BB9351", command=lambda: [win_window.destroy(), self.start_game(self.mode)]).pack(pady=10)

    def ask_return_to_login_or_setup(self):
        response = messagebox.askyesno("Return to Login?", "Do you want to return to the login page? (No will return to setup screen)")
        if response:
            self.return_to_login()
        else:
            for widget in self.root.winfo_children():                
                widget.destroy()
            self.show_setup_controls()

    def return_to_login(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.show_login_window()

    def update_best_time(self):
        mode_key = f"{self.mode}"
        if mode_key not in self.user_data[self.username]["times"]:
            self.user_data[self.username]["times"][mode_key] = self.time_elapsed
        else:
            self.user_data[self.username]["times"][mode_key] = min(self.user_data[self.username]["times"][mode_key], self.time_elapsed)

    def show_leaderboard(self):
        leaderboard_window = tk.Toplevel(self.root)
        leaderboard_window.title("Leaderboard")
        leaderboard_window.geometry("600x400")

        leaderboard_canvas = tk.Canvas(leaderboard_window, width=600, height=400)
        leaderboard_canvas.pack()
        leaderboard_canvas.configure(bg="#1D0200")
        leaderboard_canvas.create_text(300, 20, text="Leaderboard", font=("Times New Roman", 24),fill = "white")

        leaderboard_canvas.create_text(150, 60, text="Username", font=("Times New Roman", 18, "bold"), fill= "white")
        leaderboard_canvas.create_text(300, 60, text="Game Mode", font=("Times New Roman", 18, "bold"), fill= "white")
        leaderboard_canvas.create_text(450, 60, text="Time (s)", font=("Times New Roman", 18, "bold"), fill= "white")

        leaderboard_canvas.create_line(225, 40, 225, 380, fill="white")
        leaderboard_canvas.create_line(375, 40, 375, 380,fill="white")

        y_position = 100
        for username, data in self.user_data.items():
            if "times" in data:
                for mode, time in data["times"].items():
                    leaderboard_canvas.create_text(150, y_position, text=username, font=("Times New Roman", 16), fill= "white")
                    leaderboard_canvas.create_text(300, y_position, text=mode, font=("Times New Roman", 16), fill= "white")
                    leaderboard_canvas.create_text(450, y_position, text=str(time), font=("Times New Roman", 16), fill= "white")
                    y_position += 30


def main():
    root = tk.Tk()
    game = MathGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
