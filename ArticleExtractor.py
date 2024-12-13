# imports

import requests
from bs4 import BeautifulSoup
from os import path, makedirs


# set up logging

import logging
from logging import getLogger, basicConfig

logger = getLogger("vacparser")
basicConfig(filename="HabrParser.log", encoding="utf-8", level=logging.DEBUG)


# constants

CACHE_DIR = "cache"
BASE_URL = "https://habr.com"


# functions


def save_to_cache(url, content):
    if not path.exists(CACHE_DIR):
        makedirs(CACHE_DIR)
    filename = path.join(CACHE_DIR, "content.html")
    with open(filename, "wb") as f:
        f.write(content)


def get_page(url):
    logging.debug(f"Downloading {url}")
    response = requests.get(url, headers={"User-Agent": "Custom"})
    if response.status_code == 200:
        logging.debug(
            f"Received {len(response.content)} bytes {response.content[:45]}..."
        )
        save_to_cache(url, response.content)
        return BeautifulSoup(response.content, features="lxml")
    else:
        return None


def check_keywords(keywords, chunks):
    text = ' '.join(chunks).lower()
    return any(keyword.lower() in text for keyword in keywords)


def check_content(keywords, url):
    soup = get_page(url)
    if soup:
        text = soup.select_one('article').text
        return check_keywords(keywords, (text))
    logging.debug(f"Failed to load article {url}")
    return False


def get_articles(start_url, keywords):
    result = []
    soup = get_page(start_url)
    articles = soup.select('article')
    logging.debug(f"{len(articles)} article nodes found")

    for article in articles:
        title_node = article.select_one('h2')
        if title_node:
            title = title_node.text
        else:
            logging.debug(f"Article header <h2> not found {str(article)[:45]}")
            # continue to the next article, as the title element is missing,
            # and the article link is to be extracted from it, too
            continue
        url = BASE_URL + title_node.select_one('a').get('href')
        text_node = article.select_one('p')
        if text_node:
            text = text_node.text
        else:
            logging.debug(f"Article preview <p> not found {str(article)[:45]}")
            text = '' # continue just with article header
        if check_keywords(keywords, [title, text]) or check_content(keywords, url):
            date = article.select_one('time').get('title')
            result.append((date, title, url))
        else:
            logging.debug(f"Skipping article {url} {title[:25]}")
    return result
