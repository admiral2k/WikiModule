import re
import requests
from bs4 import BeautifulSoup


class WikiPage:
    def __init__(self, link: str):
        page = requests.get(link)
        self.page = page

    def get_article_link(self) -> str:
        """get url of current random article"""
        return self.page.url

    def get_article_name(self) -> str:
        """get name of current random article"""
        soup = BeautifulSoup(self.page.text, 'lxml')
        article_name = soup.find("h1", class_="firstHeading mw-first-heading").text
        return article_name

    def get_article_content(self) -> str:
        """get content of current random article"""
        soup = BeautifulSoup(self.page.text, 'lxml')
        content_tags = soup.find("div", class_="mw-parser-output").findAll("p")
        formatted_content = ""
        for tag in content_tags:
            # escaping notes and empty tags
            if tag.get("class") != ['asbox-body'] and re.match(r"^(?!\s*$).+", tag.text):
                formatted_content += tag.text

        return formatted_content


class RandomWikiPage(WikiPage):
    _RANDOM_PAGE_TEMPLATE = "https://en.wikipedia.org/wiki/Special:Random"

    def __init__(self):
        super().__init__(self._RANDOM_PAGE_TEMPLATE)

    def randomize(self) -> None:
        """get new random page"""
        self.__init__()


def main():
    some_random_page = RandomWikiPage()
    print("You can read more about", some_random_page.get_article_name(), "here ", some_random_page.get_article_link())
    some_random_page.randomize()
    print("Also, you can read about another interesting topic -", some_random_page.get_article_name())

    # formatting small piece of content
    content_limited = some_random_page.get_article_content()[:100]
    # ending the sentence on a word
    print(f"{content_limited[:content_limited.rfind(' ')]}...")


if __name__ == "__main__":
    main()
