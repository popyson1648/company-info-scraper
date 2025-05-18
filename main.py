import os
from dotenv import load_dotenv

load_dotenv()

import time
import urllib.request
from html.parser import HTMLParser
from googleapiclient.discovery import build

API_KEY = os.environ.get("GOOGLE_API_KEY")
CSE_ID = os.environ.get("GOOGLE_CSE_ID")

if not API_KEY or not CSE_ID:
    print("GOOGLE_API_KEYとGOOGLE_CSE_IDを.envに設定してください。")
    exit(1)

def google_search(query, api_key=API_KEY, cse_id=CSE_ID):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=query, cx=cse_id, num=1).execute()
    if "items" in res:
        return res["items"][0]["link"]
    else:
        return None

def search_company_description(read_filename="company_list.txt", write_filename="url_list.txt"):
    with open(read_filename, "r", encoding="utf-8") as f:
        keywords = [line.strip() for line in f if line.strip()]
    results = []
    for kw in keywords:
        query = f'マイナビ {kw} "26"'
        url = google_search(query)
        if url:
            results.append(url)
        else:
            results.append("NOT FOUND")
        time.sleep(1)
    with open(write_filename, "w", encoding="utf-8") as f:
        for url in results:
            f.write(url + "\n")

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.target_a = False
        self.target_b = False
        self.a_result = ""
        self.b_result = ""
        self.stack = []
        self.path = []
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        self.stack.append((tag, attrs_dict))
        self.path.append((tag, attrs_dict))
        if (
            tag == "div"
            and attrs_dict.get("class") == "item"
            and attrs_dict.get("id") == "corpDescDtoListDescText100"
        ):
            self.target_a = True
        if tag == "div" and attrs_dict.get("class") == "heading1-inner-left":
            self.target_b = "in_div"
        if tag == "h1" and self.target_b == "in_div":
            self.target_b = "in_h1"
    def handle_endtag(self, tag):
        if self.target_a and tag == "div":
            self.target_a = False
        if self.target_b == "in_h1" and tag == "h1":
            self.target_b = "in_div"
        elif self.target_b == "in_div" and tag == "div":
            self.target_b = False
        if self.stack:
            self.stack.pop()
        if self.path:
            self.path.pop()
    def handle_data(self, data):
        if self.target_a:
            self.a_result += data.strip()
        if self.target_b == "in_h1":
            self.b_result += data.strip()
    def error(self, message):
        pass

def fetch_url(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10) as response:
        charset = response.headers.get_content_charset() or 'utf-8'
        html = response.read().decode(charset, errors='replace')
    return html

def extract_elements_from_urls(list_filename='url_list.txt', output_dir='output'):
    os.makedirs(output_dir, exist_ok=True)
    with open(list_filename, 'r', encoding='utf-8') as f:
        urls = [line.strip() for line in f if line.strip()]
    results = []
    for url in urls:
        try:
            html = fetch_url(url)
        except Exception as e:
            results.append(f"取得失敗: {url}\n{e}\n")
            continue
        parser = MyHTMLParser()
        parser.feed(html)
        a_content = parser.a_result.strip() or '抽出失敗'
        b_content = parser.b_result.strip() or '抽出失敗'
        results.append(f"{b_content}\n{a_content}")
        time.sleep(120)
    with open(os.path.join(output_dir, 'output.txt'), 'w', encoding='utf-8') as f:
        for entry in results:
            f.write(entry + "\n\n")

if __name__ == '__main__':
    search_company_description('company_list.txt', 'url_list.txt')
    extract_elements_from_urls('url_list.txt', output_dir='output')

