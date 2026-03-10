# Learning Playwright with skyward thing, which will lead to DATA EATER!!!
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time


password = ""
username = ""

class PasswordError(Exception):
    pass

class GradeManager:

    # Warning, this code is considered to be spaghetti code, please read at your own risk. 

    container = {}
    grades = {"Grades": ["Q1 P1", "Q1 P2", "Q1 P3", "Q2 P1", "Q2 P2", "Q2 P3", "Final Semester Grade"]}
    classes = []

    def __init__(self, html):
        self.html = html
        self.soup = BeautifulSoup(html, "lxml")
        self.grade_table = None
        self.class_table = None
        self.get_tables()

    def get_tables(self): # Needed Tables: idx 5 is the tabel for grades, idx 7 is the table for classes
        tables = self.soup.find_all("table")
        self.grade_table = tables[5]
        self.class_table = tables[7]

    def get_single_grade(self):
        part = self.grade_table.find("tr", class_="odd cPd vAm bZe tOA gDt3R")
        grades = part.find_all("a")
        for grade in grades:
            print(f"Grade: {grade.text}")
    
    def get_all_grades(self):
        grades = self.grade_table.find_all("tr", class_=["odd cPd vAm bZe tOA gDt3R", "even cPd vAm bZe tOA gDt3R", "cPd vAm bZe tOA gDt3R odd", "cPd vAm bZe tOA gDt3R even"])
        for grade, grade_storage in zip(grades, self.container.values()):
            grade = grade.find_all("a")
            length = len(grade)
            for i in range(7):
                if length - 1 > i:
                    grade_storage.append(grade[i].text)
                elif i == 6:
                    grade_storage.append(grade[length - 1].text)
                else:
                    grade_storage.append("NA")
        self.grades.update(self.container)

    def get_classes(self):
        classes = self.class_table.find_all("td", class_="cCl cMwS")
        old_class = "nothin lol"
        for classs in classes:
            class_thing = classs.find_all("a")[1].text
            if old_class == class_thing:
                class_thing += " Semester 2"
            else:
                old_class = class_thing
            container = {class_thing: []}
            self.container.update(container)

    def print_all_grades(self):
        print("***************************************************************************")
        for classs, grades in zip(self.grades, self.grades.values()):
            print(f"Class-{classs}:")
            for i, grade in enumerate(grades):
                print(f"    Grade #{i+1}: {grade}")
            print("***************************************************************************")


def get_password():
    with open("password.txt", "r") as f:
        info = f.read()
        if info == "Replace this text with your credentials":
            raise PasswordError("Error: Please input your credentials for Skyward to use this program")
        info = info.split("\n")
    return info[0], info[1]


def get_html(playwright):
    chromium = playwright.chromium
    browser = chromium.launch(channel="msedge", headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://aisd-tx.us001-rapididentity.com")
    page.get_by_label("Username").fill(username)
    page.get_by_role("button", name="Go").click()
    page.get_by_role("textbox", name="Password").fill(password)
    time.sleep(1)
    page.get_by_role("button", name="Go").click()
    with context.expect_page() as new_tab_info:
        page.get_by_role("button", name="Skyward Student").first.click()
    new_page = new_tab_info.value
    new_page.get_by_text("Gradebook").click()
    time.sleep(1)
    return new_page.content()

if __name__ == "__main__":
    
    username, password = get_password()
    with sync_playwright() as playwright:
        print("Getting Html...")
        html = get_html(playwright)
        print("Html Has Been Attained")
    gm = GradeManager(html)
    gm.get_single_grade()
    gm.get_classes()
    gm.get_all_grades()
    gm.print_all_grades()