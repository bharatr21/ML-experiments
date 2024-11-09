from bs4 import BeautifulSoup
import requests
from pathlib import Path
import tqdm
import os

SEMESTER_PREFIX = "4420-f24"
base_url = f"https://faculty.cc.gatech.edu/~jarulraj/courses/{SEMESTER_PREFIX}/pages/schedule.html"

response = requests.get(base_url)
soup = BeautifulSoup(response.content, "html.parser")

slides_path = Path("Slides")
code_path = Path("Code")
slides_path.mkdir(exist_ok=True)
code_path.mkdir(exist_ok=True)

trs = soup.find_all("tr")
for tr in tqdm.tqdm(trs):
    tds = tr.find_all("td")
    if len(tds) < 3:
        continue
    reading = reading if tds[-2].text.strip() == '"' else tds[-2].text
    for td in tds:
        links = td.find_all("a")
        if links:
            topic = links[0].text
            with open(code_path / "code_links.txt", "a") as f:
                if not topic.startswith("["):
                    f.write(f"{'-' * 40}\n")
                    f.write(f"{topic}\n")
                    f.write(f"{'-' * 40}\n")
                    if reading.strip() != '"' and "§" in reading:
                        reading = reading.replace("§", "Chapter(s)")
                    f.write(f"Reading: {reading}\n")
                for link in links:
                    link_url = link.get("href")
                    if link_url.endswith("pdf"):
                        slides_name = link_url.split("/")[-1]
                        slides_response = requests.get(link_url)
                        with open(slides_path / slides_name, "wb") as fs:
                            fs.write(slides_response.content)
                    elif link_url.endswith("cpp"):
                        f.write(f"{link_url}\n")
                
# In the code file, replace multiple newlines with a single newline
with open(code_path / "code_links.txt", "r") as f:
    lines = f.readlines()
    new_lines = []
    for line in lines:
        if line.strip() != "":
            new_lines.append(line + "\n")
    with open(code_path / "code_links.txt", "w") as f:
        f.writelines(new_lines)
