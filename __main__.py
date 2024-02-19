import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime
import hashlib
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

RSS_URL = "https://cabq.legistar.com/Feed.ashx?M=Calendar&ID=24036010&GUID=935b0b27-867f-426d-a887-d4b5f45b4036&Mode=All&Title=City+of+Albuquerque+-+Calendar+(All)"

CACHE_DIR = Path(".cache")
MINUTES_DIR = Path("minutes")


def cached_fetch(url, prefix) -> bytes:
    hashed = hashlib.sha256(url.encode()).hexdigest()[0:10]
    cached_path = CACHE_DIR / prefix / hashed
    if cached_path.is_file():
        with open(cached_path, "rb") as f:
            return f.read()
    else:
        cached_path.parent.mkdir(exist_ok=True, parents=True)
        response = requests.get(url)
        if response.status_code == 200:
            with open(cached_path, "wb") as f:
                f.write(response.content)
            return response.content
        else:
            raise RuntimeError("couldn't retrieve url")


def fetch(url) -> bytes:
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        raise RuntimeError("couldn't retrieve url")


def minutes_status(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    # Find the span containing "Minutes status:"
    status_label = soup.find(
        lambda tag: tag.name == "span" and "Minutes status:" in tag.text
    )
    if status_label:
        # Find the next sibling <td> of the parent <td> to get the status value
        status_value_td = status_label.find_parent("td").find_next_sibling("td")
        if status_value_td:
            status_span = status_value_td.find("span")
            if status_span:
                # print(f"Minutes status: {status_span.text}")
                return status_span.text.lower().strip()
            else:
                print("Minutes status value not found")
                return None
    else:
        print("Label 'Minutes status:' not found")
        return None


def minutes_link(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    # Find the <span> tag that contains "Published minutes:"
    span_tag = soup.find(
        "span", text=lambda text: text and "Published minutes:" in text
    )
    if span_tag:
        # Navigate to the <a> tag from the found <span>
        # Assuming the <a> tag is in the same or next <td> element
        next_td = span_tag.find_parent("td").find_next_sibling("td")
        if next_td:
            a_tag = next_td.find("a")
            if a_tag:
                # Extract the href attribute
                relative_link = a_tag["href"]
                # Combine the relative link with the base URL

                # print(f"Absolute URL: {absolute_url}")
                return relative_link
            else:
                print("Link not found in the next <td>")
                return None
        else:
            print("Next <td> not found")
            return None
    else:
        print("Span with 'Published minutes:' not found")
        return None


def process(title: str, url: str, date_str: str):
    date = datetime_obj = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S GMT")
    content = cached_fetch(url, "url")
    status = minutes_status(content)
    print(f"{date} - {status}")
    if status and "final" in status:
        pdf_rel = minutes_link(content)
        if pdf_rel is not None:
            pdf_url = urljoin(url, pdf_rel)
            print(f"{pdf_url}")
            pdf_content = cached_fetch(pdf_url, "pdf")
            output_name = datetime_obj.strftime("%Y_%m_%d_%H_%M_%S")
            output_path = MINUTES_DIR / (output_name + ".pdf")
            with open(output_path, "wb") as f:
                f.write(pdf_content)


if __name__ == "__main__":
    content = cached_fetch(RSS_URL, "url")
    # Parse the XML content of the feed
    root = ET.fromstring(content)

    # Navigate through the structure to find items
    for item in root.findall(".//item"):
        title = item.find("title").text
        link = item.find("link").text
        pubDate = item.find("pubDate").text

        # Print the title, link, and publication date of each item
        # print(f"Title: {title}\nLink: {link}\nPublication Date: {pubDate}\n")
        process(title, link, pubDate)
