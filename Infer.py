import subprocess
import json
import os
import re


project_path = input(print("Enter project directory path: "))
build_tool = input(print("Enter project build tool: "))


class Vulnerability:
    def __init__ (self, type, file, description, bug_function, functions):
        self.type = type
        self.file = file
        self.description = description
        self.bug_function = bug_function
        self.functions = functions
    
    def show(self):
        rep = f'VULNERABILITY Type: {self.type},  File: {self.file},  Description: {self.description}, Bug_function: {self.bug_function}\n, Functions: {self.functions}\n'
        print(rep + '\n')

def run_infer_scan(sourcePath, build_tool):
    os.chdir(sourcePath)

    if build_tool == "Maven":
        command = ["infer", "run", "--", "mvn", "clean", "install"]
    if build_tool == "Make":
        command = ["make", "clean"]
        subprocess.run(command)
        command = ["infer", "run", "--", "make"]
    if build_tool == "C":
        file_name = input(print("Enter C file name: "))
        command = ["infer", "run", "--", "gcc", "-c", file_name]
    
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
        bug_function_start_line = issue.get('procedure_start_line')
        func_name = issue.get('procedure')

        # extracting bug_function code depending on file and function start line
        file_path = sourcePath + "/" + file
        bug_function = get_bug_function(file_path, bug_function_start_line, func_name)
        
        # extracting functions_code from bug_trace
        bug_trace = issue.get('bug_trace', [])
        bug_functions = set()

        for step in bug_trace:
            file_name = step.get('filename')
            line_number = step.get('line_number')
            print(line_number)
            function_code = get_function_code(file_name, line_number)
            bug_functions.add(function_code)

        functions_code = '\n\n'.join(bug_functions)

        vulnerabilities.append(Vulnerability(type, file, desc, bug_function, functions_code))

    

    return vulnerabilities


def read_infer_text(sourcePath):
    path = os.path.join(sourcePath, "infer-out/report.txt")
    with open(path, 'r') as file:
        report_content = file.read()

    #print("Report content:")
    #print(report_content)  # Debug: Print the contents of the report.txt file
    
    # Regular expression to capture the issues and their details
    pattern = re.compile(
        r"#(\d+)\n(.*?):(\d+): error: (.*?)\n(.*?)\n\n",
        re.DOTALL
    )
    
    matches = pattern.findall(report_content)
    #print(f"Matches found: {len(matches)}")  # Debug: Print the number of matches found

    i = 0
    for match in matches:
        issue_id, file_path, line_number, issue_type, code_snippets = match
        #print(f"Match: {match}")  # Debug: Print each match

        # Process the code snippets
        code_snippet_lines = re.findall(r"^\s*(\d+)\.\s+(.*?)$", code_snippets, re.MULTILINE)
        code_snippet = "\n".join(f"{line}. {snippet}" for line, snippet in code_snippet_lines)
        
        vuls[i].code_snippet = code_snippet
        i = i + 1


def read_bug_traces(sourcePath):
    command = ["infer", "explore", "--html"]
    path = os.path.join(sourcePath, "infer-out/report.html/traces")
    
    for filename in os.listdir(path):
        trace_path = os.path.join(path, filename)
        
        with open(trace_path, 'r') as trace_file:
            trace_content = trace_file.read()
            
def get_bug_function(file_path, start_line, function_name):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Start reading from the start line
    code_lines = lines[start_line - 1:]
    
    # Identify the function by its name and the starting line
    function_code = []
    brace_count = 0
    in_function = False

    for line in code_lines:
        # Check for the start of the function
        if not in_function:
            # Function name with start_line should be the beginning of the function
            if re.match(rf"\s*\w[\w\s\*]*\b{function_name}\s*\(", line):
                in_function = True
        
        if in_function:
            function_code.append(line)
            brace_count += line.count('{')
            brace_count -= line.count('}')

            # Check if the function has ended
            if brace_count == 0:
                break

    return ''.join(function_code)

def get_function_code(file_name, line_number):
    with open(file_name, 'r') as file:
        lines = file.readlines()

    found = False
    for i in range(line_number - 1, -1, -1):
        if re.match(r'^\s*\w[\w\s\*]*\b\w+\s*\(', lines[i]):
                function_start = i
                found = True
                break
    
    if found == False:
        return None
        
    function_code = []
    brace_count = 0
    in_function = False

    for line in lines[function_start:]:
        function_code.append(line)
        brace_count += line.count('{')
        brace_count -= line.count('}')
        if brace_count == 0:
            break

    return ''.join(function_code)


#read_bug_traces(project_path)

run_infer_scan(project_path, build_tool)
vuls = read_infer_json(project_path)
#read_infer_text(project_path)

for vul in vuls:
    vul.show()