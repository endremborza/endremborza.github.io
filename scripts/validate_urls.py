import time
from pathlib import Path

from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from tqdm import tqdm

XML_PATH = "static/data/tree/main.xml"
ALLOWED_LINKS = ["https://rateyourmusic.com/~endremborza"]


def validate_urls():
    as_ = BeautifulSoup(Path(XML_PATH).read_text(), features="xml").find_all("a")
    links = list(set(a["href"] for a in as_))
    driver = Chrome()
    for link in tqdm(links, desc="links"):
        if link in ALLOWED_LINKS:
            continue
        driver.get(link)
        time.sleep(5)


if __name__ == "__main__":
    validate_urls()
