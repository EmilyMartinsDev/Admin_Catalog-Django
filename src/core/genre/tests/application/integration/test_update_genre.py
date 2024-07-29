import pytest
from uuid import uuid4


from core.category.domain.category import Category
from core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from core.genre.domain.genre import Genre
from core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository
from src.core.genre.application.use_cases.update_genre import UpdateGenre
from src.core.genre.application.use_cases.exceptions import GenreNotFound, InvalidGenre, RelatedCategoriesNotFound

class TestUpdateGenre:
    def test_update_genre_not_exists(self):
        # Arrange: Create in-memory repositories and use case
        category_repository = InMemoryCategoryRepository()
        genre_repository = InMemoryGenreRepository()

        use_case = UpdateGenre(
            repository=genre_repository,
            category_repository=category_repository
        )

        # Create an Input dataclass instance with a non-existent genre ID
        non_existent_genre_id = uuid4()  # Generate a random UUID
        input_data = UpdateGenre.Input(
            id=non_existent_genre_id,
            name="test2",
            is_active=True,
            categories=set()
        )

        # Act & Assert: Attempt to update a genre that doesn't exist and expect a GenreNotFound exception
        with pytest.raises(GenreNotFound) as ex:
            use_case.execute(input_data)

        # Optionally, assert the exception message or properties if necessary
        assert str(ex.value) == f"Genre with {non_existent_genre_id} not found"

    def test_update_genre_with_invalid_attributes(self):
        # Arrange: Create in-memory repositories and use case
            category_repository = InMemoryCategoryRepository()
            genre_repository = InMemoryGenreRepository()
            genre = Genre(name="Initial Genre", is_active=True, categories=set())
            # Add a genre to the repository for testing
            genre_repository.save(genre)

            get_genre = genre_repository.get_by_id(genre.id)

            use_case = UpdateGenre(
                repository=genre_repository,
                category_repository=category_repository
            )

            # Act & Assert: Attempt to update a genre with invalid attributes and expect an InvalidGenre exception
            invalid_name = ""  # Assuming an empty name is invalid
            with pytest.raises(InvalidGenre):
                use_case.execute(UpdateGenre.Input(
                    id=get_genre.id,
                    name=invalid_name,
                    is_active=True,
                    categories=set()
                ))
    def test_update_genre_with_non_existing_categories(self):
        # Arrange: Create in-memory repositories and use case
        category_repository = InMemoryCategoryRepository()
        genre_repository = InMemoryGenreRepository()

        genre = Genre(name="Initial Genre", is_active=True, categories=set())
            # Add a genre to the repository for testing
        genre_repository.save(genre)

        get_genre = genre_repository.get_by_id(genre.id)

        use_case = UpdateGenre(
            repository=genre_repository,
            category_repository=category_repository
        )

        # Act & Assert: Attempt to update a genre with non-existing categories and expect a RelatedCategoriesNotFound exception
        non_existing_category_id = uuid4()  # Generate a random UUID for a non-existing category
        with pytest.raises(RelatedCategoriesNotFound):
            use_case.execute(UpdateGenre.Input(
                id=get_genre.id,
                name="Updated Genre",
                is_active=True,
                categories={non_existing_category_id}
            ))
    def test_update_genre_with_existing_categories(self):
        # Arrange: Create in-memory repositories and use case
        category_repository = InMemoryCategoryRepository()
        genre_repository = InMemoryGenreRepository()
    
        category_1 = Category(name="cat1")
        category_2 = Category(name="cat2")

        category_repository.save(category_1)
        category_repository.save(category_2)
        
        genre = Genre(name="genre1", categories={category_1.id, category_2.id}) 
        # Add a genre to the repository for testing
        genre_repository.save(genre)

        use_case = UpdateGenre(
            repository=genre_repository,
            category_repository=category_repository
        )

        # Act: Update the genre with existing categories
        input_data = UpdateGenre.Input(
            id=genre.id,
            name="Updated Genre",
            is_active=False,
            categories={category_1.id, category_2.id}
        )
        use_case.execute(input_data)

        # Assert: Check if the genre was updated correctly
        updated_genre = genre_repository.get_by_id(genre.id)
        assert updated_genre.name == "Updated Genre"
        assert updated_genre.is_active is False
        assert updated_genre.categories == {category_1.id, category_2.id}        