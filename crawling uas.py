import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

# Fungsi untuk mendapatkan daftar artikel dari halaman kategori
def get_article_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    article_links = []
    h2 = soup.find_all("a", class_="articles--iridescent-list--text-item__title-link")
    for tag in h2:
        if 'href' in tag.attrs:
            article_links.append(tag['href'])
    return article_links

# Fungsi untuk mendapatkan kategori dan konten artikel dari URL
def get_article_content(article_url, category):
    response = requests.get(article_url)
    soup = BeautifulSoup(response.text, "html.parser")

    paragraphs = soup.find_all("div", class_="article-content-body__item-content")
    # Menggabungkan semua paragraf dan hanya mengambil huruf
    content = " ".join([re.sub(r'[^a-zA-Z\s]', '', para.get_text(separator=" ", strip=True)) for para in paragraphs])
    
    return content, category

# Daftar URL halaman kategori
urls = [
    "https://www.liputan6.com/hot",
    "https://www.liputan6.com/tekno",
    "https://www.liputan6.com/lifestyle",
    "https://www.liputan6.com/showbiz"
]

# Fungsi untuk mendapatkan kategori dari URL
def extract_category_from_url(url):
    return url.split('/')[-1]

# Mengumpulkan data dari semua artikel di semua kategori
data = []
for url in urls:
    category = extract_category_from_url(url)
    article_links = get_article_links(url)
    for link in article_links:
        try:
            content, category = get_article_content(link, category)
            data.append({"text": content, "category": category})
            # Delay untuk menghindari batasan permintaan
            time.sleep(1)
        except Exception as e:
            print(f"Error fetching content from {link}: {e}")

# Menyimpan data ke dalam file CSV
df = pd.DataFrame(data)
print(df)
df.to_csv('UAS.csv', index=False)

print("Crawling complete and saved to UAS.csv")
