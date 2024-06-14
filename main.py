from Infer import run_infer_scan, read_infer_json
from scoring import calculate_security_score, bug_severity_dict
import os

def main():
    project_path = input("Enter project directory path: ")
    build_tool = input("Enter project build tool: ")

    run_infer_scan(project_path, build_tool)
    vuls = read_infer_json(project_path)

    os.chdir(project_path)

    for vul in vuls:
        f = open("resultsFile.txt", "a")
        f.write(vul.show())
        print(vul.show())

    score = calculate_security_score(vuls, bug_severity_dict)
    print(f"Security Score: {score}/100")

if __name__ == "__main__":
    main()
