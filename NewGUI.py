import customtkinter
from PIL import Image
import random
from tkinter import filedialog
from db import get_user_by_email, connect_to_db, add_user

conn = connect_to_db('SecureX.db')

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")


def start_page():
    root = customtkinter.CTk()
    root.geometry("500x350")
    root.title("SecureX - Welcome")

    frame = customtkinter.CTkFrame(master=root)
    frame.pack(pady=20, padx=60, fill="both", expand=True)

    welcome_label = customtkinter.CTkLabel(master=frame, text="Welcome to SecureX", font=("Verdana", 24, "bold"))
    welcome_label.pack(pady=12, padx=10)

    login_button = customtkinter.CTkButton(master=frame, text="Login", width=180, height=40, command=lambda: login_window(root))
    login_button.pack(pady=12, padx=10)

    register_button = customtkinter.CTkButton(master=frame, text="Register", width=180, height=40, command=register_window)
    register_button.pack(pady=12, padx=10)

    root.mainloop()

def login(email_entry, password_entry, root, label):
    user = get_user_by_email(conn, email_entry.get())
    if user and user.password == password_entry.get():
        print("Successful login.")
        home_page(root)
    else:
        label.configure(text="Invalid email or password. Please try again.")


def login_window(root_start):
    root_start.destroy()

    root = customtkinter.CTk()
    root.geometry("500x350")
    root.title("SecureX - Login")

    frame = customtkinter.CTkFrame(master=root)
    frame.pack(pady=20, padx=60, fill="both", expand=True)

    label = customtkinter.CTkLabel(master=frame, text="SecureX Login", font=("Verdana", 24, "bold"))
    label.pack(pady=12, padx=10)

    entry1 = customtkinter.CTkEntry(master=frame, placeholder_text="Email")
    entry1.pack(pady=12, padx=10)

    entry2 = customtkinter.CTkEntry(master=frame, placeholder_text="Password", show="*")
    entry2.pack(pady=12, padx=10)

    error_label = customtkinter.CTkLabel(master=frame, text="", text_color="red")
    error_label.pack(pady=6, padx=10)

    button = customtkinter.CTkButton(master=frame, text="Login", command=lambda: login(entry1, entry2, root, error_label))
    button.pack(pady=12, padx=10)

    checkbox = customtkinter.CTkCheckBox(master=frame, text="Stay logged in")
    checkbox.pack(pady=12, padx=10)

    root.mainloop()

def register_window():

    root = customtkinter.CTk()
    root.geometry("500x350")
    root.title("SecureX - Register")

    frame = customtkinter.CTkFrame(master=root)
    frame.pack(pady=20, padx=60, fill="both", expand=True)

    label = customtkinter.CTkLabel(master=frame, text="Create Account", font=("Verdana", 24, "bold"))
    label.pack(pady=12, padx=10)

    entry1 = customtkinter.CTkEntry(master=frame, placeholder_text="Email")
    entry1.pack(pady=12, padx=10)

    entry2 = customtkinter.CTkEntry(master=frame, placeholder_text="Username")
    entry2.pack(pady=12, padx=10)

    entry3 = customtkinter.CTkEntry(master=frame, placeholder_text="Password", show="*")
    entry3.pack(pady=12, padx=10)

    button = customtkinter.CTkButton(master=frame, text="Register", command=lambda: register(entry1, entry2, entry3, root))
    button.pack(pady=12, padx=10)

    checkbox = customtkinter.CTkCheckBox(master=frame, text="Receive updates about new features")
    checkbox.pack(pady=12, padx=10)

    root.mainloop()

