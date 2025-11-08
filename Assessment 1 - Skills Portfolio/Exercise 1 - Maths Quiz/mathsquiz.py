from tkinter import *
from tkinter import messagebox
import random

# Create main window
root = Tk()
root.title("Maths Quiz")
root.geometry("700x500")
root.resizable(False, False)

# Global variables
current_questions = []
current_index = 0
current_score = 0
current_difficulty = ""
current_attempt = 1

def displayMenu():
    """
    Shows the difficulty level menu with three options:
    Easy, Moderate, and Advanced
    """
    # Clear the screen
    clear_screen()
    
    # Set background color
    task_frame.config(bg="#e0f2fe")
    
    # Title
    title = Label(task_frame, text="Maths Quiz", 
                  font=("Arial", 32, "bold"), 
                  bg="#e0f2fe", fg="#0c4a6e")
    title.pack(pady=40)
    
    # Subtitle
    subtitle = Label(task_frame, text="Choose Your Difficulty Level", 
                     font=("Arial", 16), 
                     bg="#e0f2fe", fg="#075985")
    subtitle.pack(pady=10)
    
    # Easy button
    easy_btn = Button(task_frame, text="1. Easy", 
                      font=("Arial", 14, "bold"),
                      bg="#86efac", fg="white", 
                      width=20, height=2,
                      command=lambda: start_quiz("Easy"))
    easy_btn.pack(pady=10)
    
    # Moderate button
    moderate_btn = Button(task_frame, text="2. Moderate", 
                          font=("Arial", 14, "bold"),
                          bg="#fbbf24", fg="white", 
                          width=20, height=2,
                          command=lambda: start_quiz("Moderate"))
    moderate_btn.pack(pady=10)
    
    # Advanced button
    advanced_btn = Button(task_frame, text="3. Advanced", 
                          font=("Arial", 14, "bold"),
                          bg="#f87171", fg="white", 
                          width=20, height=2,
                          command=lambda: start_quiz("Advanced"))
    advanced_btn.pack(pady=10)
    
    # Instructions button
    info_btn = Button(task_frame, text="Instructions", 
                      font=("Arial", 11),
                      bg="#60a5fa", fg="white", 
                      width=15,
                      command=show_instructions)
    info_btn.pack(pady=20)
    
    # Back to home button
    home_btn = Button(task_frame, text="Back to Home", 
                      font=("Arial", 10),
                      bg="#94a3b8", fg="white",
                      command=lambda: show_frame(home_frame))
    home_btn.place(x=20, y=450)


def randomInt(difficulty):
    """
    Generates two random numbers based on difficulty level.
    Easy: 1-9, Moderate: 10-99, Advanced: 1000-9999
    """
    if difficulty == "Easy":
        return random.randint(1, 9), random.randint(1, 9)
    elif difficulty == "Moderate":
        return random.randint(10, 99), random.randint(10, 99)
    else:  # Advanced
        return random.randint(1000, 9999), random.randint(1000, 9999)


def decideOperation():
    """
    Randomly chooses between addition (+) or subtraction (-)
    """
    return random.choice(['+', '-'])


def displayProblem(question, attempt):
    """
    Formats the question with attempt number
    """
    return f"Attempt {attempt}: {question} = ?"


def isCorrect(user_answer, correct_answer):
    """
    Checks if user's answer matches the correct answer
    """
    return user_answer == correct_answer


def displayResults(score):
    """
    Shows final score and rank based on performance
    """
    # Clear screen
    clear_screen()
    
    # Set background
    task_frame.config(bg="#f0fdf4")
    
    # Calculate rank
    if score >= 90:
        rank = "A+"
        message = "Outstanding!"
        color = "#059669"
    elif score >= 80:
        rank = "A"
        message = "Excellent!"
        color = "#0891b2"
    elif score >= 70:
        rank = "B"
        message = "Good job!"
        color = "#7c3aed"
    elif score >= 60:
        rank = "C"
        message = "Not bad!"
        color = "#ea580c"
    else:
        rank = "D"
        message = "Keep practicing!"
        color = "#dc2626"
    
    # Results display
    Label(task_frame, text="Quiz Completed!", 
          font=("Arial", 28, "bold"), 
          bg="#f0fdf4", fg="#065f46").pack(pady=40)
    
    Label(task_frame, text=f"Your Score: {score}/100", 
          font=("Arial", 22, "bold"), 
          bg="#f0fdf4", fg="#0369a1").pack(pady=10)
    
    Label(task_frame, text=f"Rank: {rank}", 
          font=("Arial", 24, "bold"), 
          bg="#f0fdf4", fg=color).pack(pady=10)
    
    Label(task_frame, text=message, 
          font=("Arial", 16), 
          bg="#f0fdf4", fg="#374151").pack(pady=10)
    
    # Buttons
    Button(task_frame, text="Play Again", 
           font=("Arial", 14, "bold"),
           bg="#10b981", fg="white", 
           width=15, height=2,
           command=replay_quiz).pack(pady=20)
    
    Button(task_frame, text="Exit", 
           font=("Arial", 12),
           bg="#ef4444", fg="white", 
           width=15,
           command=root.quit).pack(pady=5)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def clear_screen():
    """
    Removes all widgets from task frame
    """
    for widget in task_frame.winfo_children():
        widget.destroy()


