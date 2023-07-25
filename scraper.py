import re
import time
import random
import requests
import urllib.request
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

from headers import AllHeader

head = AllHeader()


class PRNScrapper:
    def __init__(self, link):
        self.link = link

    def request_text(self, use_random_header=False) -> str:
        if use_random_header:
            random_header = random.choice(head.headers_list)
        else:
            random_header = head.headers_list[0]

        response = requests.get(self.link, headers={"User-Agent": random_header})
        html_text = response.text

        assert type(html_text) == str, "request_text not return a string"
        print("HEADER: ", random_header)
        print("REQUEST STATUS: ", response.status_code)
        # print("TEXT:\n", html_text)
        return html_text

    def get_text_from_tag(self, html_text) -> str:
        """
        class is referred to Metro website
        """
        time.sleep(3)  # delay request
        soup_ = BeautifulSoup(html_text, "html.parser")

        div_tag = soup_.find("div", {"class": "wrap-container"})
        div_col = div_tag.find("div", {"class": "col"}).get_text()

        # print(f"LOGGER: LEN: {len(div_col)}, TYPE: {type(div_col)}")

        div_col_list = [x for x in div_col]
        article_comp = div_col_list[1]
        return str(article_comp)

    def split_text(self, article_comp: str) -> list:
        text_list = article_comp.split(";")
        return text_list


def main(link):
    scraper = PRNScrapper(link)
    html_text = scraper.request_text()
    article_component = scraper.get_text_from_tag(html_text=html_text)
    print(article_component)
    # text_list = scraper.split_text(article_comp=article_component)
    # print(text_list)


if __name__ == "__main__":
    # BERITA HARIAN (403; HIDDEN)
    link_1 = "https://www.bharian.com.my/berita/nasional/2022/11/1021490/senarai-calon-dun-pru15"

    # METRO (200)
    link_2 = "https://www.hmetro.com.my/mutakhir/2022/11/898686/pru-15-senarai-calon-kerusi-parlimen-dun-pn"

    main(link=link_2)
