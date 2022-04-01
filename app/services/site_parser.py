import re
import logging
from operator import itemgetter

import httpx
from bs4 import BeautifulSoup
from pydantic import Field, AnyHttpUrl, BaseSettings
from tenacity import TryAgain, retry, after_log, wait_random, stop_after_attempt

from app.schemas.topics import TopicSchema, CategorySchema, ParentCategorySchema

logger = logging.getLogger(__name__)


class PlabParserConfig(BaseSettings):
    headers: dict
    auth_form_data: dict
    index_page: AnyHttpUrl = Field(...)
    forum_page: AnyHttpUrl = Field(f"{index_page}/forum", exclude=True)
    login_page: AnyHttpUrl = Field(f"{forum_page}/login.php", exclude=True)


class PLabParser:
    def __init__(self, config: PlabParserConfig):
        self.client = httpx.AsyncClient()
        self.config = config

    @retry(stop=stop_after_attempt(5), wait=wait_random(min=1, max=3), after=after_log(logger, logging.ERROR))
    async def _get_html(self, category_url: str, page_num: int) -> str:
        """
        :param category_url: url of category
        :param page_num: page number
        :return: html content
        """
        status, result = await self.client.get(
            f"{self.config.forum_page}{category_url}",
            params={"start": page_num},
            headers=self.config.headers,
        )
        await self.client.aclose()

        if not 200 <= status < 300:
            logger.error(f"http code: {status}, Try again")
            raise TryAgain

        return result

    async def get_topics_by_category(self, category_url: str, pagination: int = 1) -> list[TopicSchema]:
        """
        Get data about category topics and sort it by max leeches
        :param category_url:
        :param pagination: how many scrap pages
        :return: list of Topic objects
        """
        await self.client.get(self.config.login_page, headers=self.config.headers)
        await self.client.post(
            self.config.login_page,
            headers=self.config.headers,
            data=self.config.auth_form_data,
        )
        await self.client.aclose()

        page_num = 0
        results = []
        for _ in range(0, pagination):
            page_html = await self._get_html(category_url, page_num)
            page_content = BeautifulSoup(page_html, "lxml").find("table", {"class": "forumline forum"})
            for topic_content in page_content.find_all(attrs={"id": re.compile("tr-")}):
                topic, rate = topic_content.find("a"), topic_content.find_all(
                    "span", {"class": ["seedmed", "leechmed"]}
                )
                link, title = topic.get("href"), topic.text
                if rate and title:
                    results.append(
                        dict(
                            link=f"{self.config.forum_page}/{link.lstrip()}",
                            title=title,
                            seeders=int(rate[0].next.text),
                            leechers=int(rate[1].next.text),
                            # download_count=0,
                        )
                    )
            page_num += 50
        return [TopicSchema(**item) for item in results]

    @retry(stop=stop_after_attempt(5), wait=wait_random(min=1, max=3), after=after_log(logger, logging.DEBUG))
    async def get_categories(self) -> list[ParentCategorySchema]:
        """
        Get all category with subcategories data from the site
        :return: Category objects
        """

        parent_categories = []
        status, resp = await self.client.get(self.config.index_page, headers=self.config.headers)
        await self.client.aclose()

        if not 200 <= status < 300:
            logger.error(f"http code: {status}, Try again")
            raise TryAgain

        content = BeautifulSoup(resp, "lxml").find_all("table", {"class": "forums"})[3]
        for parent_category in content.find_all("tr"):
            item = parent_category.find("h4", {"class": "forumlink"})
            categories = []
            for category in parent_category.find_all("span", {"class": "sf_title"}):
                title = category.text.strip()
                slug = slugify(title)
                categories.append(
                    CategorySchema(title=title, url_path=category.find("a").get("href")[1:], slug=slug)
                )
            if categories:
                parent_categories.append(ParentCategorySchema(name=item.text.rstrip(), categories=categories))

        return parent_categories


# Helper functions
def slugify(title: str) -> str:
    return "_".join(title.strip())


def sort_topics_by_field(topics: list[TopicSchema], order_by: str = "leechers") -> list[TopicSchema]:
    return sorted(topics, key=itemgetter(order_by), reverse=True)