def show_frame(frame):
    """
    Brings a frame to the front
    """
    frame.tkraise()


def replay_quiz():
    """
    Resets quiz and goes back to difficulty menu
    """
    global current_index, current_score, current_attempt
    current_index = 0
    current_score = 0
    current_attempt = 1
    displayMenu()


def show_instructions():
    """
    Shows instructions in a popup window
    """
    instructions = """
    HOW TO PLAY:
    
    1. Choose a difficulty level:
       - Easy: Single digit (1-9)
       - Moderate: Double digit (10-99)
       - Advanced: Four digit (1000-9999)
    
    2. Answer 10 math questions
    
    3. You get 2 attempts per question:
       - 1st attempt correct: +10 points
       - 2nd attempt correct: +5 points
       - Both wrong: 0 points
    
    4. Total possible score: 100 points
    
    5. Ranking:
       - 90-100: A+ (Outstanding)
       - 80-89: A (Excellent)
       - 70-79: B (Good)
       - 60-69: C (Not Bad)
       - Below 60: D (Keep Practicing)
    
    Good luck!
    """
    messagebox.showinfo("Instructions", instructions)


def confirm_exit():
    """
    Asks user if they want to exit during quiz
    """
    response = messagebox.askyesno("Exit Quiz", 
                                   f"Current Score: {current_score}/100\n\nAre you sure you want to exit?")
    if response:
        displayMenu()


def start_quiz(difficulty):
    """
    Starts the quiz with selected difficulty
    Generates 10 questions
    """
    global current_questions, current_index, current_score, current_difficulty, current_attempt
    
    # Reset variables
    current_questions = []
    current_index = 0
    current_score = 0
    current_difficulty = difficulty
    current_attempt = 1
    
    # Generate 10 questions
    for i in range(10):
        num1, num2 = randomInt(difficulty)
        operation = decideOperation()
        question = f"{num1} {operation} {num2}"
        answer = eval(question)  # Calculate correct answer
        current_questions.append((question, answer))
    
    # Show first question
    show_question()


