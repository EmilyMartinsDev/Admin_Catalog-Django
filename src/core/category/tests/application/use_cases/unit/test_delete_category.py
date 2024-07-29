from unittest.mock import create_autospec
from core.category.application.category_repository import CategoryRepository
from core.category.application.use_cases.delete_category import DeleteCategory, DeleteCategoryRequest
from core.category.domain.category import Category


class TestDeleteCategory:
    def test_delete_category_from_repository(self):
        category = Category(
            name="Filme",
            description="Categoria de filmes",
        )
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = DeleteCategory(mock_repository)
        use_case.execute(DeleteCategoryRequest(id=category.id))

        mock_repository.delete.assert_called_once_with(category.id)