def home_page(login_root):
    login_root.destroy()

    root = customtkinter.CTk()
    root.geometry("800x600")
    root.title("SecureX - Home")

    # Main container frame
    main_frame = customtkinter.CTkFrame(master=root)
    main_frame.pack(fill="both", expand=True)

    # Left frame (options menu)
    left_frame = customtkinter.CTkFrame(master=main_frame, width=200, height=600, corner_radius=10, border_width=0, fg_color="#1c1c1c")
    left_frame.pack(side="left", fill="y", padx=(0, 2))

    welcome_label = customtkinter.CTkLabel(master=left_frame, text="Welcome!", font=("Verdana", 18, "bold"))
    welcome_label.pack(anchor="nw", pady=10, padx=10)

    # Define transparent button style
    button_style = {
        "fg_color": "transparent",  # Transparent background
        "hover_color": "grey",      # Hover color for visual feedback
        "text_color": "white",      # White text color
        "anchor": "w",              # Align text to the left
        "font": ("Helvetica", 14, "italic")     # Font settings
    }

    analyze_button = customtkinter.CTkButton(
        master=left_frame, text="Analyze new project", width=180, height=40, **button_style)
    analyze_button.pack(pady=10, padx=10)

    reports_button = customtkinter.CTkButton(
        master=left_frame, text="My reports", width=180, height=40, **button_style)
    reports_button.pack(pady=10, padx=10)

    scores_button = customtkinter.CTkButton(
        master=left_frame, text="My scores", width=180, height=40, **button_style, command=scores_page)
    scores_button.pack(pady=10, padx=10)

    profile_button = customtkinter.CTkButton(
        master=left_frame, text="Profile", width=180, height=40, **button_style)
    profile_button.pack(pady=10, padx=10)

    # Right frame (main content)
    right_frame = customtkinter.CTkFrame(master=main_frame, corner_radius=10)
    right_frame.pack(side="left", fill="both", expand=True)

    new_label = customtkinter.CTkLabel(master=right_frame, text="Recent scans", font=("Verdana", 18, "bold"))
    new_label.pack(anchor="nw", padx=10, pady=10)

    root.mainloop()

def register(email_entry, username_entry, password_entry, root):
    email = email_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    new_user = add_user(conn, username, email, password)
    if new_user:
        succes_window = customtkinter.CTkToplevel(root)
        succes_window.geometry("300x300")

        frame = customtkinter.CTkFrame(master=succes_window)
        frame.pack(fill="both", expand=True)

        label = customtkinter.CTkLabel(master=frame, text="Account created successfully!", font=("Verdana", 18))
        label.pack(padx=10, pady=10)
    else:
        failure_window = customtkinter.CTkToplevel(root)
        failure_window.geometry("300x300")

        frame = customtkinter.CTkFrame(master=failure_window)
        frame.pack(fill="both", expand=True)

        label = customtkinter.CTkLabel(master=frame, text="Email already associated with an account!", font=("Verdana", 18))
        label.pack(padx=10, pady=10)

    def close():
        succes_window.destroy()
        succes_window.update()
        root.destroy()
        root.update()

    button = customtkinter.CTkButton(master=frame, text="Ok", font=("Verdana", 18), command=close)
    button.pack(padx=10, pady=10)



scores_data = [
    {
        "project_name": "Project Alpha",
        "score": random.randint(50, 100),
        "vulnerabilities": random.randint(0, 10),
        "detection_method": "SAST"
    },
    {
        "project_name": "Project Beta",
        "score": random.randint(50, 100),
        "vulnerabilities": random.randint(0, 10),
        "detection_method": "DAST"
    },
    {
        "project_name": "Project Gamma",
        "score": random.randint(50, 100),
        "vulnerabilities": random.randint(0, 10),
        "detection_method": "Both"
    }
]