def show_question():
    """
    Displays current question on screen
    """
    global current_attempt
    
    # Check if quiz is finished
    if current_index >= len(current_questions):
        displayResults(current_score)
        return
    
    # Clear screen
    clear_screen()
    
    # Get current question
    question, correct_answer = current_questions[current_index]
    
    # Set background color based on difficulty
    if current_difficulty == "Easy":
        task_frame.config(bg="#dcfce7")
    elif current_difficulty == "Moderate":
        task_frame.config(bg="#fef3c7")
    else:
        task_frame.config(bg="#fee2e2")
    
    # Progress bar
    progress_text = f"Question {current_index + 1}/10  |  Score: {current_score}/100"
    Label(task_frame, text=progress_text, 
          font=("Arial", 12, "bold"),
          bg="#1f2937", fg="white",
          pady=10).pack(fill=X)
    
    # Question display
    question_text = displayProblem(question, current_attempt)
    Label(task_frame, text=question_text, 
          font=("Arial", 24, "bold"),
          bg="white", fg="#1f2937",
          pady=30).pack(pady=40)
    
    # Answer entry
    Label(task_frame, text="Your Answer:", 
          font=("Arial", 14),
          bg=task_frame.cget("bg")).pack()
    
    answer_entry = Entry(task_frame, 
                        font=("Arial", 18),
                        width=20,
                        justify="center")
    answer_entry.pack(pady=10)
    answer_entry.focus()
    
    # Feedback label (initially empty)
    feedback_label = Label(task_frame, text="", 
                          font=("Arial", 13, "bold"),
                          bg=task_frame.cget("bg"))
    feedback_label.pack(pady=10)
    
    # Submit function
    def submit_answer():
        global current_index, current_score, current_attempt
        
        # Get user input
        try:
            user_answer = int(answer_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number!")
            return
        
        # Check answer
        if isCorrect(user_answer, correct_answer):
            # Correct answer
            if current_attempt == 1:
                current_score += 10
                feedback_label.config(text="Correct! +10 points", fg="#059669")
            else:
                current_score += 5
                feedback_label.config(text="Correct! +5 points", fg="#0891b2")
            
            # Move to next question after 1 second
            current_attempt = 1  # Reset attempt for next question
            current_index += 1
            root.after(1000, show_question)
        else:
            # Wrong answer
            current_attempt += 1
            
            if current_attempt <= 2:
                # Give second chance
                feedback_label.config(text="Incorrect! Try again", fg="#dc2626")
                answer_entry.delete(0, END)
                # Update question label for attempt 2
                for widget in task_frame.winfo_children():
                    if isinstance(widget, Label) and "Attempt" in widget.cget("text"):
                        widget.config(text=displayProblem(question, current_attempt))
            else:
                # No more attempts
                feedback_label.config(text=f"Wrong! Answer was {correct_answer}", fg="#dc2626")
                current_attempt = 1  # Reset for next question
                current_index += 1
                root.after(2000, show_question)
    
    # Submit button
    Button(task_frame, text="Submit Answer", 
           font=("Arial", 14, "bold"),
           bg="#3b82f6", fg="white",
           width=15, height=2,
           command=submit_answer).pack(pady=10)
    
    # Exit button
    Button(task_frame, text="Exit Quiz", 
           font=("Arial", 11),
           bg="#64748b", fg="white",
           width=12,
           command=confirm_exit).pack(pady=5)
    
    # Enter key to submit
    answer_entry.bind('<Return>', lambda event: submit_answer())


# ============================================================================
# CREATE FRAMES
# ============================================================================

# Home frame
home_frame = Frame(root, bg="#dbeafe")
home_frame.place(relwidth=1, relheight=1)

# Task frame (for quiz)
task_frame = Frame(root)
task_frame.place(relwidth=1, relheight=1)

# ============================================================================
# HOME SCREEN WITH MATH DECORATIONS
# ============================================================================

# Create canvas for math decorations
home_canvas = Canvas(home_frame, width=700, height=500, bg="#dbeafe", highlightthickness=0)
home_canvas.pack(fill=BOTH, expand=True)

# Adds floating math symbols in background
math_symbols = [
    ("+", 80, 100, 30, "#3b82f6"),
    ("-", 600, 120, 30, "#8b5cf6"),
    ("×", 120, 350, 28, "#10b981"),
    ("÷", 580, 380, 28, "#f59e0b"),
    ("=", 100, 250, 25, "#ec4899"),
    ("π", 600, 280, 32, "#06b6d4"),
    ("+", 150, 450, 24, "#a78bfa"),
    ("√", 620, 200, 26, "#14b8a6"),
    ("∑", 50, 180, 30, "#f97316"),
    ("∞", 650, 450, 28, "#84cc16"),
]

for symbol, x, y, size, color in math_symbols:
    home_canvas.create_text(x, y, text=symbol, 
                           font=("Arial", size, "bold"), 
                           fill=color, 
                           stipple="gray50")  # Makes it semi transparent

# Add math equation decorations
equations = [
    ("2+2=4", 70, 420, "#64748b"),
    ("5×3=15", 600, 50, "#64748b"),
]

for eq, x, y, color in equations:
    home_canvas.create_text(x, y, text=eq, 
                           font=("Arial", 12), 
                           fill=color,
                           stipple="gray50")

# Main title
home_canvas.create_text(350, 100, text="Maths Quiz", 
                       font=("Arial", 40, "bold"),
                       fill="#1e3a8a")

# Subtitle
home_canvas.create_text(350, 160, text="Test Your Arithmetic Skills!", 
                       font=("Arial", 16),
                       fill="#1e40af")

# Description
home_canvas.create_text(350, 195, text="Answer 10 questions and get ranked!", 
                       font=("Arial", 13),
                       fill="#475569")

# Start button on canvas
Button(home_frame, text="Start Quiz", 
       font=("Arial", 16, "bold"),
       bg="#10b981", fg="white",
       width=15, height=2,
       command=lambda: [displayMenu(), show_frame(task_frame)]).place(x=250, y=240)

# Instructions button
Button(home_frame, text="Instructions", 
       font=("Arial", 12),
       bg="#3b82f6", fg="white",
       width=12,
       command=show_instructions).place(x=290, y=330)

# ============================================================================
# START APPLICATION
# ============================================================================

show_frame(home_frame)
root.mainloop()