from pydantic import BaseModel, AnyHttpUrl


class TopicSchema(BaseModel):
    link: AnyHttpUrl
    title: str
    seeders: int
    leechers: int
    # download_count: int


class CategorySchema(BaseModel):
    title: str
    slug: str
    url_path: str
    topics: list[TopicSchema] | None = None


class ParentCategorySchema(BaseModel):
    name: str
    categories: list[CategorySchema]


class TopRatedTopicsOutSchema(BaseModel):
    topics: list[TopicSchema]
    order_by: str