def scores_page():
    root = customtkinter.CTk()
    root.geometry("800x600")
    root.title("SecureX - My Scores")

    # Main container frame
    main_frame = customtkinter.CTkFrame(master=root)
    main_frame.pack(fill="both", expand=True)

    # Left frame (options menu)
    left_frame = customtkinter.CTkFrame(master=main_frame, width=200, height=600, corner_radius=10, border_width=0, fg_color="#1c1c1c")
    left_frame.pack(side="left", fill="y", padx=(0, 2))

    welcome_label = customtkinter.CTkLabel(master=left_frame, text="Welcome!", font=("Verdana", 18, "bold"))
    welcome_label.pack(anchor="nw", pady=10, padx=10)

    # Define transparent button style
    button_style = {
        "fg_color": "transparent",  # Transparent background
        "hover_color": "grey",      # Hover color for visual feedback
        "text_color": "white",      # White text color
        "anchor": "w",              # Align text to the left
        "font": ("Helvetica", 14, "italic")     # Font settings
    }

    analyze_button = customtkinter.CTkButton(
        master=left_frame, text="Analyze new project", width=180, height=40, **button_style)
    analyze_button.pack(pady=10, padx=10)

    reports_button = customtkinter.CTkButton(
        master=left_frame, text="My reports", width=180, height=40, **button_style)
    reports_button.pack(pady=10, padx=10)

    scores_button = customtkinter.CTkButton(
        master=left_frame, text="My scores", width=180, height=40, **button_style)
    scores_button.pack(pady=10, padx=10)

    profile_button = customtkinter.CTkButton(
        master=left_frame, text="Profile", width=180, height=40, **button_style)
    profile_button.pack(pady=10, padx=10)

    # Right frame (main content)
    right_frame = customtkinter.CTkFrame(master=main_frame, corner_radius=10)
    right_frame.pack(side="left", fill="both", expand=True)

    scores_label = customtkinter.CTkLabel(master=right_frame, text="My Scores", font=("Verdana", 24, "bold"))
    scores_label.pack(anchor="nw", padx=10, pady=20)

    def on_enter(event, frame):
        frame.configure(fg_color="#3a3a3a")

    def on_leave(event, frame):
        frame.configure(fg_color="transparent")

    for score in scores_data:
        score_frame = customtkinter.CTkFrame(master=right_frame, fg_color="transparent", border_width=2, border_color="grey", corner_radius=10)
        score_frame.pack(fill="x", padx=20, pady=20, ipady=20)

        score_frame.bind("<Enter>", lambda e, f=score_frame: on_enter(e, f))
        score_frame.bind("<Leave>", lambda e, f=score_frame: on_leave(e, f))

        project_label = customtkinter.CTkLabel(master=score_frame, text=score["project_name"], font=("Helvetica", 20, "bold"))
        project_label.pack(side="left", padx=20)

        progress_color = "green" if score["score"] > 90 else "orange" if score["score"] > 70 else "red"
        progress_bar = customtkinter.CTkProgressBar(master=score_frame, width=250, fg_color="#E0E0E0", progress_color=progress_color)
        progress_bar.set(score["score"] / 100)
        progress_bar.pack(side="left", padx=20)

        score_frame_inner = customtkinter.CTkFrame(master=score_frame, fg_color="transparent")
        score_frame_inner.pack(side="left", padx=20)

        score_label = customtkinter.CTkLabel(master=score_frame_inner, text=f"{score['score']}/100", font=("Helvetica", 18))
        score_label.pack()
        score_text_label = customtkinter.CTkLabel(master=score_frame_inner, text="Score", font=("Helvetica", 18, "bold"))
        score_text_label.pack()

        vulnerabilities_frame = customtkinter.CTkFrame(master=score_frame, fg_color="transparent")
        vulnerabilities_frame.pack(side="left", padx=20)

        vulnerabilities_value = customtkinter.CTkLabel(master=vulnerabilities_frame, text=score["vulnerabilities"], font=("Helvetica", 18))
        vulnerabilities_value.pack()
        vulnerabilities_label = customtkinter.CTkLabel(master=vulnerabilities_frame, text="Vulnerabilities", font=("Helvetica", 18, "bold"))
        vulnerabilities_label.pack()

        detection_frame = customtkinter.CTkFrame(master=score_frame, fg_color="transparent")
        detection_frame.pack(side="left", padx=20)

        detection_value = customtkinter.CTkLabel(master=detection_frame, text=score["detection_method"], font=("Helvetica", 18))
        detection_value.pack()
        detection_label = customtkinter.CTkLabel(master=detection_frame, text="Detection", font=("Helvetica", 18, "bold"))
        detection_label.pack()

        view_report_button = customtkinter.CTkButton(master=score_frame, text="View Report", width=100, height=40, fg_color="grey")
        view_report_button.pack(side="right", padx=20)

    root.mainloop()

