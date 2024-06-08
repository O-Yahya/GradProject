import subprocess
import json
import os
import re


project_path = input(print("Enter project directory path: "))
build_tool = input(print("Enter project build tool: "))


class Vulnerability:
    def __init__ (self, type, code_snippet, file, description):
        self.type = type
        self.code_snippet = code_snippet
        self.file = file
        self.description = description
    
    def show(self):
        rep = f'VULNERABILITY Type: {self.type},    Code: {self.code_snippet},  File: {self.file},  Description: {self.description}'
        print(rep + '\n')

def run_infer_scan(sourcePath, build_tool):
    if build_tool == "Maven":
        command = ["infer", "run", "--", "mvn", "clean", "install"]
    if build_tool == "CMake":
        command = ["infer", "run", "--", "make"]
    os.chdir(sourcePath)
    
    res = subprocess.run(command, capture_output=True, text=True)

    if res.returncode != 0:
        print(f"Error running Infer static analysis. Error: {res.stderr}")

def read_infer_json(sourcePath):
    path = sourcePath + "/infer-out/report.json"
    with open(path, 'r') as file:
        data = json.load(file)

    vulnerabilities = []
    for issue in data:
        type = issue.get('bug_type')
        file = issue.get('file')
        desc = issue.get('qualifier')
        vulnerabilities.append(Vulnerability(type, '', file, desc))

    return vulnerabilities

vuls = read_infer_json(project_path)

def read_infer_text(sourcePath):
    path = os.path.join(sourcePath, "infer-out/report.txt")
    with open(path, 'r') as file:
        report_content = file.read()

    print("Report content:")
    print(report_content)  # Debug: Print the contents of the report.txt file
    
    # Regular expression to capture the issues and their details
    pattern = re.compile(
        r"#(\d+)\n(.*?):(\d+): error: (.*?)\n(.*?)\n\n",
        re.DOTALL
    )
    
    matches = pattern.findall(report_content)
    print(f"Matches found: {len(matches)}")  # Debug: Print the number of matches found

    i = 0
    for match in matches:
        issue_id, file_path, line_number, issue_type, code_snippets = match
        print(f"Match: {match}")  # Debug: Print each match

        # Process the code snippets
        code_snippet_lines = re.findall(r"^\s*(\d+)\.\s+(.*?)$", code_snippets, re.MULTILINE)
        code_snippet = "\n".join(f"{line}. {snippet}" for line, snippet in code_snippet_lines)
        
        vuls[i].code_snippet = code_snippet
        i = i + 1
        # Find corresponding vulnerability in vuls list and update the code_snippet


    




# run_infer_scan(project_path, build_tool)

read_infer_text(project_path)
for vul in vuls:
    vul.show()