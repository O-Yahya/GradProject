import customtkinter
from PIL import Image
import random
from tkinter import filedialog
from db import get_user_by_email, connect_to_db, add_user, add_project, add_report, get_project_by_id, get_report_by_id, get_projects_by_user, get_reports_by_project
from Infer import run_infer_scan, read_infer_json
import scoring

conn = connect_to_db('SecureX.db')

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

current_user = None

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

def is_valid_email(email):
    return email.endswith(".com")

def login(email_entry, password_entry, root, label):
    email = email_entry.get()
    password = password_entry.get()

    # Check if any field is empty
    if email == "" or password == "":
        label.configure(text="Please fill in all fields.")
        return

    # Validate email format
    if not is_valid_email(email):
        label.configure(text="Invalid email. Please use an email ending with .com")
        return

    # Attempt to find the user and verify password
    user = get_user_by_email(conn, email)
    if user and user.password == password:
        print("Successful login.")
        global current_user
        current_user = user
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

def register(email_entry, username_entry, password_entry, root):
    email = email_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    # Check if any field is empty
    if email == "" or username == "" or password == "":
        error_label.configure(text="Please fill in all fields.")
        return

    # Validate email format
    if not is_valid_email(email):
        error_label.configure(text="Invalid email. Please use an email ending with .com")
        return

    # Attempt to add the user
    new_user = add_user(conn, username, email, password)
    if new_user:
        error_label.configure(text="Account created successfully!", text_color="green")
    else:
        error_label.configure(text="Email already associated with an account!", text_color="red")


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

    global error_label  # Define error_label globally to update it in the register function
    error_label = customtkinter.CTkLabel(master=frame, text="", text_color="red")
    error_label.pack(pady=6, padx=10)

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
        master=left_frame, text="Analyze new project", width=180, height=40, **button_style, command=analyze_project_window)
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

    new_label = customtkinter.CTkLabel(master=right_frame, text="Analyze a new project or view reports.", font=("Helvetica", 20))
    new_label.pack(pady=20, padx=10)

    root.mainloop()


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
    }
]

def get_user_scores_data():
    global current_user, scores_data
    scores_data = []  # Clear the list to avoid duplicates
    projects = get_projects_by_user(conn, current_user.user_id)
    for project in projects:
        reports = get_reports_by_project(conn, project.project_id)
        for report in reports:
            score_data = {
                "project_name": project.project_name,
                "score": report.score,
                "vulnerabilities": report.num_vulnerabilities,
                "detection_method": report.detection_method
            }
            scores_data.append(score_data)

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

    def populate_scores():
        # Clear the right_frame before populating it
        for widget in right_frame.winfo_children():
            widget.destroy()

        scores_label = customtkinter.CTkLabel(master=right_frame, text="My Scores", font=("Verdana", 24, "bold"))
        scores_label.pack(anchor="nw", padx=10, pady=20)

        get_user_scores_data()
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

            # Button to view report details
            view_report_button = customtkinter.CTkButton(master=score_frame, text="View Report", width=100, height=40, fg_color="grey",
                                                        command=lambda s=score: view_report_details(s))
            view_report_button.pack(side="right", padx=20)

    populate_scores()

    root.mainloop()


def view_report_details(score):
    # Function to display report details in a new window
    report_window = customtkinter.CTkToplevel()
    report_window.geometry("600x400")
    report_window.title("Report Details")

    frame = customtkinter.CTkFrame(master=report_window)
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Header Frame for Title
    header_frame = customtkinter.CTkFrame(master=frame)
    header_frame.pack(fill="x", pady=(0, 20))

    file_label = customtkinter.CTkLabel(master=header_frame, text=f"File: {score['project_name']} Report", font=("Verdana", 20, "bold"))
    file_label.pack(anchor="center", pady=(10, 0))

    # Content Frame for Details
    content_frame = customtkinter.CTkFrame(master=frame)
    content_frame.pack(fill="both", expand=True, pady=10)

    description_label = customtkinter.CTkLabel(master=content_frame, text="Description: Lorem ipsum dolor sit amet, consectetur adipiscing elit.", font=("Verdana", 14), wraplength=550)
    description_label.pack(anchor="w", pady=(5, 15))

    type_label = customtkinter.CTkLabel(master=content_frame, text=f"Type: {score['detection_method']}", font=("Verdana", 14))
    type_label.pack(anchor="w", pady=(5, 15))

    # Footer Frame for Close Button
    footer_frame = customtkinter.CTkFrame(master=frame)
    footer_frame.pack(fill="x", pady=(20, 10))

    def close_window():
        report_window.destroy()

    close_button = customtkinter.CTkButton(master=footer_frame, text="Close", command=close_window, width=100, height=40, corner_radius=10)
    close_button.pack(pady=(10, 0))

    report_window.grab_set()  # This makes the window modal, blocking interaction with other windows
    report_window.mainloop()







