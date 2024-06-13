import tkinter as tk
from tkinter import Toplevel, Label, Entry, Button, StringVar, filedialog

class RoundedEntry(Entry):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.config(bd=2, relief="groove", font=("Calibri", 12))

class SecurityApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("500x500")
        self.root.title("Account Login")
        self.root.configure(bg="#e0e0e0")
        self.username_verify = StringVar()
        self.password_verify = StringVar()
        self.username = StringVar()
        self.password = StringVar()
        self.main_screen()

    def main_screen(self):
        Label(text="Select Your Choice", bg="#007acc", width="300", height="2", font=("Calibri", 16, "bold"), fg="white").pack()
        Label(text="", bg="#e0e0e0").pack()
        Button(text="Login", height="2", width="30", font=("Calibri", 14), fg="white", bg="#007acc", command=self.login).pack(pady=10)
        Label(text="", bg="#e0e0e0").pack()
        Button(text="Register", height="2", width="30", font=("Calibri", 14), fg="white", bg="#007acc", command=self.register).pack(pady=10)

    def register(self):
        register_screen = Toplevel(self.root)
        register_screen.title("Register")
        register_screen.geometry("500x500")
        register_screen.configure(bg="#e0e0e0")

        Label(register_screen, text="Create an Account", fg="black", font=("Calibri", 18, "bold"), bg="#e0e0e0").pack(pady=20)
        Label(register_screen, text="", bg="#e0e0e0").pack()

        Label(register_screen, text="Username * ", font=("Calibri", 14), bg="#e0e0e0").pack()
        username_entry = RoundedEntry(register_screen, textvariable=self.username)
        username_entry.pack(pady=5)

        Label(register_screen, text="Password * ", font=("Calibri", 14), bg="#e0e0e0").pack()
        password_entry = RoundedEntry(register_screen, textvariable=self.password, show='*')
        password_entry.pack(pady=5)

        Label(register_screen, text="", bg="#e0e0e0").pack()
        Button(register_screen, text="Register", width=15, height=2, fg="white", bg="#007acc", font=("Calibri", 14), command=self.register_user).pack(pady=10)

    def login(self):
        login_screen = Toplevel(self.root)
        login_screen.title("Login")
        login_screen.geometry("500x500")
        login_screen.configure(bg="#e0e0e0")

        Label(login_screen, text="Welcome Back!", fg="black", font=("Calibri", 18, "bold"), bg="#e0e0e0").pack(pady=20)
        Label(login_screen, text="", bg="#e0e0e0").pack()

        Label(login_screen, text="Username * ", font=("Calibri", 14), bg="#e0e0e0").pack()
        self.username_login_entry = RoundedEntry(login_screen, textvariable=self.username_verify)
        self.username_login_entry.pack(pady=5)

        Label(login_screen, text="Password * ", font=("Calibri", 14), bg="#e0e0e0").pack()
        self.password_login_entry = RoundedEntry(login_screen, textvariable=self.password_verify, show='*')
        self.password_login_entry.pack(pady=5)

        Label(login_screen, text="", bg="#e0e0e0").pack()
        Button(login_screen, text="Login", width=15, height=2, fg="white", bg="#007acc", font=("Calibri", 14), command=self.login_verify).pack(pady=10)

    def register_user(self):
        username_info = self.username.get()
        password_info = self.password.get()

        with open(username_info, "w") as file:
            file.write(username_info + "\n")
            file.write(password_info)

        self.username.set("")
        self.password.set("")

        Label(self.register_screen, text="Registration Success", fg="green", font=("Calibri", 11), bg="#e0e0e0").pack()

    def login_verify(self):
        username1 = self.username_verify.get()
        password1 = self.password_verify.get()
        self.username_login_entry.delete(0, 'end')
        self.password_login_entry.delete(0, 'end')

        list_of_files = os.listdir()
        if username1 in list_of_files:
            with open(username1, "r") as file:
                verify = file.read().splitlines()
                if password1 in verify:
                    self.login_success()
                else:
                    self.password_not_recognised()
        else:
            self.user_not_found()

    def login_success(self):
        login_success_screen = Toplevel(self.root)
        login_success_screen.title("Success")
        login_success_screen.geometry("150x100")
        login_success_screen.configure(bg="#e0e0e0")
        Label(login_success_screen, text="Login Success", bg="#e0e0e0").pack()
        Button(login_success_screen, text="OK", command=lambda: (self.open_security_tool(), login_success_screen.destroy())).pack()
        login_success_screen.after(20000, login_success_screen.destroy)

    def open_security_tool(self):
        self.security_tool_screen = Toplevel(self.root)
        self.security_tool_screen.title("Security Tool")
        self.security_tool_screen.geometry("500x500")
        self.security_tool_screen.configure(bg="#e0e0e0")

        Label(self.security_tool_screen, text="Welcome to our automated security tool application.\nPlease enter the URL and upload the file.", font=("Calibri", 18), bg="#e0e0e0").pack(pady=30)

        Label(self.security_tool_screen, text="", bg="#e0e0e0").pack()

        Label(self.security_tool_screen, text="Enter URL:", fg="black", font=("Calibri", 16, "bold"), bg="#e0e0e0").pack(pady=5)
        self.url_entry = RoundedEntry(self.security_tool_screen)
        self.url_entry.pack(pady=5)

        Button(self.security_tool_screen, text="Analyze URL", fg="white", bg="#007acc", font=("Calibri", 16), command=self.analyze_url).pack(pady=10)

        self.analysis_result_label = Label(self.security_tool_screen, text="", font=("Calibri", 18), bg="#e0e0e0")
        self.analysis_result_label.pack(pady=10)

        Button(self.security_tool_screen, text="Upload File", fg="white", bg="#007acc", font=("Calibri", 16), command=self.upload_file).pack(pady=10)

        Button(self.security_tool_screen, text="Done", font=("Calibri", 14), width=10, fg="white", bg="#007acc", command=self.open_score_page).pack(side="bottom", anchor="se", pady=10, padx=10)

    def analyze_url(self):
        url = self.url_entry.get()
        self.analysis_result_label.config(text=f"Analyzing URL: {url}")

    def upload_file(self):
        file_path = filedialog.askopenfilename()
        self.file_path_label.config(text=f"Selected file: {file_path}")

    def password_not_recognised(self):
        password_not_recog_screen = Toplevel(self.root)
        password_not_recog_screen.title("Invalid Password")
        password_not_recog_screen.geometry("150x100")
        password_not_recog_screen.configure(bg="#e0e0e0")
        Label(password_not_recog_screen, text="Invalid Password", bg="#e0e0e0").pack()
        Button(password_not_recog_screen, text="OK", command=password_not_recog_screen.destroy).pack()

    def user_not_found(self):
        user_not_found_screen = Toplevel(self.root)
        user_not_found_screen.title("User Not Found")
        user_not_found_screen.geometry("150x100")
        user_not_found_screen.configure(bg="#e0e0e0")
        Label(user_not_found_screen, text="User Not Found", bg="#e0e0e0").pack()
        Button(user_not_found_screen, text="OK", command=user_not_found_screen.destroy).pack()

    def open_score_page(self):
        self.security_tool_screen.destroy()
        score_screen = Toplevel(self.root)
        score_screen.title("Score")
        score_screen.geometry("500x500")
        score_screen.configure(bg="#e0e0e0")

        Label(score_screen, text="This is the Score Page", font=("Calibri", 18), bg="#e0e0e0").pack(pady=20)

        Button(score_screen, text="Back", font=("Calibri", 14), width=10, fg="white", bg="#007acc", command=lambda: (self.open_security_tool(), score_screen.destroy())).pack(side="bottom", anchor="sw", pady=10, padx=10)
        Button(score_screen, text="Done", font=("Calibri", 14), width=10, fg="white", bg="#007acc", command=self.open_report_page).pack(side="bottom", anchor="se", pady=10, padx=10)

    def open_report_page(self):
        self.score_screen.destroy()
        report_screen = Toplevel(self.root)
        report_screen.title("Report")
        report_screen.geometry("500x500")
        report_screen.configure(bg="#e0e0e0")

        Label(report_screen, text="This is the Report Page", font=("Calibri", 18), bg="#e0e0e0").pack(pady=20)

        self.file_path_label = Label(report_screen, text="", font=("Calibri", 14), bg="#e0e0e0")
        self.file_path_label.pack(pady=10)

        Button(report_screen, text="Back", font=("Calibri", 14), width=10, fg="white", bg="#007acc", command=lambda: (self.open_security_tool(), report_screen.destroy())).pack(side="bottom", anchor="sw", pady=10, padx=10)
        Button(report_screen, text="Finish", font=("Calibri", 14), width=10, fg="white", bg="#007acc", command=self.root.destroy).pack(side="bottom", anchor="se", pady=10, padx=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = SecurityApp(root)
    root.mainloop()