import requests
from bs4 import BeautifulSoup
import csv

def fetch_books(keyword):
    url = f"https://search.books.com.tw/search/query/key/{keyword}/cat/all"

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    resp = requests.get(url, headers=headers)
    resp.encoding = "utf-8"
    soup = BeautifulSoup(resp.text, "html.parser")

    books = []

    for book_block in soup.select(".table-td"):
        # 書名
        title_tag = book_block.select_one("h4 a")
        if not title_tag:
            continue
        title = title_tag.text.strip()
        link = title_tag["href"]

        # 作者
        author_tag = book_block.select_one('a[rel="go_author"]')
        author = author_tag.text.strip() if author_tag else "無資料"

        # 價格（取「元」前的數字，即第二個 <b>）
        price_ul = book_block.select_one("ul.price.clearfix")
        price = "無資料"
        if price_ul:
            b_tags = price_ul.find_all("b")
            if len(b_tags) >= 2:
                price = b_tags[1].text.strip()  # 第二個 <b> 是元前的數字

        books.append([title, author, price, link])

    return books

def save_to_csv(data, filename="booklist.csv"):
    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["書名","作者","價格","網址"])
        writer.writerows(data)

if __name__ == "__main__":
    keyword = input("請輸入搜尋關鍵字：")
    data = fetch_books(keyword)
    save_to_csv(data)
    print(f"完成！抓到 {len(data)} 筆書籍資料，已存入 booklist.csv")
