from tkinter import Tk, Toplevel, Label, Entry, Button, StringVar, filedialog
import os

class RoundedEntry(Entry):
    def _init_(self, master=None, **kwargs):
        super()._init_(master, **kwargs)
        self.config(bd=2, relief="groove", font=("Calibri", 12))

def register():
    global register_screen
    register_screen = Toplevel(main_screen)
    register_screen.title("Register")
    register_screen.geometry("500x500")
    register_screen.configure()

    global username
    global password
    global username_entry
    global password_entry
    username = StringVar()
    password = StringVar()

    Label(register_screen, text="Create an Account", fg="black", font=("Calibri", 18, "bold")).pack()
    Label(register_screen, text="").pack()
    username_label = Label(register_screen, text="Username * ")
    username_label.pack()
    username_entry = RoundedEntry(register_screen, textvariable=username)
    username_entry.pack()
    password_label = Label(register_screen, text="Password * ")
    password_label.pack()
    password_entry = RoundedEntry(register_screen, textvariable=password, show='*')
    password_entry.pack()
    Label(register_screen, text="").pack()
    Button(register_screen, text="Register", width=10, height=1, fg="#ff0000", command=register_user).pack()

def login():
    global login_screen
    login_screen = Toplevel(main_screen)
    login_screen.title("Login")
    login_screen.geometry("500x500")
    login_screen.configure()
    Label(login_screen, text="Welcome Back!", fg="black", font=("Calibri", 18, "bold")).pack()  
    Label(login_screen, text="").pack()

    global username_verify
    global password_verify
    global username1  # Make these variables global
    global password1

    username_verify = StringVar()
    password_verify = StringVar()

    global username_login_entry
    global password_login_entry

    Label(login_screen, text="Username * ").pack()
    username_login_entry = RoundedEntry(login_screen, textvariable=username_verify)
    username_login_entry.pack()
    Label(login_screen, text="").pack()
    Label(login_screen, text="Password * ").pack()
    password_login_entry = RoundedEntry(login_screen, textvariable=password_verify, show='*')
    password_login_entry.pack()
    Label(login_screen, text="").pack()
    Button(login_screen, text="Login", width=10, height=1, fg="#ff0000", command=login_verify).pack()

def register_user():
    username_info = username.get()
    password_info = password.get()

    file = open(username_info, "w")
    file.write(username_info + "\n")
    file.write(password_info)
    file.close()

    username_entry.delete(0, 'end')
    password_entry.delete(0, 'end')

    Label(register_screen, text="Registration Success", fg="green", font=("calibri", 11)).pack()

def login_verify():
    global username1
    global password1
    username1 = username_verify.get()
    password1 = password_verify.get()
    username_login_entry.delete(0, 'end')
    password_login_entry.delete(0, 'end')

    list_of_files = os.listdir()
    for file_name in list_of_files:
        if file_name == username1:
            file1 = open(username1, "r")
            verify = file1.read().splitlines()
            if password1 in verify:
                login_success()
                return
            else:
                password_not_recognised()
                return
    user_not_found()

def login_success():
    global login_success_screen
    login_success_screen = Toplevel(login_screen)
    login_success_screen.title("Success")
    login_success_screen.geometry("150x100")
    login_success_screen.configure(bg="#F0F0F0")
    Label(login_success_screen, text="Login Success").pack()
    Button(login_success_screen, text="OK", command=lambda: (open_security_tool(), login_screen.destroy())).pack()
    # Close the current login_success_screen after 20 seconds
    login_success_screen.after(20000, login_success_screen.destroy)

def open_security_tool():
    global security_tool_screen
    # Close the current login_success_screen
    login_success_screen.destroy()
    # Open the new window for security tool
    security_tool_screen = Toplevel()
    security_tool_screen.title("Security Tool")
    security_tool_screen.geometry("500x500")
    
    # Add a label with welcome message
    welcome_label = Label(security_tool_screen, text="Welcome to our automated security tool application.\nPlease enter the URL and upload the file.", font=("Calibri", 18))
    welcome_label.pack(pady=50)
    
    # Add spacing
    Label(security_tool_screen, text="").pack()
    
    # Add a label and entry widget for URL input
    Label(security_tool_screen, text="Enter URL: " ,fg="black", font=("Calibri", 16, "bold")).pack()
    global url_entry
    url_entry = RoundedEntry(security_tool_screen)
    url_entry.pack()
    
    # Add a button to initiate URL analysis
    analyze_button = Button(security_tool_screen, text="Analyze URL", fg="#336699", font=("Calibri", 16), command=analyze_url)
    analyze_button.pack()
    
    # Add a label to display analysis results
    global analysis_result_label
    analysis_result_label = Label(security_tool_screen, text="", font=("Calibri", 18))
    analysis_result_label.pack()
    
    # Add an upload button
    upload_button = Button(security_tool_screen, text="Upload File", fg="#336699", font=("Calibri", 16), command=upload_file)
    upload_button.pack(pady=20)
    
    # Add a button for "Done" on the bottom right
    done_button = Button(security_tool_screen, text="Done", font=("Calibri", 14), width=10, fg="#336699", command=open_score_page)
    done_button.pack(side="bottom", anchor="se")

