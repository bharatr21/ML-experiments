# Scrape the links from the course schedule given in this website: https://mahdi-roozbahani.github.io/CS46417641-summer2024/docs/course-info/course-schedule/

import PyPDF2
import requests
import urllib.request
from bs4 import BeautifulSoup
import tqdm

url = "https://mahdi-roozbahani.github.io/CS46417641-summer2024/docs/course-info/course-schedule/"
other_url = "https://mahdi-roozbahani.github.io/CS46417641-summer2024/other/"

response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")

links = soup.find_all("a")

# Write all the non-PDF links to a file and save that file to the Misc folder
# If the link is a pdf, then download and save the PDF to the Notes folder

import os

os.makedirs("Misc", exist_ok=True)
os.makedirs("Notes", exist_ok=True)

with open("Misc/misc.txt", "w") as f:
    for link in tqdm.tqdm(links):
        link_url = link.get("href")
        if link_url.endswith(".pdf"):
            if not link_url.startswith("http"):
                pdf_url = f"{url}{link_url}"
                try:
                    pdf_response = requests.get(pdf_url)
                    pdf_response.raise_for_status()
                except requests.exceptions.HTTPError as e:
                    if e.response.status_code == 404:
                        pdf_url = f"{other_url}{link_url}"
                        pdf_response = requests.get(pdf_url)
                        if pdf_response.status_code == 404:
                            print(f"Warning: {pdf_url} is not a valid PDF. Error: {e}")

            pdf_name = link.get("href").split("/")[-1]
            with open(f"Notes/{pdf_name}", "wb") as pdf_file:
                pdf_file.write(pdf_response.content)
                try:
                    with open(f"Notes/{pdf_name}", "rb") as pdf_file_read:
                        PyPDF2.PdfReader(pdf_file_read)
                except PyPDF2.errors.PdfReadError as e:
                    print(f"Warning: {pdf_name} is not a valid PDF. Error: {e}")
        else:
            link_url = link.get("href")
            if not link_url.startswith("https"):
                link_url = f"{url}{link_url}"
            f.write(link_url + "\n")
