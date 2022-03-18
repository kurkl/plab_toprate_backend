from pydantic import BaseModel, AnyHttpUrl


class TopicSchema(BaseModel):
    link: AnyHttpUrl
    title: str
    seeds: int
    leech: int


class CategorySchema(BaseModel):
    title: str
    url_path: str


class ParentCategorySchema(BaseModel):
    name: str
    categories: list[CategorySchema]
