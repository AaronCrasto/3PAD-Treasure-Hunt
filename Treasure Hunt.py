# Author: Aaron Crasto, Date: 3/9/2024 
# The purpose of the program is to develop a curriculum that will help students become more proficient mathematicians


import tkinter as tk  # This line of code imports the tkinter module for creating the GUI.
from tkinter import messagebox  # This line of code imports the messagebox from tkinter for dialog boxes.
import random  # This line of code imports the random module to generate random numbers.
import json  # This line of code imports the json module to read and write user data.
import os  # This line of code imports the os module to check file existence and other OS-related operations.
import re  # This line of code imports the re module to work with regular expressions.

# This line of code defines the TimeTracker class to handle the timing functionality for the game.
class TimeTracker:
    def __init__(self, root, label):

        self.root = root  # This line of code initializes the root attribute with the main Tkinter window.
        self.label = label  # This line of code initializes the label attribute to display time.
        self.time_elapsed = 0  # This line of code initializes the time_elapsed attribute to track the elapsed time.
        self.timer_running = False  # This line of code initializes the timer_running attribute to track if the timer is running.

    def start(self):

        self.timer_running = True  # This line of code sets the timer_running attribute to True to start the timer.
        self.update_timer()  # This line of code calls the update_timer method to update the timer.

    def stop(self):

        self.timer_running = False  # This line of code sets the timer_running attribute to False to stop the timer.

    def reset(self):
        self.time_elapsed = 0  # This line of code resets the time_elapsed attribute to zero.
        self.update_label()  # This line of code updates the label to reflect the reset time.

    def update_timer(self):
        if self.timer_running:  # This line of code checks if the timer is running.
            self.time_elapsed += 1  # This line of code increments the time_elapsed attribute by 1 second.
            self.update_label()  # This line of code updates the label with the new time.
            self.root.after(1000, self.update_timer)  # This line of code schedules the update_timer method to be called after 1 second.

    def update_label(self):
        self.label.config(text=f"Time: {self.time_elapsed}s")  # This line of code updates the label text to show the current time.

    def get_time(self):
        return self.time_elapsed  # This line of code returns the current elapsed time.

# This line of code defines the MathGame class to manage the main game logic, including the GUI setup and game mechanics.


