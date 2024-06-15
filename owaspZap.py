# OWASP ZAP API library
from zapv2 import ZAPv2
import subprocess
import os
import time

class DASTVulnerability:
    def __init__(self, description, risk, solution, method, url):
        self.description = description
        self.risk = risk
        self.solution = solution
        self.method = method
        self.url = url

    def show(self):
        print(f"\nVulnerability - Found by {self.method} request to {self.url}      Description: {self.description}     Risk: {self.risk}       Suggested Solution: {self.solution}")



# Info needed for using ZAP API
zap_url = "http://localhost:8081"
zap_key = "ioc86mishqumq6mf0j8qhsnalb"

# creating ZAP API instance
#zap = ZAPv2(proxies={'http': 'http://127.0.0.1:8081', 'https': 'http://127.0.0.1:8081'}, apikey=zap_key)
#zap.core.new_session("Test Session")

# function to take url of target app and analyze it using OWASP ZAP
def zap_scan():
    try:
        target_url = input("Enter url of web app to be scanned: ")

        # running spider, which scans web app for all endpoints and waiting until it is done
        scanid = zap.spider.scan(url=target_url)
        print("Spider active...")
        time.sleep(2)

        while int(zap.spider.status(scanid=scanid)) < 100:
            print("Spider progress %: " + zap.spider.status(scanid))
            time.sleep(2)

        # running analysis and waiting until done
        scanid = zap.ascan.scan(target_url)
        print("Scanning target...")

        while int(zap.ascan.status(scanid)) < 100:
            print("Scan progress %: " + zap.ascan.status(scanid))
            time.sleep(4)

        issues = zap.core.alerts(baseurl=target_url)
        print("Security issues:")
        for issue in issues:
            print(f"    Issue: {issue['name']}, Risk: {issue['risk']}, Description: {issue['description']}")

    except Exception as e:
        print("Error: ", e)

# function to retrieve security vulnerabilities found during ZAP analysis
def get_zap_alerts():
    try:
        dast_vulnerabilities = []
        target_url = input("Enter url of web app to be scanned: ")
        issues = zap.core.alerts(baseurl=target_url)
        for issue in issues:
            if issue['risk'] != "Informational":
                vul = DASTVulnerability(issue['description'], issue['risk'], issue['solution'], issue['method'], issue['url'])
                dast_vulnerabilities.append(vul)

        return dast_vulnerabilities
    except Exception as e:
        print("Error: ", e)


dast_vuls = get_zap_alerts()

#print("-------------------------------------------DAST ANALYSIS-------------------------------------------")
#for vul in dast_vuls:
    #vul.show()

#zap_scan()
