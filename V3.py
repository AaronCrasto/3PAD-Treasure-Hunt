import tkinter as tk
from tkinter import messagebox
import random
import json
import os

class MathGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Treasure")

        self.window_width = 1920
        self.window_height = 1080
        self.root.geometry(f"{self.window_width}x{self.window_height}")

        self.difficulty = "Easy"
        self.mode = None
        self.level = None

        self.CELL_SIZE = 60
        self.ROWS = 10
        self.COLS = 10

        self.wall_image = tk.PhotoImage(file="wall.png")
        self.wall_image = self.wall_image.subsample(1)

        self.player_image = tk.PhotoImage(file="wizard.png")
        self.player_image = self.resize_image(self.player_image, self.CELL_SIZE, self.CELL_SIZE)

        self.red_box_image = tk.PhotoImage(file="goblin1.png")
        self.red_box_image = self.resize_image(self.red_box_image, self.CELL_SIZE, self.CELL_SIZE)

        self.green_box_image = tk.PhotoImage(file="dirt .png")
        self.green_box_image = self.resize_image(self.green_box_image, self.CELL_SIZE, self.CELL_SIZE)

        self.empty_space_image = tk.PhotoImage(file="dirt .png")
        self.empty_space_image = self.resize_image(self.empty_space_image, self.CELL_SIZE, self.CELL_SIZE)

        self.exit_image = tk.PhotoImage(file="treasure.png")
        self.exit_image = self.resize_image(self.exit_image, self.CELL_SIZE, self.CELL_SIZE)

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

        self.show_login_window()
    
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

        username_label = tk.Label(self.login_canvas, text="Username", font=("Times New Roman", 18), bg="#1D0200", fg="white")
        self.login_canvas.create_window(self.window_width // 2, self.window_height * 0.4, window=username_label)

        self.username_entry = tk.Entry(self.login_canvas, font=("Times New Roman", 18))
        self.login_canvas.create_window(self.window_width // 2, self.window_height * 0.45, window=self.username_entry)

        password_label = tk.Label(self.login_canvas, text="Password", font=("Times New Roman", 18), bg="#1D0200", fg="white")
        self.login_canvas.create_window(self.window_width // 2, self.window_height * 0.5, window=password_label)

        self.password_entry = tk.Entry(self.login_canvas, show="*", font=("Times New Roman", 18))
        self.login_canvas.create_window(self.window_width // 2, self.window_height * 0.55, window=self.password_entry)

        login_button = tk.Button(self.login_canvas, text="Login", font=("Times New Roman", 18), command=self.check_login)
        self.login_canvas.create_window(self.window_width // 2, self.window_height * 0.65, window=login_button)

    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password.")
        else:
            self.username = username
            if self.username not in self.user_data:
                self.user_data[self.username] = {}
            self.login_canvas.destroy()
            self.show_setup_controls()

    def show_setup_controls(self):
        self.canvas = tk.Canvas(self.root, width=self.root.winfo_width(), height=self.root.winfo_height())
        self.canvas.pack(fill="both", expand=True)

        button_width = 800
        button_height = 400

        self.addition_button = tk.Button(self.root, image=self.addition_image, width=button_width, height=button_height,
                                     command=lambda: self.show_level_selection("Addition"))
        self.addition_button_window = self.canvas.create_window(100, 100, window=self.addition_button, anchor="nw")
        self.addition_button.bind("<Enter>", self.on_enter)
        self.addition_button.bind("<Leave>", self.on_leave)

        self.subtraction_button = tk.Button(self.root, image=self.subtraction_image, width=button_width, height=button_height,
                                        command=lambda: self.show_level_selection("Subtraction"))
        self.subtraction_button_window = self.canvas.create_window(1000, 100, window=self.subtraction_button, anchor="nw")
        self.subtraction_button.bind("<Enter>", self.on_enter)
        self.subtraction_button.bind("<Leave>", self.on_leave)

        self.multiplication_button = tk.Button(self.root, image=self.multiplication_image, width=button_width, height=button_height,
                                           command=lambda: self.show_level_selection("Multiplication"))
        self.multiplication_button_window = self.canvas.create_window(100, 600, window=self.multiplication_button, anchor="nw")
        self.multiplication_button.bind("<Enter>", self.on_enter)
        self.multiplication_button.bind("<Leave>", self.on_leave)

        self.division_button = tk.Button(self.root, image=self.division_image, width=button_width, height=button_height,
                                     command=lambda: self.show_level_selection("Division"))
        self.division_button_window = self.canvas.create_window(1000, 600, window=self.division_button, anchor="nw")
        self.division_button.bind("<Enter>", self.on_enter)
        self.division_button.bind("<Leave>", self.on_leave)

    def show_level_selection(self, mode):
        self.mode = mode

        self.canvas.delete(self.addition_button_window)
        self.canvas.delete(self.subtraction_button_window)
        self.canvas.delete(self.multiplication_button_window)
        self.canvas.delete(self.division_button_window)
        self.canvas.destroy()

        setup_label = tk.Label(self.root, text=f"Choose a level for {mode}:", font=("Times New Roman", 18))
        setup_label.pack(pady=20)

        for level in range(1, 6):
            button = tk.Button(self.root, text=f"Level {level}", width=15, height=2,
                               command=lambda lvl=level: self.start_game(lvl))
            button.pack(pady=10)

    def start_game(self, level):
        self.level = level
        
        for widget in self.root.winfo_children():
            widget.pack_forget()

        self.initialize_maze()

        self.canvas = tk.Canvas(self.root, width=self.COLS * self.CELL_SIZE, height=self.ROWS * self.CELL_SIZE, bg='white')
        self.canvas.pack(pady=20)

        self.timer_label.pack(anchor='ne', padx=20, pady=10)
        self.feedback_label.pack(pady=10)

        self.draw_maze()
        self.draw_player()

        self.timer_running = True
        self.time_elapsed = 0
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
        mazes = {
            1: [
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 2, 1],
                [1, 0, 1, 1, 1, 0, 1, 0, 0, 1],
                [1, 0, 0, 0, 1, 0, 1, 1, 0, 1],
                [1, 1, 1, 0, 1, 0, 0, 0, 0, 1],
                [1, 0, 2, 0, 1, 1, 1, 1, 0, 1],
                [1, 0, 1, 0, 0, 0, 2, 1, 0, 1],
                [1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 2, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 4, 1],
            ],
            2: [
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 2, 1, 0, 0, 0, 2, 1],
                [1, 0, 1, 1, 1, 1, 1, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 1, 1, 0, 1],
                [1, 1, 1, 1, 1, 0, 0, 0, 0, 1],
                [1, 0, 2, 0, 1, 1, 1, 1, 0, 1],
                [1, 0, 1, 0, 0, 0, 2, 1, 0, 1],
                [1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 2, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 4, 1],
            ],
            3: [
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 2, 1],
                [1, 0, 1, 1, 1, 0, 1, 0, 0, 1],
                [1, 0, 0, 0, 1, 0, 1, 1, 0, 1],
                [1, 1, 1, 0, 1, 0, 0, 0, 0, 1],
                [1, 0, 2, 0, 1, 1, 1, 1, 0, 1],
                [1, 0, 1, 0, 0, 0, 2, 1, 0, 1],
                [1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 2, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 4, 1],
            ],
            4: [
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 2, 0, 0, 0, 2, 1],
                [1, 0, 1, 1, 1, 1, 1, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 1, 1, 0, 1],
                [1, 1, 1, 1, 1, 0, 0, 0, 0, 1],
                [1, 0, 2, 0, 1, 1, 1, 1, 0, 1],
                [1, 0, 1, 0, 0, 0, 2, 1, 0, 1],
                [1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 2, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 4, 1],
            ],
            5: [
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 2, 0, 0, 0, 2, 1],
                [1, 0, 1, 1, 1, 1, 1, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 1, 1, 0, 1],
                [1, 1, 1, 1, 1, 0, 0, 0, 0, 1],
                [1, 0, 2, 0, 1, 1, 1, 1, 0, 1],
                [1, 0, 1, 0, 0, 0, 2, 1, 0, 1],
                [1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 2, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 4, 1],
            ]
        }

        self.maze = mazes[self.level]

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
                if cell_value == 1:
                    self.canvas.create_image(x, y, anchor=tk.NW, image=self.wall_image)
                elif cell_value == 2:
                    self.canvas.create_image(x, y, anchor=tk.NW, image=self.red_box_image)
                    self.red_boxes.add((row, col))
                elif cell_value == 3:
                    self.canvas.create_image(x, y, anchor=tk.NW, image=self.green_box_image)
                elif cell_value == 4:
                    self.canvas.create_image(x, y, anchor=tk.NW, image=self.exit_image)
                else:
                    self.canvas.create_image(x, y, anchor=tk.NW, image=self.empty_space_image)

    def draw_player(self):
        x = self.player_pos[1] * self.CELL_SIZE
        y = self.player_pos[0] * self.CELL_SIZE
        self.canvas.create_image(x, y, anchor=tk.NW, image=self.player_image)

    def move_player(self, dx, dy):
        new_row = self.player_pos[0] + dy
        new_col = self.player_pos[1] + dx

        if 0 <= new_row < self.ROWS and 0 <= new_col < self.COLS:
            if self.maze[new_row][new_col] != 1:
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
                self.feedback_label.config(text="Not all red boxes are solved yet.")

    def display_math_question(self):
        if not self.math_question_active:
            self.math_question_active = True
            self.unbind_keys()

            self.question_window = tk.Toplevel(self.root)
            self.question_window.title("Math Question")
            self.question_window.geometry("400x300")

            self.question_window.protocol("WM_DELETE_WINDOW", lambda: None)

            question, self.correct_answer = self.generate_question()
            self.question_label = tk.Label(self.question_window, text=question, font=("Times New Roman", 18))
            self.question_label.pack(pady=10)

            self.answer_buttons = []
            for answer in self.generate_answers(self.correct_answer):
                button = tk.Button(self.question_window, text=answer, 
                                   command=lambda a=answer: self.check_answer(a), 
                                   height=2, width=15, 
                                   font=("Times New Roman", 16))
                button.pack(pady=10)
                self.answer_buttons.append(button)

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
            a, b = random.randint(1, 10), random.randint(1, 10)
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

            current_pos = tuple(self.player_pos)
            if current_pos in self.red_boxes:
                self.red_boxes.remove(current_pos)
                self.solved_boxes.add(current_pos)
                self.maze[self.player_pos[0]][self.player_pos[1]] = 3
                self.draw_maze()
        else:
            self.feedback_label.config(text="Incorrect!")

        self.question_window.destroy()
        self.math_question_active = False
        self.bind_keys()

        self.check_for_events()

    def show_win_message(self):
        self.timer_running = False
        self.update_best_time()
        self.save_user_data()

        response = messagebox.askyesno("Congratulations!", "You've completed the level! Do you want to proceed to the next level?")
        if response and self.level < 5:
            self.start_game(self.level + 1)
        else:
            self.show_setup_controls()

    def update_best_time(self):
        mode_level_key = f"{self.mode}_Level_{self.level}"
        if mode_level_key not in self.user_data[self.username]:
            self.user_data[self.username][mode_level_key] = self.time_elapsed
        else:
            self.user_data[self.username][mode_level_key] = min(self.user_data[self.username][mode_level_key], self.time_elapsed)

root = tk.Tk()
game = MathGame(root)
root.mainloop()
