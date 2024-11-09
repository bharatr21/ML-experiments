from bs4 import BeautifulSoup
import requests
from pathlib import Path
import tqdm
import os

SEMESTER_PREFIX = "4420-f23"
base_url = f"https://faculty.cc.gatech.edu/~jarulraj/courses/{SEMESTER_PREFIX}/pages/schedule.html"

response = requests.get(base_url)
soup = BeautifulSoup(response.content, "html.parser")

slides_path = Path("Slides")
code_path = Path("Code")
problem_sets_path = Path("ProblemSets")
slides_path.mkdir(exist_ok=True)
code_path.mkdir(exist_ok=True)
problem_sets_path.mkdir(exist_ok=True)

trs = soup.find_all("tr")
for tr in tqdm.tqdm(trs):
    tds = tr.find_all("td")
    if len(tds) < 3:
        continue
    topic = tds[2].text
    reading = reading if tds[-1].text.strip() == '"' else tds[-1].text
    for td in tds:
        links = td.find_all("a")
        if links:
            title = links[0].get("title")
            if title.startswith("CODE"):
                with open(code_path / "code_links.txt", "a") as f:
                    f.write(f"{title} - {topic}\n")
                    f.write(f"{'-' * 40}\n")
                    if reading.strip() != '"' and "§" in reading:
                        reading = reading.replace("§", "Chapter(s)")
                    f.write(f"Reading: {reading}\n")
                    for link in links:
                        code_link = link.get("href")
                        f.write(f"{code_link}\n")
                    f.write(f"{'-' * 40}\n")
            elif title.startswith("SLIDES"):
                link = links[0]
                slides_link = link.get("href")
                slides_name = slides_link.split("/")[-1]
                slides_response = requests.get(slides_link)
                with open(slides_path / slides_name, "wb") as f:
                    f.write(slides_response.content)
            elif title.startswith("PROBLEM SET"):
                link = links[0]
                problem_set_link = link.get("href")
                problem_set_name = problem_set_link.split("/")[-1]
                problem_set_response = requests.get(problem_set_link)
                with open(problem_sets_path / problem_set_name, "wb") as f:
                    f.write(problem_set_response.content)

# In the code file, replace multiple newlines with a single newline
with open(code_path / "code_links.txt", "r") as f:
    lines = f.readlines()
    new_lines = []
    for line in lines:
        if line.strip() != "":
            new_lines.append(line + "\n")
    with open(code_path / "code_links.txt", "w") as f:
        f.writelines(new_lines)
