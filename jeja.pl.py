""" Losuje dowcip ze strony https://dowcipy.jeja.pl """

import random
import re
import time

from bs4 import BeautifulSoup
import cloudscraper

SCRAPER = cloudscraper.CloudScraper()


def list_topics() -> list:

    url = r"https://dowcipy.jeja.pl"

    result = SCRAPER.get(url)
    print()

    topics = (
        BeautifulSoup(result.text, "html.parser")
        .find_all("div", {"class": "menu-right"})[-1]
        .find_all("li")
    )
    return topics


def draw_topic():

    topics = list_topics()
    chosen = random.choice(topics)
    chosen_topic = chosen.find("a").get_text()
    chosen_href = chosen.find("a")["href"]
    print(f"KATEGORIA: {chosen_topic}")
    url = r"https://dowcipy.jeja.pl/" + chosen_href
    return url


def scrap_links_under_pagination(url):

    result = SCRAPER.get(url, timeout=10)
    latest_page = BeautifulSoup(result.text, "html.parser").find_all(
        "a", {"class": "pagination-number"}
    )[-1]
    url = latest_page["href"]
    for idx in range(1, int(latest_page.get_text()) + 1):
        result = (
            r"https://dowcipy.jeja.pl/" + re.split(r"\d+.html", url)[0] + f"{idx}.html"
        )
        yield result


def draw_page(url):
    pages = scrap_links_under_pagination(url)
    pages = list(pages)
    print(f"Znaleziono {len(pages)} stron dla kategorii.\n")
    return random.choice(pages)


def scrap_jokes(url: str = r"https://dowcipy.jeja.pl/nowe,4,binladen.html"):

    page = draw_page(url)
    result = SCRAPER.get(page)
    boxes = BeautifulSoup(result.text, "html.parser").find_all(
        "div", {"class": "dow-left-text"}
    )
    for box in boxes:
        yield box.find("p").get_text()


def draw_joke():

    url = draw_topic()
    time.sleep(1)
    jokes = scrap_jokes(url)
    jokes = list(jokes)
    chosen = random.choice(jokes)
    okcyan = "\033[96m"
    print(f"{okcyan}{chosen}")


if __name__ == "__main__":
    draw_joke()