def analyze_project_window():
    root = customtkinter.CTk()
    root.geometry("800x400")  # Increased width for better layout
    root.title("SecureX - Analyze New Project")

    # Main container frame
    main_frame = customtkinter.CTkFrame(master=root)
    main_frame.pack(fill="both", expand=True)

    # Left frame (file path selection and combo box)
    left_frame = customtkinter.CTkFrame(master=main_frame, width=400, corner_radius=10)
    left_frame.pack(side="left", fill="both", padx=20, pady=20, expand=True)

    # File path label and entry (increased width)
    file_path_label = customtkinter.CTkLabel(master=left_frame, text="File Path:", font=("Verdana", 12))
    file_path_label.pack(anchor="w", padx=10, pady=(10, 2))

    file_path_entry = customtkinter.CTkEntry(master=left_frame, placeholder_text="Select file path...", width=240)  # Increased width
    file_path_entry.pack(anchor="w", padx=10, pady=(0, 20))

    # Button to open file dialog
    def select_file():
        file_path = filedialog.askopenfilename()
        file_path_entry.delete(0, "end")  # Clear any existing text
        file_path_entry.insert(0, file_path)

    file_button = customtkinter.CTkButton(master=left_frame, text="Browse", command=select_file)
    file_button.pack(anchor="w", padx=10, pady=(0, 20))

    # Combo box for selecting project type
    project_type_label = customtkinter.CTkLabel(master=left_frame, text="Select Project Type:", font=("Verdana", 12))
    project_type_label.pack(anchor="w", padx=10, pady=(20, 2))

    project_type_var = customtkinter.StringVar()
    project_type_var.set("Project")  # Default selection

    project_type_combo = customtkinter.CTkComboBox(master=left_frame, values=["Project", "Single File"], variable=project_type_var, width=120)  # Adjusted width
    project_type_combo.pack(anchor="w", padx=10, pady=(0, 20))

    # Function to handle visibility of radio buttons based on combo box selection
    def show_radio_buttons():
        selection = project_type_var.get()
        print(selection)
        if selection == "Project":
            build_tool_label.pack(anchor="w", padx=10, pady=(10, 2))
            for radio in build_tool_radios:
                radio.pack(anchor="w", padx=20)
            language_label.pack_forget()
            for radio in language_radios:
                radio.pack_forget()
        elif selection == "Single File":
            language_label.pack(anchor="w", padx=10, pady=(10, 2))
            for radio in language_radios:
                radio.pack(anchor="w", padx=20)
            build_tool_label.pack_forget()
            for radio in build_tool_radios:
                radio.pack_forget()

    # Right frame (radio buttons for Build Tool and Language)
    right_frame = customtkinter.CTkFrame(master=main_frame, width=300, corner_radius=10)
    right_frame.pack(side="right", fill="both", padx=20, pady=20, expand=True)

    # Project build tool label and radio buttons
    build_tool_label = customtkinter.CTkLabel(master=right_frame, text="Project Build Tool:", font=("Verdana", 12))

    build_tool_var = customtkinter.StringVar()
    build_tool_var.set("Make")  # Default selection

    build_tool_options = ["Make", "CMake", "Maven", "Gradle"]

    build_tool_radios = []
    for tool in build_tool_options:
        radio = customtkinter.CTkRadioButton(master=right_frame, text=tool, variable=build_tool_var, value=tool)
        build_tool_radios.append(radio)

    # Single file language label and radio buttons
    language_label = customtkinter.CTkLabel(master=right_frame, text="Single File Language:", font=("Verdana", 12))

    language_var = customtkinter.StringVar()
    language_var.set("C/C++")  # Default selection

    language_options = ["C/C++", "Java", "Python"]

    language_radios = []
    for language in language_options:
        radio = customtkinter.CTkRadioButton(master=right_frame, text=language, variable=language_var, value=language)
        language_radios.append(radio)

    # Initially show build tool options
    build_tool_label.pack(anchor="w", padx=10, pady=(10, 2))
    for radio in build_tool_radios:
        radio.pack(anchor="w", padx=20)

    # Binding combo box selection event to show_radio_buttons function
    project_type_combo.bind("<<ComboboxSelected>>", show_radio_buttons)

    # Analyze button
    analyze_button = customtkinter.CTkButton(master=main_frame, text="Analyze", width=100, height=40, corner_radius=10)
    analyze_button.pack(pady=(20, 0))

    root.mainloop()

# Example usage
analyze_project_window()








#start_page()