class MathGame:
    def __init__(self, root):

        self.root = root  # This line of code initializes the root attribute with the main Tkinter window.
        self.root.title("Treasure")  # This line of code sets the window title to "Treasure".
        
        self.root.protocol("WM_DELETE_WINDOW", self.confirm_close)  # This line of code sets the protocol for the window close button.

        # This block of code sets the window dimensions and geometry.
        self.window_width = 1920
        self.window_height = 1080
        self.root.geometry(f"{self.window_width}x{self.window_height}")

        # This block of code initializes the game settings.
        self.difficulty = "Easy"  # This line of code sets the default difficulty to "Easy".
        self.mode = None  # This line of code initializes the mode attribute with None, as no game mode is selected initially.

        # This block of code sets constants for the maze dimensions.
        self.CELL_SIZE = 60  # This line of code sets the size of each cell in the maze.
        self.ROWS = 16  # This line of code sets the number of rows in the maze.
        self.COLS = 30  # This line of code sets the number of columns in the maze.

        # This block of code loads images for different game elements.
        self.wall_image = tk.PhotoImage(file="wall.png")  # This line of code loads the wall image.
        self.wall_image = self.wall_image.subsample(1)  # This line of code resizes the wall image.
        self.player_image = tk.PhotoImage(file="wizard.png")  # This line of code loads the player image.
        self.player_image = self.resize_image(self.player_image, self.CELL_SIZE, self.CELL_SIZE)  # This line of code resizes the player image.

        self.red_box_image = tk.PhotoImage(file="goblin1.png")  # This line of code loads the goblin image.
        self.red_box_image = self.resize_image(self.red_box_image, self.CELL_SIZE, self.CELL_SIZE)  # This line of code resizes the goblin image.

        self.green_box_image = tk.PhotoImage(file="dirt .png")  # This line of code loads the correct answer box image.
        self.green_box_image = self.resize_image(self.green_box_image, self.CELL_SIZE, self.CELL_SIZE)  # This line of code resizes the correct answer box image.

        self.empty_space_image = tk.PhotoImage(file="dirt .png")  # This line of code loads the empty space image.
        self.empty_space_image = self.resize_image(self.empty_space_image, self.CELL_SIZE, self.CELL_SIZE)  # This line of code resizes the empty space image.

        self.exit_image = tk.PhotoImage(file="treasure.png")  # This line of code loads the exit/treasure image.
        self.exit_image = self.resize_image(self.exit_image, self.CELL_SIZE, self.CELL_SIZE)  # This line of code resizes the exit/treasure image.

        # This block of code loads images for math operation selection.
        self.addition_image = tk.PhotoImage(file="Addition 1.png")  # This line of code loads the addition operation image.
        self.subtraction_image = tk.PhotoImage(file="Subtraction .png")  # This line of code loads the subtraction operation image.
        self.multiplication_image = tk.PhotoImage(file="Multiplication .png")  # This line of code loads the multiplication operation image.
        self.division_image = tk.PhotoImage(file="Division .png")  # This line of code loads the division operation image.
        self.maze_background_image = tk.PhotoImage(file="Screen.png")  # This line of code loads the maze background image.

        self.maze = []  # This line of code initializes the maze as an empty list.

        self.player_pos = [1, 1]  # This line of code sets the initial player position in the maze.
        self.math_question_active = False  # This line of code initializes the math_question_active attribute to False.
        self.red_boxes = set()  # This line of code initializes a set to track the positions of red boxes (goblins).
        self.solved_boxes = set()  # This line of code initializes a set to track solved red boxes.

        self.time_elapsed = 0  # This line of code initializes the time_elapsed attribute to zero.
        self.timer_label = tk.Label(self.root, text="Time: 0s", font=("Times New Roman", 24))  # This line of code creates a label to show time.
        self.timer_running = False  # This line of code initializes the timer_running attribute to False.

        self.feedback_label = tk.Label(self.root, text="", font=("Times New Roman", 18))  # This line of code creates a label for feedback messages.

        self.user_data_file = "user_data.json"  # This line of code sets the file path for storing user data.
        self.load_user_data()  # This line of code calls the load_user_data method to load user data from the file.

        self.correct_answers = 0  # This line of code initializes the correct_answers counter to zero.
        self.incorrect_answers = 0  # This line of code initializes the incorrect_answers counter to zero.

        self.show_login_window()  # This line of code calls the show_login_window method to display the login window.

    def confirm_close(self):

        """Handles the window close event with a confirmation dialog."""

        if messagebox.askokcancel("Quit", "Do you really want to quit?"):
            self.root.destroy()  # This line of code destroys the window if the user confirms they want to quit.

    def on_enter(self, event):

        """Handle mouse entering a button (for hover effect)."""

        event.widget.config(relief=tk.RAISED)  # This line of code changes the button appearance to raised on hover.

    def on_leave(self, event):

        """Handles mouse leaving a button (for hover effect)."""
        event.widget.config(relief=tk.FLAT)  # This line of code reverts the button appearance to flat when hover ends.

    def load_user_data(self):

        """Load user data from a JSON file."""
        if os.path.exists(self.user_data_file):  # This line of code checks if the user data file exists.
            with open(self.user_data_file, 'r') as file:
                self.user_data = json.load(file)  # This line of code loads user data from the JSON file.
        else:
            self.user_data = {}  # This line of code initializes an empty user data dictionary if the file doesn't exist.

    def save_user_data(self):
        """Save user data to a JSON file."""
        with open(self.user_data_file, 'w') as file:
            json.dump(self.user_data, file, indent=4)  # This line of code saves user data to the JSON file.

    def show_login_window(self):

        """Display the login window with input fields and buttons."""

        self.login_canvas = tk.Canvas(self.root, width=self.window_width, height=self.window_height)  # This line of code creates a canvas for the login screen.
        self.login_canvas.pack(fill="both", expand=True)  # This line of code expands the canvas to fill the window.

        self.background_image = tk.PhotoImage(file="login screen.png")  # This line of code loads the background image for the login screen.
        self.login_canvas.create_image(0, 0, image=self.background_image, anchor=tk.NW)  # This line of code places the background image on the canvas.

        self.additional_image = tk.PhotoImage(file="Treasure Hunt.png")  # This line of code loads an additional image for the login screen.
        self.login_canvas.create_image(self.window_width // 2, self.window_height * 0.15, image=self.additional_image, anchor=tk.N)  # This line of code places the additional image.

        # This block of code creates a username label and entry field.
        username_label = tk.Label(self.login_canvas, text="Username", font=("Times New Roman", 18), bg="#1D0200", fg="white")
        self.login_canvas.create_window(self.window_width // 2, self.window_height * 0.4, window=username_label)

        self.username_entry = tk.Entry(self.login_canvas, font=("Times New Roman", 18))  # This line of code creates the username entry field.
        self.login_canvas.create_window(self.window_width // 2, self.window_height * 0.45, window=self.username_entry)

        # This block of code creates a password label and entry field.
        password_label = tk.Label(self.login_canvas, text="Password", font=("Times New Roman", 18), bg="#1D0200", fg="white")
        self.login_canvas.create_window(self.window_width // 2, self.window_height * 0.5, window=password_label)

        self.password_entry = tk.Entry(self.login_canvas, show="*", font=("Times New Roman", 18))  # This line of code creates the password entry field.
        self.login_canvas.create_window(self.window_width // 2, self.window_height * 0.55, window=self.password_entry)

        # This block of code creates the login button.
        login_button = tk.Button(self.login_canvas, text="Login", height=1, width=20, font=("Times New Roman", 18), bg="#BB9351", command=self.check_login)
        self.login_canvas.create_window(self.window_width // 2, self.window_height * 0.65, window=login_button)

        # This block of code creates the leaderboard button.
        leaderboard_button = tk.Button(self.login_canvas, text="Leaderboard", height=1, width=20, font=("Times New Roman", 18), bg="#BB9351", command=self.show_leaderboard)
        self.login_canvas.create_window(self.window_width // 2, self.window_height * 0.75, window=leaderboard_button)

        # This block of code creates the create account button.
        create_account_button = tk.Button(self.login_canvas, text="Create Account", height=1, width=20, font=("Times New Roman", 18), bg="#BB9351", command=self.show_create_account_window)
        self.login_canvas.create_window(self.window_width // 2, self.window_height * 0.85, window=create_account_button)

        # This block of code creates the How to Play button.
        how_to_play_button = tk.Button(self.login_canvas, text="How to Play ?", height=1, width=20, font=("Times New Roman", 18), bg="#BB9351", command=self.show_how_to_play)
        self.login_canvas.create_window(self.window_width // 2, self.window_height * 0.95, window=how_to_play_button)

    def show_how_to_play(self):

        """Display a window with instructions on how to play the game."""

        how_to_play_window = tk.Toplevel(self.root)  # This line of code creates a new top-level window for the instructions.
        how_to_play_window.title("How to Play")  # This line of code sets the title for the instructions window.
        how_to_play_window.geometry("900x700")  # This line of code sets the window size.
        how_to_play_window.configure(bg="#1D0200")  # This line of code sets the background color.

        # This line of code adds a title label to the instructions window.
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

        # This line of code displays the instructions text in the instructions window.
        tk.Label(how_to_play_window, text=instructions, font=("Times New Roman", 16), bg="#1D0200", fg="white", justify=tk.LEFT).pack(pady=20, padx=20)

    def check_login(self):

        """Verifies the user's login credentials."""

        username = self.username_entry.get()  # This line of code gets the entered username.
        password = self.password_entry.get()  # This line of code gets the entered password.

        if not self.validate_username(username):  # This line of code checks if the username is valid using the validate_username method.
            messagebox.showerror("Error", "Invalid username. Must be 1-15 characters long and contain only letters, numbers, or underscores.")  # This line of code shows an error message if the username is invalid.
            return

        if not username or not password:  # This line of code checks if both username and password are provided.
            messagebox.showerror("Error", "Please enter both username and password.")  # This line of code shows an error message if either field is empty.
        else:
            self.username = username  # This line of code sets the username attribute.
            if self.username not in self.user_data:  # This line of code checks if the username exists in user data.
                messagebox.showerror("Error", "Username not found. Please create an account.")  # This line of code shows an error message if the username is not found.
                return
            elif self.user_data[self.username]["password"] != password:  # This line of code checks if the entered password matches the stored password.
                messagebox.showerror("Error", "Incorrect password.")  # This line of code shows an error message if the password is incorrect.
                return

            self.save_user_data()  # This line of code calls the save_user_data method to save user data.

            self.login_canvas.destroy()  # This line of code removes the login canvas from the window.
            self.show_setup_controls()  # This line of code calls the show_setup_controls method to display the game setup controls.

    def show_create_account_window(self):

        """Displays a window for creating a new user account."""

        self.create_account_window = tk.Toplevel(self.root)  # This line of code creates a new window for account creation.
        self.create_account_window.title("Create Account")  # This line of code sets the window title.
        self.create_account_window.geometry("400x300")  # This line of code sets the window size.
        self.create_account_window.configure(bg="#1D0200")  # This line of code sets the background color.

        # This block of code creates the account creation form.
        tk.Label(self.create_account_window, text="Create a New Account", font=("Times New Roman", 18), bg="#1D0200", fg="white").pack(pady=10)

        tk.Label(self.create_account_window, text="Username", font=("Times New Roman", 14), bg="#1D0200", fg="white").pack()
        self.new_username_entry = tk.Entry(self.create_account_window, font=("Times New Roman", 14))  # This line of code creates the new username entry field.
        self.new_username_entry.pack(pady=5)

        tk.Label(self.create_account_window, text="Password", font=("Times New Roman", 14), bg="#1D0200", fg="white").pack()
        self.new_password_entry = tk.Entry(self.create_account_window, show="*", font=("Times New Roman", 14))  # This line of code creates the new password entry field.
        self.new_password_entry.pack(pady=5)

        tk.Button(self.create_account_window, text="Create Account", font=("Times New Roman", 14), command=self.create_account, bg="#BB9351").pack(pady=20)  # This line of code creates the submit button for account creation.

    def create_account(self):

        """Create a new user account and save it."""

        new_username = self.new_username_entry.get()  # This line of code gets the entered new username.
        new_password = self.new_password_entry.get()  # This line of code gets the entered new password.

        if not self.validate_username(new_username):  # This line of code checks if the new username is valid using the validate_username method.
            messagebox.showerror("Error", "Invalid username. Must be 1-15 characters long and contain only letters, numbers, or underscores.")  # This line of code shows an error message if the username is invalid.
            return

        if not new_username or not new_password:  # This line of code checks if both new username and password fields are filled.
            messagebox.showerror("Error", "Please fill in both fields.")  # This line of code shows an error message if either field is empty.
            return

        if new_username in self.user_data:  # This line of code checks if the new username already exists in user data.
            messagebox.showerror("Error", "Username already exists. Please choose a different one.")  # This line of code shows an error message if the username already exists.
            return

        self.user_data[new_username] = {"password": new_password, "times": {}}  # This line of code adds the new user to user data.
        self.save_user_data()  # This line of code calls the save_user_data method to save user data.
        messagebox.showinfo("Success", "Account created successfully!")  # This line of code shows a success message if the account is created successfully.
        self.create_account_window.destroy()  # This line of code closes the account creation window.

    def validate_username(self, username):

        """Validates the username to ensure it meets the criteria."""

        return re.match(r'^[A-Za-z0-9_]{1,15}$', username) is not None  # This line of code uses regex to validate if the username is 1-15 characters long and contains only letters, numbers, or underscores.

    def show_setup_controls(self):

        """Display the controls for setting up the game."""

        self.canvas = tk.Canvas(self.root, width=self.root.winfo_width(), height=self.root.winfo_height())  # This line of code creates a canvas for game setup controls.
        self.canvas.pack(fill="both", expand=True)  # This line of code expands the canvas to fill the window.

        self.background_image = tk.PhotoImage(file="Setup Screen.png")  # This line of code loads the background image for the setup screen.
        self.canvas.create_image(0, 0, image=self.background_image, anchor="nw")  # This line of code places the background image on the canvas.

        button_width = 800  # This line of code sets the button width.
        button_height = 400  # This line of code sets the button height.

        # This block of code creates the addition game mode button.
        self.addition_button = tk.Button(self.root, image=self.addition_image, width=button_width, height=button_height,
                                         command=lambda: self.start_game("Addition"))
        self.addition_button_window = self.canvas.create_window(100, 100, window=self.addition_button, anchor="nw")
        self.addition_button.bind("<Enter>", self.on_enter)  # This line of code binds the on_enter method to the button hover event.
        self.addition_button.bind("<Leave>", self.on_leave)  # This line of code binds the on_leave method to the button hover leave event.

        # This block of code creates the subtraction game mode button.
        self.subtraction_button = tk.Button(self.root, image=self.subtraction_image, width=button_width, height=button_height,
                                            command=lambda: self.start_game("Subtraction"))
        self.subtraction_button_window = self.canvas.create_window(1000, 100, window=self.subtraction_button, anchor="nw")
        self.subtraction_button.bind("<Enter>", self.on_enter)  # This line of code binds the on_enter method to the button hover event.
        self.subtraction_button.bind("<Leave>", self.on_leave)  # This line of code binds the on_leave method to the button hover leave event.

        # This block of code creates the multiplication game mode button.
        self.multiplication_button = tk.Button(self.root, image=self.multiplication_image, width=button_width, height=button_height,
                                               command=lambda: self.start_game("Multiplication"))
        self.multiplication_button_window = self.canvas.create_window(100, 550, window=self.multiplication_button, anchor="nw")
        self.multiplication_button.bind("<Enter>", self.on_enter)  # This line of code binds the on_enter method to the button hover event.
        self.multiplication_button.bind("<Leave>", self.on_leave)  # This line of code binds the on_leave method to the button hover leave event.

        # This block of code creates the division game mode button.
        self.division_button = tk.Button(self.root, image=self.division_image, width=button_width, height=button_height,
                                         command=lambda: self.start_game("Division"))
        self.division_button_window = self.canvas.create_window(1000, 550, window=self.division_button, anchor="nw")
        self.division_button.bind("<Enter>", self.on_enter)  # This line of code binds the on_enter method to the button hover event.
        self.division_button.bind("<Leave>", self.on_leave)  # This line of code binds the on_leave method to the button hover leave event.

    def start_game(self, mode):

        """Starts creating the maze for the game."""
        self.mode = mode  # This line of code sets the selected game mode.

        for widget in self.root.winfo_children():  # This line of code clears existing widgets from the window.
            widget.pack_forget()

        self.initialize_maze()  # This line of code calls the initialize_maze method to initialize the maze for the selected mode.

        self.player_pos = [1, 1]  # This line of code sets the initial player position.

        # This block of code creates a canvas for the maze.
        self.canvas = tk.Canvas(self.root, width=self.COLS * self.CELL_SIZE, height=self.ROWS * self.CELL_SIZE, bg='white')
        self.canvas.pack(pady=20)

        self.timer_label.place(x=1600, y=1000)  # This line of code places the timer label on the window.

        self.feedback_label.pack(pady=10)  # This line of code packs the feedback label.

        self.draw_maze()  # This line of code calls the draw_maze method to draw the maze on the canvas.
        self.draw_player()  # This line of code calls the draw_player method to draw the player in the initial position.

        self.timer_running = True  # This line of code sets the timer_running attribute to True to start the timer.
        self.time_elapsed = 0  # This line of code resets the time_elapsed attribute to zero.
        self.correct_answers = 0  # This line of code resets the correct_answers counter to zero.
        self.incorrect_answers = 0  # This line of code resets the incorrect_answers counter to zero.
        self.update_timer()  # This line of code calls the update_timer method to start the timer update loop.

        self.bind_keys()  # This line of code calls the bind_keys method to bind keys for player movement.

    def bind_keys(self):

        """ Binds all the keys for the wizard movement."""
        self.root.bind("<Left>", lambda event: self.move_player(-1, 0))  # This line of code binds the left arrow key to move the player left.
        self.root.bind("<Right>", lambda event: self.move_player(1, 0))  # This line of code binds the right arrow key to move the player right.
        self.root.bind("<Up>", lambda event: self.move_player(0, -1))  # This line of code binds the up arrow key to move the player up.
        self.root.bind("<Down>", lambda event: self.move_player(0, 1))  # This line of code binds the down arrow key to move the player down.

    def unbind_keys(self):

        """Unbinds all the keys for wizard movement"""
        self.root.unbind("<Left>")  # This line of code unbinds the left arrow key.
        self.root.unbind("<Right>")  # This line of code unbinds the right arrow key.
        self.root.unbind("<Up>")  # This line of code unbinds the up arrow key.
        self.root.unbind("<Down>")  # This line of code unbinds the down arrow key.

    def initialize_maze(self): # This line of code is the function for the preset of the maze 

        """Preset for all the mazes."""

        mazes = {
            "Addition": [ # The rows of numbers below this are the preset maze for the Addition game mode
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
            ]

            }

        self.maze = mazes[self.mode]  # This line of code sets the maze layout based on the selected game mode.

    def update_timer(self):

        """Updates the Timer."""

        if self.timer_running:  # This line of code checks if the timer is running.
            self.time_elapsed += 1  # This line of code increments the time_elapsed attribute by 1 second.
            self.timer_label.config(text=f"Time: {self.time_elapsed}s")  # This line of code updates the timer label with the new time.
            self.root.after(1000, self.update_timer)  # This line of code schedules the update_timer method to be called after 1 second.

    def resize_image(self, image, width, height):

        """Resizes the image to fit."""

        return image.subsample(int(image.width() // width), int(image.height() // height))  # This line of code resizes an image to the specified width and height.

    def draw_maze(self):

        """Draws the preset for the maze """
        self.canvas.delete("all")  # This line of code clears the canvas.
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.maze_background_image)  # This line of code draws the background image on the canvas.

        # This block of code loops through each cell in the maze and draws the appropriate image.
        for row in range(self.ROWS):  # This line of code loops through each row of the maze.
            for col in range(self.COLS):  # This line of code loops through each column of the maze.
                cell_value = self.maze[row][col]  # This line of code gets the value of the current cell.
                x = col * self.CELL_SIZE  # This line of code calculates the x-coordinate for drawing.
                y = row * self.CELL_SIZE  # This line of code calculates the y-coordinate for drawing.

                self.canvas.create_image(x, y, anchor=tk.NW, image=self.empty_space_image)  # This line of code draws the empty space image by default.

                if cell_value == 1:
                    self.canvas.create_image(x, y, anchor=tk.NW, image=self.wall_image)  # This line of code draws the wall image if the cell value is 1.
                elif cell_value == 3:
                    self.canvas.create_image(x, y, anchor=tk.NW, image=self.green_box_image)  # This line of code draws the green box image if the cell value is 3.
                elif cell_value == 4:
                    self.canvas.create_image(x, y, anchor=tk.NW, image=self.exit_image)  # This line of code draws the exit image if the cell value is 4.

                if cell_value == 2:
                    self.canvas.create_image(x, y, anchor=tk.NW, image=self.red_box_image)  # This line of code draws the red box image if the cell value is 2.
                    self.red_boxes.add((row, col))  # This line of code adds the position to the red_boxes set.

    def draw_player(self):

        """Draws the wizard for the game."""

        x = self.player_pos[1] * self.CELL_SIZE  # This line of code calculates the x-coordinate for the player's position.
        y = self.player_pos[0] * self.CELL_SIZE  # This line of code calculates the y-coordinate for the player's position.
        self.canvas.create_image(x, y, anchor=tk.NW, image=self.player_image)  # This line of code draws the player image at the calculated position.

    def move_player(self, dx, dy):

        """Controls to move the wizard."""

        new_row = self.player_pos[0] + dy  # This line of code calculates the new row position for the player.
        new_col = self.player_pos[1] + dx  # This line of code calculates the new column position for the player.

        # This block of code checks if the new position is within the maze bounds and if movement is allowed.
        if 0 <= new_row < self.ROWS and 0 <= new_col < self.COLS:  # This line of code checks if the new position is within the maze bounds.
            cell_value = self.maze[new_row][new_col]  # This line of code gets the value of the new cell.

            # This block of code blocks movement if it's a wall or if it's the exit when there are still red boxes.
            if cell_value == 1:
                return  # This line of code blocks movement if it's a wall.
            elif cell_value == 4:
                if len(self.red_boxes) > 0:
                    self.feedback_label.config(text="Not all goblins have been defeated yet.")  # This line of code shows a message if not all goblins are defeated.
                    return  # This line of code blocks movement if not all goblins are defeated.

            # This block of code allows movement over empty spaces (0), green boxes (3), and exit (4 if no goblins left).
            self.player_pos = [new_row, new_col]  # This line of code updates the player position.
            self.draw_maze()  # This line of code redraws the maze.
            self.draw_player()  # This line of code redraws the player.
            self.check_for_events()  # This line of code calls the check_for_events method to check for events at the new position.

    def check_for_events(self):

        """Checks for character interactions with the maze."""

        current_pos = tuple(self.player_pos)  # This line of code gets the current player position as a tuple.
        if current_pos in self.red_boxes:  # This line of code checks if the player is on a red box.
            self.display_math_question()  # This line of code calls the display_math_question method to display a math question.

        elif self.maze[self.player_pos[0]][self.player_pos[1]] == 4:
            if len(self.red_boxes) == 0:  # This line of code checks if the player reached the exit and all goblins are defeated.
                self.show_win_message()  # This line of code calls the show_win_message method to show the win message.
            else:
                self.feedback_label.config(text="Not all goblins have been defeated yet.")  # This line of code shows a message if not all goblins are defeated.

    def display_math_question(self):

        """Displays the maths question in a new window."""

        if not self.math_question_active:  # This line of code checks if a math question is not already active.
            self.math_question_active = True  # This line of code sets the math_question_active attribute to True.
            self.unbind_keys()  # This line of code calls the unbind_keys method to unbind movement keys.

            # This block of code creates the question window.
            self.question_window = tk.Toplevel(self.root)  # This line of code creates a new window for the question.
            self.question_window.title("Math Question")  # This line of code sets the window title.
            self.question_window.geometry("800x700")  # This line of code sets a fixed size for the question window.
            self.question_window.configure(bg="#1D0200")  # This line of code sets the background color.

            # This line of code centers the question window on the screen.
            self.center_window(self.question_window, 800, 700)

            self.question_window.attributes("-toolwindow", 1)  # This line of code sets window attributes to remove maximize and minimize buttons.
            self.question_window.protocol("WM_DELETE_WINDOW", lambda: None)  # This line of code disables the window close button.

            question, self.correct_answer = self.generate_question()  # This line of code calls the generate_question method to generate a math question.
            # This line of code creates a label for the question in the question window.
            self.question_label = tk.Label(self.question_window, text=question, font=("Times New Roman", 18), bg="#1D0200", fg="white")
            self.question_label.pack(pady=10)  # This line of code packs the question label.

            self.answer_buttons = []  # This line of code initializes a list to store answer buttons.
            answers = self.generate_answers(self.correct_answer)  # This line of code calls the generate_answers method to generate answer options.

            for i, answer in enumerate(answers):  # This block of code creates buttons for each answer option.
                button = tk.Button(self.question_window, text=answer, 
                                command=lambda a=answer: self.check_answer(a), 
                                height=2, width=15, 
                                font=("Times New Roman", 16),
                                bg="#BB9351", fg="white",
                                relief="raised", bd=3)
                button.pack(pady=10)  # This line of code packs the button.
                self.answer_buttons.append(button)  # This line of code adds the button to the answer_buttons list.

            # This block of code binds number keys to answer selection.
            self.root.bind("1", lambda event: self.check_answer(answers[0]))
            self.root.bind("2", lambda event: self.check_answer(answers[1]))
            self.root.bind("3", lambda event: self.check_answer(answers[2]))
            self.root.bind("4", lambda event: self.check_answer(answers[3]))

    def center_window(self, window, width, height):

        """Centres the window where the question is being displayed"""

        # This block of code centers the window on the screen.
        screen_width = window.winfo_screenwidth()  # This line of code gets the screen width.
        screen_height = window.winfo_screenheight()  # This line of code gets the screen height.

        # This block of code calculates the position x and y to center the window.
        position_x = (screen_width // 2) - (width // 2)  # This line of code calculates the x-coordinate.
        position_y = (screen_height // 2) - (height // 2)  # This line of code calculates the y-coordinate.

        # This line of code sets the position of the window.
        window.geometry(f'{width}x{height}+{position_x}+{position_y}')

    def generate_question(self):

        """Generates the questions for the user to answer."""

        if self.mode == "Addition":  # This line of code checks if the game mode is addition.
            a, b = random.randint(1, 10), random.randint(1, 10)  # This line of code generates two random numbers.
            return f"{a} + {b} =", a + b  # This line of code returns the addition question and answer.
        elif self.mode == "Subtraction":  # This line of code checks if the game mode is subtraction.
            a, b = random.randint(1, 10), random.randint(1, 10)  # This line of code generates two random numbers.
            return f"{a} - {b} =", a - b  # This line of code returns the subtraction question and answer.
        elif self.mode == "Multiplication":  # This line of code checks if the game mode is multiplication.
            a, b = random.randint(1, 10), random.randint(1, 10)  # This line of code generates two random numbers.
            return f"{a} x {b} =", a * b  # This line of code returns the multiplication question and answer.
        elif self.mode == "Division":  # This line of code checks if the game mode is division.
            b = random.randint(1, 10)  # This line of code generates a random number for the divisor.
            a = b * random.randint(1, 10)  # This line of code generates a random number for the dividend.
            return f"{a} ÷ {b} =", a // b  # This line of code returns the division question and answer.
        else:
            return "Error", 0  # This line of code returns an error if the mode is not recognized.

    def generate_answers(self, correct_answer):

        """Generates the answer to display on the buttons."""

        answers = [correct_answer]  # This line of code starts with the correct answer in the list.
        while len(answers) < 4:  # This line of code generates three more wrong answers.
            wrong_answer = random.randint(1, 20)  # This line of code generates a random wrong answer.
            if wrong_answer != correct_answer:  # This line of code ensures the wrong answer is not the same as the correct answer.
                answers.append(wrong_answer)  # This line of code adds the wrong answer to the list.
        random.shuffle(answers)  # This line of code shuffles the list of answers.
        return answers  # This line of code returns the shuffled list of answers.

    def check_answer(self, user_answer):

        """Checks the user interaction with the answer."""

        if user_answer == self.correct_answer:  # This line of code checks if the user's answer is correct.
            self.feedback_label.config(text="Correct!")  # This line of code updates the feedback label to show "Correct!".
            self.correct_answers += 1  # This line of code increments the correct_answers counter by 1.

            current_pos = tuple(self.player_pos)  # This line of code gets the current player position as a tuple.
            if current_pos in self.red_boxes:  # This line of code checks if the current position is a red box.
                self.red_boxes.remove(current_pos)  # This line of code removes the red box from the set.
                self.solved_boxes.add(current_pos)  # This line of code adds the position to the solved_boxes set.
                self.maze[self.player_pos[0]][self.player_pos[1]] = 3  # This line of code updates the maze structure to a green box.

                # This block of code redraws the maze and player immediately after the answer is correct.
                self.draw_maze()  # This line of code redraws the maze.
                self.draw_player()  # This line of code redraws the player.

        else:
            self.feedback_label.config(text="Incorrect!")  # This line of code updates the feedback label to show "Incorrect!".
            self.incorrect_answers += 1  # This line of code increments the incorrect_answers counter by 1.
            self.time_elapsed += 1  # This line of code penalizes the player by increasing the time_elapsed by 1 second.
            self.timer_label.config(text=f"Time: {self.time_elapsed}s")  # This line of code updates the timer label with the penalty time.

        self.question_window.destroy()  # This line of code closes the question window.
        self.math_question_active = False  # This line of code sets the math_question_active attribute to False.
        self.bind_keys()  # This line of code calls the bind_keys method to re-bind keys for movement.

        # This block of code unbinds the number keys used for answering the question.
        self.root.unbind("1")
        self.root.unbind("2")
        self.root.unbind("3")
        self.root.unbind("4")

        self.check_for_events()  # This line of code calls the check_for_events method to check for events at the current position.

    def show_win_message(self):

        """Displays the window when maze is completed."""

        self.timer_running = False  # This line of code stops the timer by setting timer_running to False.
        self.update_best_time()  # This line of code calls the update_best_time method to update the best time for the user.
        self.save_user_data()  # This line of code calls the save_user_data method to save user data to the file.

        # This block of code creates a new window for the win message.
        win_window = tk.Toplevel(self.root)  # This line of code creates a new top-level window for the win message.
        win_window.title("Congratulations!")  # This line of code sets the window title.
        win_window.geometry("400x300")  # This line of code sets the window size.
        win_window.configure(bg="#1D0200")  # This line of code sets the background color.

        # This line of code creates a label to display the win message.
        tk.Label(win_window, text=f"You've completed the level in {self.time_elapsed} seconds!\n"
                                f"Correct Answers: {self.correct_answers}, Incorrect Answers: {self.incorrect_answers}",
                font=("Times New Roman", 16), bg="#1D0200", fg="white").pack(pady=20)

        # This block of code creates buttons for returning to login, game mode selection, and replaying.
        tk.Button(win_window, text="Return to Login", font=("Times New Roman", 14), bg="#BB9351", command=lambda: [win_window.destroy(), self.return_to_login()]).pack(pady=10)
        #tk.Button(win_window, text="Return to Game Modes", font=("Times New Roman", 14), bg="#BB9351", command=lambda: [win_window.destroy(), self.show_setup_controls()]).pack(pady=10)
        tk.Button(win_window, text="Play Again", font=("Times New Roman", 14), bg="#BB9351", command=lambda: [win_window.destroy(), self.start_game(self.mode)]).pack(pady=10)

    def ask_return_to_login_or_setup(self):

        """Reroutes the user after the maze is completed."""
        # This line of code asks the user if they want to return to the login page or the setup screen.
        response = messagebox.askyesno("Return to Login?", "Do you want to return to the login page? (No will return to setup screen)")
        if response:
            self.return_to_login()  # This line of code calls the return_to_login method if the user wants to return to the login page.
        else:
            for widget in self.root.winfo_children():                
                widget.destroy()  # This line of code destroys all widgets in the window.
            self.show_setup_controls()  # This line of code calls the show_setup_controls method to show the game setup controls.

    def return_to_login(self):

        """Reroutes the user to the login page"""

        for widget in self.root.winfo_children():  # This line of code loops through all widgets in the window.
            widget.destroy()  # This line of code destroys each widget.
        self.show_login_window()  # This line of code calls the show_login_window method to display the login window.

    def update_best_time(self):

        """Updates the leaderboard if its the users best attempt."""

        mode_key = f"{self.mode}"  # This line of code gets the key for the current game mode.
        if mode_key not in self.user_data[self.username]["times"]:  # This line of code checks if there's no best time recorded for this mode.
            self.user_data[self.username]["times"][mode_key] = self.time_elapsed  # This line of code records the best time for this mode.
        else:
            self.user_data[self.username]["times"][mode_key] = min(self.user_data[self.username]["times"][mode_key], self.time_elapsed)  # This line of code updates the best time with the minimum time.

    def show_leaderboard(self):

        """Displays the leaderboard with other users attempts."""

        leaderboard_window = tk.Toplevel(self.root)  # This line of code creates a new window for the leaderboard.
        leaderboard_window.title("Leaderboard")  # This line of code sets the window title.
        leaderboard_window.geometry("600x400")  # This line of code sets the window size.

        leaderboard_canvas = tk.Canvas(leaderboard_window, width=600, height=400)  # This line of code creates a canvas for the leaderboard.
        leaderboard_canvas.pack()  # This line of code packs the canvas.
        leaderboard_canvas.configure(bg="#1D0200")  # This line of code sets the background color.

        # This line of code draws the leaderboard title.
        leaderboard_canvas.create_text(300, 20, text="Leaderboard", font=("Times New Roman", 24), fill="white")

        # This block of code draws column headers for the leaderboard.
        leaderboard_canvas.create_text(150, 60, text="Username", font=("Times New Roman", 18, "bold"), fill="white")
        leaderboard_canvas.create_text(300, 60, text="Game Mode", font=("Times New Roman", 18, "bold"), fill="white")
        leaderboard_canvas.create_text(450, 60, text="Time (s)", font=("Times New Roman", 18, "bold"), fill="white")

        # This block of code draws dividing lines between columns.
        leaderboard_canvas.create_line(225, 40, 225, 380, fill="white")
        leaderboard_canvas.create_line(375, 40, 375, 380, fill="white")

        y_position = 100  # This line of code sets the initial y-position for drawing rows.
        for username, data in self.user_data.items():  # This line of code loops through each user in user data.
            if "times" in data:  # This line of code checks if times data exists for
                for mode, time in data["times"].items(): # This line of code loops through each mode and time for the user
                    leaderboard_canvas.create_text(150, y_position, text=username, font=("Times New Roman", 16), fill= "white") # This line of code draws the username
                    leaderboard_canvas.create_text(300, y_position, text=mode, font=("Times New Roman", 16), fill= "white") # This line of code draws teh game mode
                    leaderboard_canvas.create_text(450, y_position, text=str(time), font=("Times New Roman", 16), fill= "white") # This line of code draws the time
                    y_position += 30
def main(): 

    """Main function to initialize and start the Tkinter main loop."""

    root = tk.Tk() # This line of code  creates the main Tkinter window
    game = MathGame(root) # This line of code  creates an instance of the MathGame class
    root.mainloop() # This line of code starts the Tkinter main loo

if __name__ == "__main__":
    main() # This line of code calls the main function to start the game
