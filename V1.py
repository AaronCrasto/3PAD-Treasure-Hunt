import tkinter as tk
import random

class MathGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Math Game")

        # Initialize window size variables
        self.window_width = 1280
        self.window_height = 720
        self.root.geometry(f"{self.window_width}x{self.window_height}")

        self.score = 0
        self.difficulty = "Easy"  # Default difficulty level
        self.mode = "Addition"  # Default mode
        self.time_limit = 60  # Timer duration in seconds
        self.time_left = self.time_limit

        # Create login screen
        self.create_login_screen()

    def load_background_image(self):
        try:
            # Load the GIF image using tk.PhotoImage
            self.bg_image = tk.PhotoImage(file="space.png")  # Ensure the file is a .gif image
        except tk.TclError:
            print("Error: Background image file not found.")
            # Create a black image as a placeholder in case the image is not found
            self.bg_image = tk.PhotoImage(width=self.window_width, height=self.window_height)
            self.bg_image.put(("black",), to=(0, 0, self.window_width, self.window_height))

    def create_login_screen(self):
        self.clear_screen()

        self.login_label = tk.Label(self.root, text="Login", font=("Times New Roman", 24))
        self.login_label.pack(pady=20)

        # Username label and entry
        self.username_frame = tk.Frame(self.root)
        self.username_frame.pack(pady=5)
        self.username_label = tk.Label(self.username_frame, text="Username:", font=("Times New Roman", 18))
        self.username_label.pack(side="left", padx=10)
        self.username_entry = tk.Entry(self.username_frame, font=("Times New Roman", 18))
        self.username_entry.pack(side="left")

        # Password label and entry
        self.password_frame = tk.Frame(self.root)
        self.password_frame.pack(pady=5)
        self.password_label = tk.Label(self.password_frame, text="Password:", font=("Times New Roman", 18))
        self.password_label.pack(side="left", padx=10)
        self.password_entry = tk.Entry(self.password_frame, show="*", font=("Times New Roman", 18))
        self.password_entry.pack(side="left")

        # Error message label
        self.error_message = tk.Label(self.root, text="", font=("Times New Roman", 14), fg="red")
        self.error_message.pack(pady=5)

        self.login_button = tk.Button(self.root, text="Login", command=self.validate_login, font=("Times New Roman", 18), width=15)
        self.login_button.pack(pady=20)

    def validate_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            self.error_message.config(text="Username and Password cannot be empty.")
        elif len(username) > 12:
            self.error_message.config(text="Username cannot be longer than 12 characters.")
        elif not username.isalpha():
            self.error_message.config(text="Username must contain only letters.")
        elif not username.isalnum() or not password.isalnum():
            self.error_message.config(text="Username and Password must contain only letters and numbers.")
        else:
            self.error_message.config(text="")  # Clear the error message
            self.show_mode_selection_screen()

    def show_mode_selection_screen(self):
        self.clear_screen()

        self.mode_label = tk.Label(self.root, text="Choose Mode", font=("Times New Roman", 24))
        self.mode_label.pack(pady=20)

        self.addition_button = tk.Button(self.root, text="Addition", command=lambda: self.show_difficulty_options("Addition"), font=("Times New Roman", 18), width=20)
        self.addition_button.pack(pady=10)

        self.subtraction_button = tk.Button(self.root, text="Subtraction", command=lambda: self.show_difficulty_options("Subtraction"), font=("Times New Roman", 18), width=20)
        self.subtraction_button.pack(pady=10)

        self.multiplication_button = tk.Button(self.root, text="Multiplication", command=lambda: self.show_difficulty_options("Multiplication"), font=("Times New Roman", 18), width=20)
        self.multiplication_button.pack(pady=10)

        self.division_button = tk.Button(self.root, text="Division", command=lambda: self.show_difficulty_options("Division"), font=("Times New Roman", 18), width=20)
        self.division_button.pack(pady=10)

    def show_difficulty_options(self, mode):
        self.mode = mode
        self.clear_screen()

        self.difficulty_label = tk.Label(self.root, text="Choose Difficulty", font=("Times New Roman", 24))
        self.difficulty_label.pack(pady=20)

        self.easy_button = tk.Button(self.root, text="Easy", command=lambda: self.start_game("Easy"), font=("Times New Roman", 18), width=15)
        self.easy_button.pack(pady=10)

        self.hard_button = tk.Button(self.root, text="Hard", command=lambda: self.start_game("Hard"), font=("Times New Roman", 18), width=15)
        self.hard_button.pack(pady=10)

    def start_game(self, difficulty):
        self.difficulty = difficulty
        self.clear_screen()
        self.load_background_image()

        # Create background label
        self.bg_label = tk.Label(self.root, image=self.bg_image)
        self.bg_label.place(relwidth=1, relheight=1)

        # Score and timer labels
        self.score_label = tk.Label(self.root, text=f"Score: {self.score}", font=("Times New Roman", 24), bg='lightblue')
        self.score_label.place(relx=0.97, rely=0.01)  # Top right

        self.timer_label = tk.Label(self.root, text=f"Time left: {self.time_left}", font=("Times New Roman", 24), bg='lightblue')
        self.timer_label.place(x=10, y=10, anchor='nw')  # Top left

        # Problem label
        self.problem_label = tk.Label(self.root, text="", font=("Times New Roman", 24), bg='white')
        self.problem_label.place(relx=0.5, rely=0.3, anchor='center')

        # Create and place answer buttons in the four corners at the bottom
        self.create_answer_buttons()

        # Feedback label
        self.feedback_label = tk.Label(self.root, text="", font=("Times New Roman", 18), bg='lightblue')
        self.feedback_label.place(relx=0.5, rely=0.7, anchor='center')

        # Bind window resize event
        self.root.bind('<Configure>', self.on_resize)

        self.new_problem()
        self.update_timer()

    def on_resize(self, event):
        self.window_width = event.width
        self.window_height = event.height

        # Update background image label size
        self.bg_label.place(relwidth=1, relheight=1)

        # Update position of score and timer labels on resize
        self.score_label.place(x=self.window_width - 150, y=10, anchor='ne')
        self.timer_label.place(x=10, y=10, anchor='nw')

    def create_answer_buttons(self):
        self.answer_buttons_frame = tk.Frame(self.root)
        self.answer_buttons_frame.place(relx=0.5, rely=0.9, anchor='center')

        # Create a grid layout for buttons within the frame
        self.answer_buttons_frame.grid_columnconfigure(0, weight=1)
        self.answer_buttons_frame.grid_columnconfigure(1, weight=1)
        self.answer_buttons_frame.grid_rowconfigure(0, weight=1)
        self.answer_buttons_frame.grid_rowconfigure(1, weight=1)

        self.answer_buttons = []
        button_width = 20
        button_height = 2

        # Create and place answer buttons
        button_positions = [
            (0, 1),  # Bottom left
            (1, 1),  # Bottom right
            (0, 0),  # Top left
            (1, 0)   # Top right
        ]

        for i, (col, row) in enumerate(button_positions):
            button = tk.Button(self.answer_buttons_frame, text="", font=("Times New Roman", 18), width=button_width, height=button_height, relief=tk.RAISED, bd=3, command=lambda b=i: self.check_answer(b))
            button.grid(column=col, row=row, padx=10, pady=10, sticky='nsew')
            self.answer_buttons.append(button)

    def new_problem(self):
        if self.difficulty == "Easy":
            self.num1 = random.randint(1, 20)
            self.num2 = random.randint(1, 20)
        else:  # Hard difficulty
            self.num1 = random.randint(20, 100)
            self.num2 = random.randint(20, 100)

        if self.mode == "Addition":
            self.answer = self.num1 + self.num2
            self.problem_label.config(text=f"What is {self.num1} + {self.num2}?", bg='lightblue')

        elif self.mode == "Subtraction":
            self.num1 = max(self.num1, self.num2)  # Ensure positive results for subtraction
            self.num2 = min(self.num1, self.num2)
            self.answer = self.num1 - self.num2
            self.problem_label.config(text=f"What is {self.num1} - {self.num2}?", bg='lightblue')

        elif self.mode == "Multiplication":
            self.answer = self.num1 * self.num2
            self.problem_label.config(text=f"What is {self.num1} × {self.num2}?", bg='lightblue')

        elif self.mode == "Division":
            self.num2 = random.randint(1, 12)
            self.answer = random.randint(1, 12) * self.num2
            self.problem_label.config(text=f"What is {self.answer} ÷ {self.num2}?", bg='lightblue')

        # Set random choices for answer buttons
        self.answer_buttons_texts = random.sample(
            [self.answer, self.answer + random.randint(-10, 10), self.answer + random.randint(-10, 10), self.answer + random.randint(-10, 10)],
            4
        )

        for i, button in enumerate(self.answer_buttons):
            button.config(text=self.answer_buttons_texts[i])

    def check_answer(self, button_index):
        selected_answer = self.answer_buttons_texts[button_index]
        if selected_answer == self.answer:
            self.feedback_label.config(text="Correct!")
            self.score += 1
        else:
            self.feedback_label.config(text="Incorrect!")
            self.score -= 1

        self.score_label.config(text=f"Score: {self.score}")
        self.new_problem()

    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"Time left: {self.time_left}")
            self.root.after(1000, self.update_timer)
        else:
            self.timer_label.config(text="Time's up!")
            self.end_game()

    def end_game(self):
        self.clear_screen()
        self.final_score_label = tk.Label(self.root, text=f"Game Over! Your final score is {self.score}", font=("Times New Roman", 24))
        self.final_score_label.pack(pady=20)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MathGame(root)
    root.mainloop()