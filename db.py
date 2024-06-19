import sqlite3
from Infer import Vulnerability

def connect_to_db(name):
    print("connecting to DB")
    # creates or connects to db file
    conn = sqlite3.connect('SecureX.db')
    c = conn.cursor()

    # sqlite query to create user table
    c.execute("""CREATE TABLE IF NOT EXISTS users(
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
              );""")

    c.execute("""CREATE TABLE IF NOT EXISTS projects(
                    project_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    project_name TEXT NOT NULL,
                    project_path TEXT NOT NULL,
                    build_tool TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(user_id));""")

    c.execute("""CREATE TABLE IF NOT EXISTS vulnerabilities(
                    vulnerability_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id INTEGER,
                    bug_type TEXT NOT NULL,
                    file TEXT NOT NULL,
                    description TEXT NOT NULL,
                    bug_function TEXT NOT NULL,
                    functions TEXT NOT NULL,
                    FOREIGN KEY (project_id) REFERENCES projects(project_id));""" )

    c.execute("""CREATE TABLE IF NOT EXISTS reports(
                    report_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id INTEGER,
                    score INTEGER,
                    num_vulnerabilities INTEGER,
                    detection_method TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (project_id) REFERENCES projects(project_id));""")

    print("DB created")
    return conn





class User:
    def __init__(self, user_id, username, email, password):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password

    def show(self):
        rep = f"Username: {self.username}, Email Address: {self.email}"
        return rep

class Project:
    def __init__(self, project_id, user_id, project_name, project_path, build_tool):
        self.project_id = project_id
        self.user_id = user_id
        self.project_name = project_name
        self.project_path = project_path
        self.build_tool = build_tool

class Report:
    def __init__(self, report_id, project_id, score, num_vulnerabilities, detection_method, created_at):
        self.report_id = report_id
        self.project_id = project_id
        self.score = score
        self.num_vulnerabilities = num_vulnerabilities
        self.detection_method = detection_method
        self.created_at = created_at

class DBVulnerability:
    def __init__(self, vulnerability_id, project_id, bug_type, file, description, bug_function, functions):
        self.vulnerability_id = vulnerability_id
        self.project_id = project_id
        self.bug_type = bug_type
        self.file = file
        self.description = description
        self.bug_function = bug_function
        self.functions = functions

def add_user(conn, username, email, password):
    print(f"Attempting to add user: {email}")
    # Check if the email already exists in the database
    if get_user_by_email(conn, email) is not None:
        print(f"User with email {email} already exists.")
        return None

    sql = '''INSERT INTO users(username, email, password) VALUES(?, ?, ?)'''
    cur = conn.cursor()
    cur.execute(sql, (username, email, password))
    conn.commit()
    print(f"User {email} added successfully.")
    return cur.lastrowid

def add_project(conn, user_id, project_name, project_path, build_tool):
    sql = '''INSERT INTO projects(user_id, project_name, project_path, build_tool) VALUES(?, ?, ?, ?)'''
    cur = conn.cursor()
    cur.execute(sql, (user_id, project_name, project_path, build_tool))
    conn.commit()
    return cur.lastrowid

def add_vulnerability(conn, project_id, bug_type, file, description, bug_function, functions):
    sql = '''INSERT INTO vulnerabilities(project_id, bug_type, file, description, bug_function, functions) VALUES(?, ?, ?, ?, ?, ?)'''
    cur = conn.cursor()
    cur.execute(sql, (project_id, bug_type, file, description, bug_function, functions))
    conn.commit()
    return cur.lastrowid

def add_report(conn, project_id, score, num_vulnerabilities, detection_method):
    sql = '''INSERT INTO reports(project_id, score, num_vulnerabilities, detection_method) VALUES(?, ?, ?, ?)'''
    cur = conn.cursor()
    cur.execute(sql, (project_id, score, num_vulnerabilities, detection_method))
    conn.commit()
    return cur.lastrowid

def get_projects_by_user(conn, user_id):
    sql = '''SELECT * FROM projects WHERE user_id=?'''
    cur = conn.cursor()
    cur.execute(sql, (user_id,))
    rows = cur.fetchall()
    return [Project(*row) for row in rows]

def get_vulnerabilities_by_project(conn, project_id):
    sql = '''SELECT * FROM vulnerabilities WHERE project_id=?'''
    cur = conn.cursor()
    cur.execute(sql, (project_id,))
    rows = cur.fetchall()
    return [DBVulnerability(*row) for row in rows]

def get_reports_by_project(conn, project_id):
    sql = '''SELECT * FROM reports WHERE project_id=?'''
    cur = conn.cursor()
    cur.execute(sql, (project_id,))
    rows = cur.fetchall()
    return [Report(*row) for row in rows]

def get_user_by_email(conn, email):
    sql = """SELECT * FROM users WHERE email=?"""
    cur = conn.cursor()
    cur.execute(sql, (email,))
    row = cur.fetchone()
    if row:
        return User(*row)
    return None

def get_project_by_id(conn, id):
    sql = """SELECT * FROM projects WHERE project_id=?"""
    cur = conn.cursor()
    cur.execute(sql, (id,))
    row = cur.fetchone()
    if row:
        return Project(*row)
    return None

def get_report_by_id(conn, id):
    sql = """SELECT * FROM reports WHERE report_id=?"""
    cur = conn.cursor()
    cur.execute(sql, (id,))
    row = cur.fetchone()
    if row:
        return Report(*row)
    return None