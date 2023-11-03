import requests
from bs4 import BeautifulSoup
import time
from collections import defaultdict

ALISA_NAME_MAPPING = {
    'Stew': "S Grant",
    'Eric Mugnier': 'E Mugnier',
    'Eric': 'E Mugnier',
    'Stewart Grant': "S Grant",
    'Anil Yelam': 'A Yelam',
    'Enze Liu': 'A Liu',
    'Alex Liu': 'A Liu',
    'Yibo Guo': 'Y Guo',
    'Yibo': 'Y Guo',
    'Zac Blanco': 'Z Blanco',
    'Zachary Blanco': 'Z Blanco',
    'Amanda Tomlinson': 'A Tomlinson',
    'Haochen Huang': 'H Huang',
    'Shu-Ting Wang': 'S Wang',
    'Rob McGuinness': 'R McGuinness',
    'Audrey Randall': 'A Randall',
    'Yudong Wu': 'Y Wu',
    'Keerthana Ganesan': 'K Ganesan',
    'Jason Zhang': 'J Zhang',
    'Jason': 'J Zhang',
    'Zesen Zhang': 'J Zhang',
    'Chengcheng Xiang': 'C Xiang',
    'Frank Wang': 'F Wang',
    'Bingyu Shen': 'B Shen',
    'Alex Yen': 'A Yen',
    'Alisha Ukani': 'A Ukani',
    'Li Zhong': 'L Zhong',
    'Edward Chen': 'E Chen',
    'Priyal Suneja': 'P Suneja',
    'Evan Laufer': 'E Laufer',
    'Tianyi Shan': 'T Shan',
    'Rukshani': 'R Athapathu',
    'Rukshani Athapathu': 'R Athapathu',
    'Allison': 'A Turner',
    'Allison Turner': 'A Turner',
    'Thomas Krenc': 'T Krenc',
    'Rajdeep Das': 'R Das',
    'Sumanth Rao': 'S Rao',
    'Hui Zhi': 'H Zhi',
    'Saarth Deshpande': "S Deshpande",
    'Ani Canumalla': 'A Canumalla',
}

# URL of the web page
URLS = [
"https://www.sysnet.ucsd.edu/classes/cse294/fa19/",
"https://www.sysnet.ucsd.edu/classes/cse294/wi20/",
"https://www.sysnet.ucsd.edu/classes/cse294/sp20/",
"https://www.sysnet.ucsd.edu/classes/cse294/fa20/",
"https://www.sysnet.ucsd.edu/classes/cse294/wi21/",
"https://www.sysnet.ucsd.edu/classes/cse294/sp21/",
"https://www.sysnet.ucsd.edu/classes/cse294/fa21/",
"https://www.sysnet.ucsd.edu/classes/cse294/wi22/",
"https://www.sysnet.ucsd.edu/classes/cse294/sp22/",
"https://www.sysnet.ucsd.edu/classes/cse294/fa22/",
"https://www.sysnet.ucsd.edu/classes/cse294/wi23/",
"https://www.sysnet.ucsd.edu/classes/cse294/sp23/",
"https://www.sysnet.ucsd.edu/classes/cse294/fa23/",
]

STUDENT_TO_ADVISOR_MAPPING = {
    "A Canumalla": ['Amy',],
    "A Liu": ['Stefan','Geoff'],
    "A Randall": ['Stefan','Geoff', 'Aaron'],
    "A Tomlinson": ['George',],
    "A Turner": ['Alex',],
    "A Ukani": ['Alex',],
    "A Yelam": ['Alex',],
    "A Yen": ['Pat',],
    "B Shen": ['YY',],
    "C Xiang": ['YY',],
    "E Chen": None,
    "E Laufer": None,
    "E Mugnier": ['YY',],
    "F Wang": None,
    "H Huang": ['YY',],
    "H Zhi": None,
    "J Zhang": ['Aaron',],
    "K Ganesan": None,
    "L Zhong": ['YY',],
    "P Suneja": None,
    "R Athapathu": ['George',],
    "R Das": ['Alex',],
    "R McGuinness": ['George',],
    "S Deshpande": ['Amy',],
    "S Grant": ['Alex',],
    "S Rao": ['Stefan','Geoff'],
    "S Wang": ['George',],
    "T Krenc": None,
    "T Shan": ['YY',],
    "Y Guo": ['George',],
    "Y Wu": ['YY',],
    "Z Blanco": ['YiYing',],
}
student_to_quarter_mapping = defaultdict(list)
total_presentation_of_a_facultys_students = defaultdict(list)

for url in URLS:
    print(url)
    # Send an HTTP GET request to the URL
    response = requests.get(url)
    time.sleep(0.5)
    current_quarter = url.split("/")[-2]

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all tables with class "papers"
        papers_tables = soup.find_all('table', class_='papers')

        # Iterate through each table with class "papers"
        for papers_table in papers_tables:
            # Find all the <tr> elements within the current table
            tr_elements = papers_table.find_all('tr')

            # Iterate through each <tr> element and enumerate the third <td>
            for tr in tr_elements:
                td_elements = tr.find_all('td')
                if len(td_elements) >= 3:
                    date_of_presentation = td_elements[0].get_text(strip=True)
                    paper_title = td_elements[1].get_text(strip=True)
                    student_name = td_elements[2].get_text(strip=True)
                    student_name = student_name.strip()
                    if len(student_name) == 0:
                        continue
                    if "job talk" in paper_title or 'A Safer Internet' in paper_title or 'Restart-Rollback' in paper_title:
                        continue
                    if student_name == 'Alex':
                        if 'Whiz' in paper_title:
                            student_name = 'Alex Liu'
                        else:
                            student_name = 'Alex Yen'
                    student_name_unique = ALISA_NAME_MAPPING[student_name]
                    student_to_quarter_mapping[student_name_unique].append(current_quarter)
                    faculty_advisors = STUDENT_TO_ADVISOR_MAPPING[student_name_unique]
                    if faculty_advisors == None:
                        continue

                    print("{}, {}".format(student_name_unique, current_quarter))
                    for f in faculty_advisors:
                        total_presentation_of_a_facultys_students[f].append((current_quarter, student_name_unique))


    else:
        print("Failed to retrieve the page. Status code:", response.status_code)

# Student Stats
student_to_quarter_mapping_sorted = sorted(student_to_quarter_mapping.items(), key=lambda item: len(item[1]), reverse = True)

max_key_length = max(len(key) for key, _ in student_to_quarter_mapping_sorted) + 1

# Print the key and length of value for each item
for key, value in student_to_quarter_mapping_sorted:
    key_padding = ' ' * (max_key_length - len(key))
    print(f'Student Name: {key}{key_padding}, Frequency: {len(value)}')

print()

# Faculty Stats:
total_presentation_of_a_facultys_students_sorted = sorted(total_presentation_of_a_facultys_students.items(), key=lambda item: len(item[1]), reverse = True)

max_key_length = max(len(key) for key, _ in total_presentation_of_a_facultys_students_sorted) + 1

# Print the key and length of value for each item
for key, value in total_presentation_of_a_facultys_students_sorted:
    key_padding = ' ' * (max_key_length - len(key))
    print(f'Faculty Name: {key}{key_padding}, Frequency: {len(value)}')