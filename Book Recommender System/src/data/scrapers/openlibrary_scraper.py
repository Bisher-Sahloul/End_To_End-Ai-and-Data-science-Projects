from bs4 import BeautifulSoup
import requests
import pandas as pd 
from urllib.parse import urljoin
import json
import csv 
import os 
import time
import random

HEADERS = {
    "User-Agent": "OpenLibraryResearchBot/1.0"
}
DELAY = 10 
CSV_FILE = "../../../data/raw/Openlibrary/openlibrary_books.csv"
FIELDNAMES = [
    "ISBN",
    "Book-Title",
    "Book-Author",
    "Year-Of-Publication",
    "Publisher",
    "Subject",
    "Description",
    "Image-URL-S",
    "Image-URL-M",
    "Image-URL-L"
]


def scrape_openlibrary_book(url , Subject):    
    r = requests.get(url, headers=HEADERS, timeout=15)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    body = soup.find('div' , class_ ="work-title-and-author mobile")

    # Getting ISBN
    ISBN = None
    try : 
        collection = soup.find('dd' , class_ = "object" , itemprop = "isbn" )
        ISBN = collection.text.strip()
    except : 
        pass

    # Getting Book-Title 
    Book_Title = None 
    try : 
        Book_Title = body.span.h1.text
    except:
        pass


    # Getting Author's name
    author = None
    try :
        author = body.find('h2' , class_ = "edition-byline")
        author = author.a.text
    except : 
        pass

    # Getting  Year-Of-Publication
    Year_Of_Publication = None 
    try : 
        body = soup.find('div' , class_ = "editionAbout")
        list_of_div = body.findAll('div' , class_ = None)
        Target = list_of_div[1]
        Year_Of_Publication = Target.find('span', itemprop="datePublished").text
    except  :
        pass

    # Getting The name of Publisher
    Publisher = None 
    try : 
        Publisher = Target.find('a' , itemprop="publisher").text
    except : 
        pass

    # Getting the description
    Description = None
    try  :
        Target = body.find('div' , class_ = "read-more__content markdown-content")
        Target = Target.findAll('p')
        Description = ""
        for paragraph in Target : 
            Description += paragraph.text
        Description = Description.strip()
    except : 
        pass

    image_url = soup.find('img' , itemprop="image")['src']                
    image_url = "https:" + image_url
    
    def replace_by_index(text, index, replacement):
       return text[:index] + replacement + text[index + 1:]

    Image_URL_S =  replace_by_index(image_url , -5 , 'S')
    Image_URL_M =  replace_by_index(image_url , -5 , 'M') 
    Image_URL_L =  replace_by_index(image_url , -5 , 'L')

    data = {
        "ISBN": ISBN ,
        "Book-Title": Book_Title,
        "Book-Author": author ,
        "Year-Of-Publication": Year_Of_Publication,
        "Publisher": Publisher,
        "Subject" : Subject , 
        "Description": Description,
        "Image-URL-S": Image_URL_S,
        "Image-URL-M": Image_URL_M,
        "Image-URL-L": Image_URL_L
    }    
    time.sleep(DELAY)
    return data

BASE = "https://openlibrary.org"
HEADERS = {"User-Agent": "OLCrawler/1.0"}

def get_work_urls_from_search(query, page = 1):
    url = f"{BASE}/search?q={query}&page={page}"
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, "html.parser")
    urls = set()
    for a in soup.select('a[href^="/works/OL"]'):
        urls.add(urljoin(BASE, a["href"].split("?")[0]))
    time.sleep(DELAY)
    return urls

def get_books_subject(url) : 
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, "html.parser")
    body = soup.find('div' , id = "subjectsPage")
    Subject_lists = []
    for x in  body.findAll('li') : 
        Subject_lists.append(x.text)
    time.sleep(DELAY)
    return Subject_lists


def update_csv(row_data):
    rows = {}
    # read existing data
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows[row["ISBN"]] = row

    isbn = row_data.get("ISBN")
    if not isbn:
        return

    # update or insert
    if isbn in rows:
        for field in FIELDNAMES:
            if row_data.get(field) and not rows[isbn].get(field):
                rows[isbn][field] = row_data[field]
    else:
        rows[isbn] = row_data

    # write back
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows.values())



def Get_data(url) : 
    Subjects = get_books_subject(url + "/subjects")
    for page in range(29 , 30) : 
        subset_subjects =  random.choices(Subjects , k = 10)
        for subject in subset_subjects : 
           try :
            books_url_per_page = get_work_urls_from_search(subject , page)
            for book_url in books_url_per_page : 
                update_csv(scrape_openlibrary_book(book_url , subject))
           except Exception as e:
               raise e
           
    

if __name__ == "__main__":
    # Example book page (replace with a real OL book URL)
    # example_url = "https://openlibrary.org/works/OL1108523W/A_Study_of_History?edition=key%3A/books/OL32145063M"
    # out = scrape_openlibrary_book(example_url)
    # print(json.dumps(out, indent=2, ensure_ascii=False))
    # print(get_books_subject("https://openlibrary.org/subjects"))
    # print(get_work_urls_from_search("architecture"))
    Get_data(BASE)
