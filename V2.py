import tkinter as tk
import random

class MathGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Math Maze Game")

        # Initialize window size variables
        self.window_width = 1280
        self.window_height = 720
        self.root.geometry(f"{self.window_width}x{self.window_height}")

        self.username = None
        self.score = 0
        self.difficulty = "Easy"  # Default difficulty level
        self.mode = None  # Mode will be set after user selection
        self.level = 0  # Start at level 0 (first level)
        self.time_limit = 60  # Timer duration in seconds
        self.time_left = self.time_limit

        # Maze settings
        self.CELL_SIZE = 60  # Size of each cell in the maze
        self.ROWS = 10       # Number of rows in the maze
        self.COLS = 10       # Number of columns in the maze

        # Maze layouts for each level (10 levels)
        self.mazes = [
            [
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 1, 2, 1],
                [1, 0, 1, 1, 1, 0, 1, 0, 0, 1],
                [1, 0, 0, 0, 1, 0, 1, 1, 0, 1],
                [1, 1, 1, 0, 1, 0, 0, 0, 0, 1],
                [1, 0, 2, 0, 1, 1, 1, 1, 0, 1],
                [1, 0, 1, 0, 0, 0, 2, 1, 0, 1],
                [1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 2, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 4, 1],  # Exit placed here
            ],
            [
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 1, 1, 0, 1, 2, 1],
                [1, 1, 1, 0, 1, 0, 1, 0, 0, 1],
                [1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
                [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
                [1, 0, 2, 1, 1, 1, 1, 1, 0, 1],
                [1, 0, 1, 0, 0, 0, 2, 0, 0, 1],
                [1, 0, 1, 1, 1, 0, 0, 1, 0, 1],
                [1, 2, 0, 0, 0, 1, 0, 2, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 4, 1],  # Exit placed here
            ],
            # Add additional maze layouts here for levels 3 to 10
        ]

        # Player starting position
        self.player_pos = [1, 1]
        self.math_question_active = False
        self.red_boxes = set()  # Set to keep track of red boxes

        # Create canvas for maze (but do not pack yet)
        self.canvas = tk.Canvas(self.root, width=self.COLS * self.CELL_SIZE, height=self.ROWS * self.CELL_SIZE, bg='white')

        # Score and timer labels (do not pack yet)
        self.score_label = tk.Label(self.root, text=f"Score: {self.score}", font=("Times New Roman", 24))
        self.timer_label = tk.Label(self.root, text=f"Time left: {self.time_left}", font=("Times New Roman", 24))

        # Feedback label (do not pack yet)
        self.feedback_label = tk.Label(self.root, text="", font=("Times New Roman", 18))

        # Show the login screen first
        self.show_login_screen()

    def show_login_screen(self):
        # Create login widgets
        self.login_label = tk.Label(self.root, text="Enter your username:", font=("Times New Roman", 18))
        self.login_label.pack(pady=20)

        self.username_entry = tk.Entry(self.root, font=("Times New Roman", 18))
        self.username_entry.pack(pady=10)

        self.login_button = tk.Button(self.root, text="Login", font=("Times New Roman", 18), command=self.process_login)
        self.login_button.pack(pady=20)

    def process_login(self):
        self.username = self.username_entry.get().strip()
        if self.username:
            # Hide login widgets
            self.login_label.pack_forget()
            self.username_entry.pack_forget()
            self.login_button.pack_forget()

            # Show the game mode selection
            self.show_setup_controls()

    def show_setup_controls(self):
        # Instruction label
        setup_label = tk.Label(self.root, text="Choose the type of math questions:", font=("Times New Roman", 18))
        setup_label.pack(pady=20)

        # Mode selection buttons
        button_width = 15
        button_height = 2

        self.addition_button = tk.Button(self.root, text="Addition", width=button_width, height=button_height,
                                    command=lambda: self.start_game("Addition"))
        self.addition_button.pack(pady=10)

        self.subtraction_button = tk.Button(self.root, text="Subtraction", width=button_width, height=button_height,
                                       command=lambda: self.start_game("Subtraction"))
        self.subtraction_button.pack(pady=10)

        self.multiplication_button = tk.Button(self.root, text="Multiplication", width=button_width, height=button_height,
                                          command=lambda: self.start_game("Multiplication"))
        self.multiplication_button.pack(pady=10)

        self.division_button = tk.Button(self.root, text="Division", width=button_width, height=button_height,
                                    command=lambda: self.start_game("Division"))
        self.division_button.pack(pady=10)

    def start_game(self, mode):
        self.mode = mode
        self.level = 0  # Start at the first level
        
        # Hide the setup buttons
        self.addition_button.pack_forget()
        self.subtraction_button.pack_forget()
        self.multiplication_button.pack_forget()
        self.division_button.pack_forget()

        # Hide setup label
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Label) and "Choose the type of math questions:" in widget.cget("text"):
                widget.pack_forget()

        # Pack the canvas and labels now that the game is starting
        self.canvas.pack()
        self.score_label.pack(anchor='ne', padx=20, pady=10)
        self.timer_label.pack(anchor='nw', padx=20, pady=10)
        self.feedback_label.pack(pady=10)

        # Bind arrow keys to move the player
        self.root.bind('<Up>', self.move_player)
        self.root.bind('<Down>', self.move_player)
        self.root.bind('<Left>', self.move_player)
        self.root.bind('<Right>', self.move_player)

        self.load_level()
        self.update_timer()  # Start the timer

    def load_level(self):
        self.maze = self.mazes[self.level]  # Load the maze layout for the current level
        self.player_pos = [1, 1]  # Reset player position for each level
        self.red_boxes.clear()  # Clear any red box tracking
        self.math_question_active = False  # Reset the math question state
        self.draw_maze()
        self.draw_player()

    def draw_maze(self):
        self.canvas.delete("all")
        for row in range(self.ROWS):
            for col in range(self.COLS):
                cell = self.maze[row][col]
                if cell == 1:
                    self.canvas.create_rectangle(
                        col * self.CELL_SIZE, row * self.CELL_SIZE,
                        (col + 1) * self.CELL_SIZE, (row + 1) * self.CELL_SIZE,
                        fill='black'
                    )
                elif cell == 2:
                    self.canvas.create_rectangle(
                        col * self.CELL_SIZE, row * self.CELL_SIZE,
                        (col + 1) * self.CELL_SIZE, (row + 1) * self.CELL_SIZE,
                        fill='red'
                    )
                    self.red_boxes.add((row, col))  # Add red box position to the set
                elif cell == 3:
                    self.canvas.create_rectangle(
                        col * self.CELL_SIZE, row * self.CELL_SIZE,
                        (col + 1) * self.CELL_SIZE, (row + 1) * self.CELL_SIZE,
                        fill='green'
                    )
                elif cell == 4:
                    self.canvas.create_rectangle(
                        col * self.CELL_SIZE, row * self.CELL_SIZE,
                        (col + 1) * self.CELL_SIZE, (row + 1) * self.CELL_SIZE,
                        fill='purple'
                    )
                else:
                    self.canvas.create_rectangle(
                        col * self.CELL_SIZE, row * self.CELL_SIZE,
                        (col + 1) * self.CELL_SIZE, (row + 1) * self.CELL_SIZE,
                        fill='white'
                    )

    def draw_player(self):
        self.player_oval = self.canvas.create_oval(
            self.player_pos[1] * self.CELL_SIZE, self.player_pos[0] * self.CELL_SIZE,
            (self.player_pos[1] + 1) * self.CELL_SIZE, (self.player_pos[0] + 1) * self.CELL_SIZE,
            fill='blue'
        )

    def move_player(self, event):
        if self.math_question_active:
            return  # Prevent movement when a question is active

        row, col = self.player_pos

        if event.keysym == 'Up':
            new_row, new_col = row - 1, col
        elif event.keysym == 'Down':
            new_row, new_col = row + 1, col
        elif event.keysym == 'Left':
            new_row, new_col = row, col - 1
        elif event.keysym == 'Right':
            new_row, new_col = row, col + 1
        else:
            return

        # Check if new position is inside the maze and is not a wall
        if 0 <= new_row < self.ROWS and 0 <= new_col < self.COLS:
            if self.maze[new_row][new_col] == 0 or self.maze[new_row][new_col] == 3:
                self.player_pos = [new_row, new_col]
                self.canvas.delete(self.player_oval)
                self.draw_player()
            elif self.maze[new_row][new_col] == 2:
                self.player_pos = [new_row, new_col]
                self.canvas.delete(self.player_oval)
                self.draw_player()
                self.math_question_active = True
                self.open_math_question_window()
            elif self.maze[new_row][new_col] == 4:
                if not self.red_boxes:  # Check if all red boxes are green
                    self.advance_level()
                else:
                    self.feedback_label.config(text="You need to turn all red boxes to green to exit.")

    def open_math_question_window(self):
        # Create a new window for the math question
        self.math_window = tk.Toplevel(self.root)
        self.math_window.title("Answer the Question")
        self.math_window.geometry("800x800")  # Resize the window

        # Problem label
        self.problem_label = tk.Label(self.math_window, text="", font=("Times New Roman", 24))
        self.problem_label.pack(pady=20)

        # Answer buttons
        self.answer_buttons_frame = tk.Frame(self.math_window)
        self.answer_buttons_frame.pack(pady=10)

        self.answer_buttons = []
        button_width = 10
        button_height = 2

        for i in range(4):
            button = tk.Button(self.answer_buttons_frame, text="", font=("Times New Roman", 18), width=button_width, height=button_height, relief=tk.RAISED, bd=3, command=lambda b=i: self.check_answer(b))
            button.grid(row=0, column=i, padx=10, pady=10)
            self.answer_buttons.append(button)

        self.new_problem()  # Generate and display a new problem in the new window

    def new_problem(self):
        # Generate math problem based on difficulty and mode
        if self.difficulty == "Easy":
            self.num1 = random.randint(1, 20)
            self.num2 = random.randint(1, 20)
        else:
            self.num1 = random.randint(20, 100)
            self.num2 = random.randint(20, 100)

        if self.mode == "Addition":
            self.answer = self.num1 + self.num2
            self.problem_label.config(text=f"What is {self.num1} + {self.num2}?")

        elif self.mode == "Subtraction":
            self.num1 = max(self.num1, self.num2)  # Ensure positive results for subtraction
            self.num2 = min(self.num1, self.num2)
            self.answer = self.num1 - self.num2
            self.problem_label.config(text=f"What is {self.num1} - {self.num2}?")

        elif self.mode == "Multiplication":
            self.answer = self.num1 * self.num2
            self.problem_label.config(text=f"What is {self.num1} × {self.num2}?")

        elif self.mode == "Division":
            self.num2 = random.randint(1, 12)
            self.answer = random.randint(1, 12) * self.num2
            self.problem_label.config(text=f"What is {self.answer} ÷ {self.num2}?")

        # Set random choices for answer buttons
        choices = [self.answer,
                   self.answer + random.randint(-10, 10),
                   self.answer + random.randint(-10, 10),
                   self.answer + random.randint(-10, 10)]
        random.shuffle(choices)

        self.answer_buttons_texts = choices  # Store the texts for easy checking

        for i, choice in enumerate(choices):
            self.answer_buttons[i].config(text=choice, state='normal')  # Enable and set text

    def check_answer(self, button_index):
        selected_answer = self.answer_buttons_texts[button_index]

        if selected_answer == self.answer:
            self.feedback_label.config(text="Correct!")
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")
            self.math_question_active = False
            self.problem_label.config(text="")
            for button in self.answer_buttons:
                button.config(state='disabled')  # Disable buttons after correct answer
            self.math_window.destroy()  # Close the math question window

            # Change the red box to green in the maze
            row, col = self.player_pos
            self.maze[row][col] = 3  # Change the red box to green
            self.red_boxes.discard((row, col))  # Remove the green box from the set
            self.draw_maze()
        else:
            self.feedback_label.config(text="Incorrect! Try again.")

    def advance_level(self):
        self.level += 1
        if self.level < len(self.mazes):
            self.load_level()
        else:
            self.show_win_message()

    def show_win_message(self):
        win_window = tk.Toplevel(self.root)
        win_window.title("Congratulations!")
        win_window.geometry("800x800")

        win_label = tk.Label(win_window, text="You Win!", font=("Times New Roman", 24))
        win_label.pack(pady=20)

        self.root.after(3000, win_window.destroy)  # Close the win window after 3 seconds

    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"Time left: {self.time_left}")
            self.root.after(1000, self.update_timer)
        else:
            self.feedback_label.config(text="Time's up!")
            for button in self.answer_buttons:
                button.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    game = MathGame(root)
    root.mainloop()