def analyze_static(path_entry, build_tool):
    path = path_entry.get()
    run_infer_scan(path, build_tool)

    vulnerabilities = read_infer_json(path)
    print(vulnerabilities[0].show())

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

    # project name label and entry
    project_name_label = customtkinter.CTkLabel(master=left_frame, text="Project Name:", font=("Verdana", 12))
    project_name_label.pack(anchor="w", padx=10, pady=(10, 2))

    project_name_entry = customtkinter.CTkEntry(master=left_frame, placeholder_text="Enter project name...", width=200)
    project_name_entry.pack(anchor="w", padx=10, pady=(0, 20))

    # File path label and entry (increased width)
    file_path_label = customtkinter.CTkLabel(master=left_frame, text="File Path:", font=("Verdana", 12))
    file_path_label.pack(anchor="w", padx=10, pady=(10, 2))

    file_path_entry = customtkinter.CTkEntry(master=left_frame, placeholder_text="Select project directory path...", width=380)  # Increased width
    file_path_entry.pack(anchor="w", padx=10, pady=(0, 20))

    # Button to open file dialog
    def select_file():
        file_path = filedialog.askdirectory()
        file_path_entry.delete(0, "end")  # Clear any existing text
        file_path_entry.insert(0, file_path)

    file_button = customtkinter.CTkButton(master=left_frame, text="Browse", command=select_file)
    file_button.pack(anchor="w", padx=10, pady=(0, 20))

    # function to show dynamic analysis options if user ticks web app checkbox
    def on_checkbox_toggle():
        if checkbox_var.get() == 1:
            web_app_url_label.pack(pady=10)
            web_app_url_entry.pack(pady=10)
            web_app_note_label.pack(pady=10)
        else:
            web_app_url_label.pack_forget()
            web_app_url_entry.pack_forget()
            web_app_note_label.pack_forget()

    # variable to store checkbox choice
    checkbox_var = customtkinter.IntVar()

    # creating checkbox, label and entry field for web app analysis
    web_app_checkbox = customtkinter.CTkCheckBox(master=left_frame, checkmark_color="green", text="Web Application", variable=checkbox_var, command=on_checkbox_toggle)
    web_app_checkbox.pack(anchor="w", padx=10, pady=10)

    web_app_url_label = customtkinter.CTkLabel(master=left_frame, text="URL: ")
    web_app_url_entry = customtkinter.CTkEntry(master=left_frame, placeholder_text="Enter web app URL...", width=280)

    web_app_note_label = customtkinter.CTkLabel(master=left_frame, text="To activate Dynamic Analysis your web application should be running at the entered URL.\n")

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

    # Initially show build tool options
    build_tool_label.pack(anchor="w", padx=10, pady=(10, 2))
    for radio in build_tool_radios:
        radio.pack(anchor="w", padx=20, pady=10)

    # Analyze button
    analyze_button = customtkinter.CTkButton(master=main_frame, text="Analyze", width=100, height=40, corner_radius=10, command=lambda: analyze_static(file_path_entry, build_tool_var, project_name_entry))
    analyze_button.pack(pady=(20, 0))

    root.mainloop()

# function to run static analysis, add project and report information to database
def analyze_static(path_entry, build_tool, name_entry):
    global current_user

    build_tool = build_tool.get()
    path = path_entry.get()
    project_name = name_entry.get()

    run_infer_scan(path, build_tool)

    created_project_id = add_project(conn, current_user.user_id, project_name, path, build_tool)
    project = get_project_by_id(conn, created_project_id)

    vulnerabilities = read_infer_json(path)
    score = scoring.calculate_security_score(vulnerabilities, scoring.bug_severity_dict)
    created_report_id = add_report(conn, project.project_id, score, len(vulnerabilities), "SAST")


    report = get_report_by_id(conn, created_report_id)
    print("Analysis completed")


#analyze_project_window()
start_page()