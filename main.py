import requests
from bs4 import BeautifulSoup

def scrape_books():
    url = "https://www.goodreads.com/shelf/show/popular"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    for book_div in soup.find_all("a", class_="elementList"):
        title_tag = book_div.find("a", class_="bookTitle")
        author_tag = book_div.find("a", class_="authorName")
        info_tag = book_div.find("span", class_="greyText smallText")

        if title_tag and author_tag:
            title = title_tag.get_text().strip()
            author = author_tag.get_text().strip()
            full_link = f"https://www.goodreads.com/{title_tag['href']}"
            avg_rating, published = None, None

            if info_tag:
                info_text = info_tag.get_text(strip=True)
                parts = [part.strip() for part in info_text.split("-")]
                for part in parts:
                    if part.startswith("avg rating"):
                        avg_rating = part.split("avg rating")[-1].strip()
                    elif part.startswith("published"):
                        published = part.split("published")[-1].strip()

books_dict = {}
author = []