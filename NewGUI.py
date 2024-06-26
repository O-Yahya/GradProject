import customtkinter
from PIL import Image
import random
from tkinter import filedialog, Scrollbar, Canvas
from db import get_user_by_email, connect_to_db, add_user, add_project, add_report, get_project_by_id, get_report_by_id, get_projects_by_user, get_reports_by_project, add_vulnerability, get_vulnerabilities_by_project
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

    # Check if any field is empty
    if email_entry.get() == "" or password_entry.get() == "":
        label.configure(text="Please fill in all fields.")
        return

    # Validate email format
    if not is_valid_email(email_entry.get()):
        label.configure(text="Invalid email. Please use an email ending with .com")
        return

    user = get_user_by_email(conn, email_entry.get())
    if user and user.password == password_entry.get():
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
    global current_user
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

    welcome_text = "Welcome " + current_user.username + "!"
    welcome_label = customtkinter.CTkLabel(master=left_frame, text=welcome_text, font=("Verdana", 18, "bold"))
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
        master=left_frame, text="My reports", width=180, height=40, **button_style, command=my_reports_window)
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


def get_user_scores_data(scores_data):
    global current_user
    projects = get_projects_by_user(conn, current_user.user_id)
    print(f"Number of projects: {len(projects)}")
    for project in projects:
        reports = get_reports_by_project(conn, project.project_id)
        for report in reports:
            score_data = {
            "project_id": project.project_id,
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

    scores_data = [
    {
        "project_id": 98,
        "project_name": "Project Alpha",
        "score": random.randint(50, 100),
        "vulnerabilities": random.randint(0, 10),
        "detection_method": "SAST"
    },
    {
        "project_id": 99,
        "project_name": "Project Beta",
        "score": random.randint(50, 100),
        "vulnerabilities": random.randint(0, 10),
        "detection_method": "DAST"
    }
]
    get_user_scores_data(scores_data)
    for score in scores_data:
        current_id = score["project_id"]
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


        view_report_button = customtkinter.CTkButton(master=score_frame, text="View Report", width=100, height=40, fg_color="grey", command=lambda: display_vulnerabilities_report(current_id))
        view_report_button.pack(side="right", padx=20)
        print(current_id)

    root.mainloop()

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

# function to run static analysis, add project, vulnerability, and report information to database
def analyze_static(path_entry, build_tool, name_entry):
    global current_user

    build_tool = build_tool.get()
    path = path_entry.get()
    project_name = name_entry.get()

    run_infer_scan(path, build_tool)

    created_project_id = add_project(conn, current_user.user_id, project_name, path, build_tool)
    project = get_project_by_id(conn, created_project_id)

    vulnerabilities = read_infer_json(path)
    for vulnerability in vulnerabilities:
        add_vulnerability(conn, created_project_id, vulnerability.type, vulnerability.file, vulnerability.description, vulnerability.bug_function, vulnerability.functions)

    score = scoring.calculate_security_score(vulnerabilities, scoring.bug_severity_dict)
    created_report_id = add_report(conn, project.project_id, score, len(vulnerabilities), "SAST")


    report = get_report_by_id(conn, created_report_id)
    print("Analysis completed")


def display_vulnerabilities_report(project_id_entry):
    project_id = project_id_entry.get()
    root = customtkinter.CTk()
    root.geometry("800x600")
    root.title("SecureX - Vulnerabilities Report")

    main_frame = customtkinter.CTkFrame(master=root)
    main_frame.pack(fill="both", expand=True)

    canvas = Canvas(main_frame, borderwidth=0, background="#2b2b2b")
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollable_frame = customtkinter.CTkFrame(master=canvas, fg_color="#2b2b2b")
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    center_frame = customtkinter.CTkFrame(master=scrollable_frame, fg_color="#2b2b2b")
    center_frame.pack(pady=20, padx=20)

    title_label = customtkinter.CTkLabel(master=center_frame, text="Project Vulnerabilities Report", font=("Verdana", 24, "bold"), fg_color="#1f1f1f")
    title_label.pack(pady=12, padx=10)

    db_vulnerabilities = get_vulnerabilities_by_project(conn, project_id)
    print(f"Report generated for project {project_id}")
    for db_vulnerability in db_vulnerabilities:
        vuln_frame = customtkinter.CTkFrame(master=center_frame, corner_radius=10, border_width=1, fg_color="#404040")
        vuln_frame.pack(pady=10, padx=10, fill="x")

        vuln_type_label = customtkinter.CTkLabel(master=vuln_frame, text=f"Type: {db_vulnerability.bug_type}", font=("Helvetica", 18, "bold"), fg_color="#333333")
        vuln_type_label.pack(anchor="w", pady=5, padx=10)

        file_label = customtkinter.CTkLabel(master=vuln_frame, text=f"File: {db_vulnerability.file}", font=("Helvetica", 16), fg_color="#333333")
        file_label.pack(anchor="w", pady=5, padx=10)

        description_label = customtkinter.CTkLabel(master=vuln_frame, text=f"Description: {db_vulnerability.description}", font=("Helvetica", 14), wraplength=700, fg_color="#333333")
        description_label.pack(anchor="w", pady=5, padx=10)

        impact_label = customtkinter.CTkLabel(master=vuln_frame, text=f"Impact on Security: HIGH", font=("Helvetica", 14), fg_color="#333333")
        impact_label.pack(anchor="w", pady=5, padx=10)

    root.mainloop()

def my_reports_window():
    global current_user
    root = customtkinter.CTk()
    root.geometry("700x500")
    root.title("SecureX - View Analysis Report")

    frame = customtkinter.CTkFrame(master=root, corner_radius=15)
    frame.pack(pady=20, padx=60, fill="both", expand=True)

    label = customtkinter.CTkLabel(master=frame, text="Projects", font=("Verdana", 26, "bold"))
    label.pack(pady=12, padx=10)

    # Fetch projects from the database
    projects = get_projects_by_user(conn, current_user.user_id)

    # Scrollable list of projects
    canvas = Canvas(frame, borderwidth=0, background="#f0f0f0")
    scrollbar = Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollable_frame = customtkinter.CTkFrame(master=canvas, fg_color="#ffffff")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    for project in projects:
        project_frame = customtkinter.CTkFrame(master=scrollable_frame, fg_color="#ffffff", corner_radius=15, border_width=2, border_color="#e0e0e0")
        project_frame.pack(pady=5, padx=10, fill="x", expand=True)

        project_label = customtkinter.CTkLabel(
            master=project_frame,
            text=f"ID: {project.project_id}    Name: {project.project_name}",
            font=("Arial", 18),
            anchor="w",
            text_color="#333333"  # Darker color for better readability
        )
        project_label.pack(anchor="w", padx=10, pady=5)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    entry_frame = customtkinter.CTkFrame(master=frame)
    entry_frame.pack(pady=20)

    entry_label = customtkinter.CTkLabel(master=entry_frame, text="Enter Project ID:", font=("Arial", 16))
    entry_label.pack(side="left", padx=10)

    entry = customtkinter.CTkEntry(master=entry_frame, placeholder_text="Project ID", width=200, font=("Arial", 16))
    entry.pack(side="left", padx=10)

    button = customtkinter.CTkButton(master=frame, text="View Analysis Report", font=("Arial", 16), command=lambda: display_vulnerabilities_report(entry))
    button.pack(pady=12, padx=10)

    root.mainloop()

start_page()
#my_reports_window()