def analyze_url():
    # Retrieve the URL from the entry widget
    url = url_entry.get()
    # Placeholder for analysis logic
    # For demonstration purposes, let's just display the URL in the analysis result label
    analysis_result_label.config(text=f"Analyzing URL: {url}")

def upload_file():
    file_path = filedialog.askopenfilename()
    # Display the selected file path in the label
    file_path_label.config(text=f"Selected file: {file_path}")

def password_not_recognised():
    global password_not_recog_screen
    password_not_recog_screen = Toplevel(login_screen)
    password_not_recog_screen.title("Success")
    password_not_recog_screen.geometry("150x100")
    password_not_recog_screen.configure(bg="#F0F0F0")
    Label(password_not_recog_screen, text="Invalid Password ").pack()
    Button(password_not_recog_screen, text="OK", command=delete_password_not_recognised).pack()

def user_not_found():
    global user_not_found_screen
    user_not_found_screen = Toplevel(login_screen)
    user_not_found_screen.title("Success")
    user_not_found_screen.geometry("150x100")
    user_not_found_screen.configure(bg="#F0F0F0")
    Label(user_not_found_screen, text="User Not Found").pack()
    Button(user_not_found_screen, text="OK", command=delete_user_not_found_screen).pack()

def delete_password_not_recognised():
    password_not_recog_screen.destroy()

def delete_user_not_found_screen():
    user_not_found_screen.destroy()

score_screen = None  # Define score_screen globally

def open_score_page():
    global score_screen
    # Close the current security_tool_screen
    security_tool_screen.destroy()
    # Open the new window for score page
    score_screen = Toplevel()
    score_screen.title("Score")
    score_screen.geometry("500x500")
    Label(score_screen, text="This is the Score Page", font=("Calibri", 18)).pack()
    
    # Add a button for "Back" to return to the security page on the bottom left
    back_button = Button(score_screen, text="Back", font=("Calibri", 14), width=10, fg="#336699", command=lambda: (open_security_tool(), score_screen.destroy()))
    back_button.pack(side="bottom", anchor="sw")
    
    # Add a button for "Done" on the bottom right
    done_button = Button(score_screen, text="Done", font=("Calibri", 14), width=10, fg="#336699", command=open_report_page)
    done_button.pack(side="bottom", anchor="se")

def open_report_page():
    # Close the current score_screen
    score_screen.destroy()
    # Open the new window for report page
    report_screen = Toplevel()
    report_screen.title("Report")
    report_screen.geometry("500x500")
    Label(report_screen, text="This is the Report Page", font=("Calibri", 18)).pack()
    
    # Add a label to display the selected file path
    global file_path_label
    file_path_label = Label(report_screen, text="", font=("Calibri", 14))
    file_path_label.pack()
    
    # Add a Back button to return to the security tool page and close the current page
    back_button = Button(report_screen, text="Back", font=("Calibri", 14), width=10, fg="#336699", command=lambda: (open_security_tool(), report_screen.destroy()))
    back_button.pack(side="bottom", anchor="sw")
    
    # Add a Finish button to close the application
    finish_button = Button(report_screen, text="Finish", font=("Calibri", 14), width=10, fg="#336699", command=main_screen.destroy)
    finish_button.pack(side="bottom", anchor="se")
    # You can add more widgets or functionality to the report page here.

def main_account_screen():
    global main_screen
    main_screen = Tk()
    main_screen.geometry("500x500")
    main_screen.title("Account Login")
    main_screen.configure(bg="#F0F0F0")
    
    # Calculate the center position for the window
    screen_width = main_screen.winfo_screenwidth()
    screen_height = main_screen.winfo_screenheight()
    window_width = 500
    window_height = 500
    x_coordinate = (screen_width / 2) - (window_width / 2)
    y_coordinate = (screen_height / 2) - (window_height / 2)
    main_screen.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coordinate, y_coordinate))
    
    Label(text="Select Your Choice", bg="#336699", width="300", height="2", font=("Calibri", 13), fg="white").pack()
    Label(text="").pack()
    Button(text="Login", height="2", width="30", command=login).pack()
    Label(text="").pack()
    Button(text="Register", height="2", width="30", command=register).pack()

    main_screen.mainloop()

main_account_screen()