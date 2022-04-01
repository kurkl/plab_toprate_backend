from fastapi import Query
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from app.schemas.topics import CategorySchema, ParentCategorySchema, TopRatedTopicsOutSchema

router = InferringRouter()


@cbv(router)
class TopicsView:
    @router.get("/categories", name="plab:get-categories-list")
    async def get_categories_list(self) -> list[ParentCategorySchema]:
        """
        Get all categories
        """
        pass

    @router.get("/{category_slug}", name="plab:get-topics")
    async def get_category_topics_list_by_slug(
        self, category_slug: str, limit: int = Query(10, gt=1)
    ) -> CategorySchema:
        """
        Get topics by category slug
        - **category_slug**:
        """
        pass

    @router.get("/{category_slug}/top", name="plab:get-top-rated-topics")
    async def get_top_rated_by_category(
        self,
        category_slug: str,
        limit: int = Query(10, gt=1),
        rate_by: str = Query("leechers", regex="^leech$"),
    ) -> TopRatedTopicsOutSchema:
        """
        Get top rated topics
        - **category_slug**:
        - **limit**:
        - **rate_by**:
        """

        pass
