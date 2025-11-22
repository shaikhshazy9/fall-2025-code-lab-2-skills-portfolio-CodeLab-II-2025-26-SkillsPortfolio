from tkinter import *
from tkinter import messagebox
import random
import os
import sys

# Change working directory to where this script is located
# This ensures the jokes file and images folder are found correctly
if getattr(sys, 'frozen', False):
    # If running as compiled exe
    script_dir = os.path.dirname(sys.executable)
else:
    # If running as Python script
    script_dir = os.path.dirname(os.path.abspath(__file__))

os.chdir(script_dir)
print(f"Working directory: {script_dir}")

# Try to import PIL for background images (To confirm)
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
    print("✓ PIL available")
except:
    PIL_AVAILABLE = False
    print("✗ PIL not available")

# Create main window
root = Tk()
root.title("🎭 Alexa Joke Assistant 🎭")
root.geometry("800x600")
root.resizable(False, False)
root.config(bg="#fef3c7")

# Store image references to prevent garbage collection
image_references = {}

# Global variables
jokes_list = []  # Will store all jokes as (setup, punchline) 
current_joke = None  # Current joke being displayed
punchline_shown = False  # Track if punchline is visible

# ============================================================================
# LOAD JOKES FROM FILE
# ============================================================================

def load_jokes():
    """
    Loads all jokes from the randomJokes.txt file.
    Each joke is on a new line with setup and punchline separated by '?'
    Stores jokes as tuples: (setup, punchline)
    """
    global jokes_list
    
    try:
        # Try to open the jokes file
        with open("randomJokes.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
            
            # Process each line
            for line in lines:
                line = line.strip()  # Remove extra spaces
                
                if line and "?" in line:
                    # Split the joke at the question mark
                    parts = line.split("?", 1)  # Split only at first '?'
                    setup = parts[0].strip() + "?"  # Add '?' back to setup
                    punchline = parts[1].strip()  # Get punchline
                    
                    # Add to jokes list
                    jokes_list.append((setup, punchline))
            
    except FileNotFoundError:
        # If file not found, show error
        messagebox.showerror("Error", "randomJokes.txt file not found!\nMake sure it's in the same folder as this program.")
    except Exception as e:
        # Any other error
        messagebox.showerror("Error", f"Error loading jokes: {e}")


# ============================================================================
# LOAD BACKGROUND IMAGES
# ============================================================================

def load_background_image(frame, image_name, fallback_color):
    """
    Loads the background image if available.
    Falls back to colored background if image not found.
    
    Parameters:
        frame: The frame to add background to
        image_name: Name of the image file in 'images' folder
        fallback_color: Color to use if image not found
    """
    if PIL_AVAILABLE:
        try:
            # Try to load background image from images folder
            image_path = f"images/{image_name}"
            print(f"Trying to load: {image_path}")
            
            img = Image.open(image_path)
            img = img.resize((800, 600))
            photo = ImageTk.PhotoImage(img)
            
            # Store reference
            image_references[image_name] = photo
            
            # Create label with background image
            bg_label = Label(frame, image=photo)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            
            print(f"✓ Loaded: {image_name}")
            return True
        except Exception as e:
            # Image not found, use colored background
            print(f"✗ Failed to load {image_name}: {e}")
            frame.config(bg=fallback_color)
            return False
    else:
        # PIL not available, use colored background
        print(f"Using color for {image_name} (PIL not available)")
        frame.config(bg=fallback_color)
        return False


# ============================================================================
# FRAME SWITCHING
# ============================================================================

def show_frame(frame):
    """
    Brings a frame to the front.
    """
    frame.tkraise()


def start_joke_app():
    """
    Switches from home screen to main joke screen.
    """
    show_frame(joke_frame)


# ============================================================================
# JOKE DISPLAY FUNCTIONS
# ============================================================================

def get_random_joke():
    """
    Selects a random joke from the jokes list.
    Displays only the setup (question part).
    """
    global current_joke, punchline_shown
    
    # Check if jokes are loaded
    if not jokes_list:
        messagebox.showwarning("No Jokes", "No jokes available!")
        return
    
    # Get a random joke
    current_joke = random.choice(jokes_list)
    punchline_shown = False
    
    # Display the setup
    setup_text = current_joke[0]
    setup_label.config(text=setup_text, fg="#1e40af")
    
    # Clear punchline
    punchline_label.config(text="")
    
    # Enable show punchline button
    punchline_button.config(state=NORMAL, bg="#f59e0b")


def show_punchline():
    """
    Displays the punchline of the current joke.
    """
    global punchline_shown
    
    # Check if there's a current joke
    if current_joke is None:
        messagebox.showinfo("No Joke", "Please click 'Alexa tell me a Joke' first!")
        return
    
    # Check if punchline already shown
    if punchline_shown:
        messagebox.showinfo("Already Shown", "Punchline is already visible!")
        return
    
    # Display the punchline
    punchline_text = current_joke[1]
    punchline_label.config(text=punchline_text, fg="#059669")
    punchline_shown = True
    
    # Disable button after showing punchline
    punchline_button.config(state=DISABLED, bg="#94a3b8")


def next_joke():
    """
    Gets a new random joke.
    Same as get_random_joke but with different name for clarity.
    """
    get_random_joke()


def quit_app():
    """
    Closes the application after confirmation.
    """
    response = messagebox.askyesno("Quit", "Are you sure you want to quit?")
    if response:
        root.quit()


def go_home():
    """
    Returns to home screen.
    """
    # Clear current joke
    global current_joke, punchline_shown
    current_joke = None
    punchline_shown = False
    setup_label.config(text="Click the button below to hear a joke!")
    punchline_label.config(text="")
    punchline_button.config(state=DISABLED, bg="#94a3b8")
    
    # Switch to home frame
    show_frame(home_frame)


# ============================================================================
# CREATE FRAMES
# ============================================================================

# Home frame (welcome screen)
home_frame = Frame(root)
home_frame.place(relwidth=1, relheight=1)

# Joke frame (main application)
joke_frame = Frame(root)
joke_frame.place(relwidth=1, relheight=1)

# ============================================================================
# HOME SCREEN DESIGN
# ============================================================================

# Create canvas first
home_canvas = Canvas(home_frame, width=800, height=600, bg="#fef3c7", highlightthickness=0)
home_canvas.pack(fill=BOTH, expand=True)

# Load home background ON THE CANVAS
if PIL_AVAILABLE:
    try:
        img = Image.open("images/home_background.jpeg")
        img = img.resize((800, 600))
        photo = ImageTk.PhotoImage(img)
        image_references['home_canvas_bg'] = photo
        home_canvas.create_image(0, 0, image=photo, anchor=NW)
        print("✓ Home background loaded on canvas")
    except Exception as e:
        print(f"✗ Home background failed: {e}")

# Main title
home_canvas.create_text(400, 150, 
                       text="Let's Laugh Together!", 
                       font=("Arial", 42, "bold"),
                       fill="#7c2d12",
                       anchor=CENTER)

# Subtitle
home_canvas.create_text(400, 210, 
                       text="🎭 Your Personal Comedy Assistant 🎭", 
                       font=("Arial", 18),
                       fill="#92400e",
                       anchor=CENTER)

# Description
home_canvas.create_text(400, 270, 
                       text="Get ready for some hilarious jokes!", 
                       font=("Arial", 15),
                       fill="#78350f",
                       anchor=CENTER)

# Big laugh emoji
home_canvas.create_text(400, 350, 
                       text="🤣", 
                       font=("Arial", 80),
                       anchor=CENTER)

# Start button on home screen
start_button = Button(
    home_frame,
    text="🚀 Start Laughing",
    font=("Arial", 18, "bold"),
    fg="white",
    bg="#f59e0b",
    activebackground="#d97706",
    width=18,
    height=2,
    borderwidth=0,
    cursor="hand2",
    command=start_joke_app
)
start_button.place(x=270, y=480)

# ============================================================================
# JOKE SCREEN DESIGN
# ============================================================================

# Load joke screen background
load_background_image(joke_frame, "joke_background.jpeg", "#f0f9ff")

# Header frame
header_frame = Frame(joke_frame, bg="#1e3a8a", height=100)
header_frame.pack(fill=X)
header_frame.pack_propagate(False)

# Title
title_label = Label(
    header_frame,
    text="🎭 Alexa Joke Assistant 🎭",
    font=("Arial", 28, "bold"),
    fg="white",
    bg="#1e3a8a"
)
title_label.pack(pady=25)

# Joke display container
joke_container = Frame(joke_frame, bg="white", relief=RAISED, bd=3)
joke_container.pack(pady=30, padx=40, fill=BOTH, expand=True)

# Joke icon
joke_icon = Label(
    joke_container,
    text="😂",
    font=("Arial", 50),
    bg="white"
)
joke_icon.pack(pady=20)

# Setup label (question part)
setup_label = Label(
    joke_container,
    text="Click the button below to hear a joke!",
    font=("Arial", 18, "bold"),
    fg="#64748b",
    bg="white",
    wraplength=700,
    justify=CENTER
)
setup_label.pack(pady=20)

# Punchline label (answer part)
punchline_label = Label(
    joke_container,
    text="",
    font=("Arial", 16, "bold"),
    fg="#059669",
    bg="white",
    wraplength=700,
    justify=CENTER
)
punchline_label.pack(pady=10)

# Buttons container
buttons_frame = Frame(joke_frame, bg="#f0f9ff")
buttons_frame.pack(pady=20)

# "Alexa tell me a Joke" button
alexa_button = Button(
    buttons_frame,
    text="🎤 Alexa tell me a Joke",
    font=("Arial", 14, "bold"),
    fg="white",
    bg="#3b82f6",
    activebackground="#2563eb",
    width=20,
    height=2,
    borderwidth=0,
    cursor="hand2",
    command=get_random_joke
)
alexa_button.grid(row=0, column=0, padx=10, pady=5)

# "Show Punchline" button
punchline_button = Button(
    buttons_frame,
    text="😆 Show Punchline",
    font=("Arial", 14, "bold"),
    fg="white",
    bg="#f59e0b",
    activebackground="#d97706",
    width=20,
    height=2,
    borderwidth=0,
    cursor="hand2",
    state=DISABLED,
    command=show_punchline
)
punchline_button.grid(row=0, column=1, padx=10, pady=5)

# "Next Joke" button
next_button = Button(
    buttons_frame,
    text="➡️ Next Joke",
    font=("Arial", 14, "bold"),
    fg="white",
    bg="#10b981",
    activebackground="#059669",
    width=20,
    height=2,
    borderwidth=0,
    cursor="hand2",
    command=next_joke
)
next_button.grid(row=1, column=0, padx=10, pady=5)

# "Home" button
home_button = Button(
    buttons_frame,
    text="🏠 Home",
    font=("Arial", 14, "bold"),
    fg="white",
    bg="#8b5cf6",
    activebackground="#7c3aed",
    width=20,
    height=2,
    borderwidth=0,
    cursor="hand2",
    command=go_home
)
home_button.grid(row=1, column=1, padx=10, pady=5)

# "Quit" button at bottom
quit_button = Button(
    joke_frame,
    text="🚪 Quit",
    font=("Arial", 12, "bold"),
    fg="white",
    bg="#ef4444",
    activebackground="#dc2626",
    width=15,
    borderwidth=0,
    cursor="hand2",
    command=quit_app
)
quit_button.pack(side=BOTTOM, pady=15)

# Footer tip
footer_label = Label(
    joke_frame,
    text="💡 Tip: Click 'Alexa tell me a Joke' to start, then 'Show Punchline' to reveal the answer!",
    font=("Arial", 10),
    fg="#64748b",
    bg="#f0f9ff"
)
footer_label.pack(side=BOTTOM, pady=5)

# ============================================================================
# INITIALIZE APPLICATION
# ============================================================================

# Load jokes when application starts
load_jokes()

# Show home frame first
show_frame(home_frame)

# Start the application
root.mainloop()