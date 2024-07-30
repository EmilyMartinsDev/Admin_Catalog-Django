from uuid import UUID, uuid4
from django.test import override_settings
from django.urls import reverse
import pytest
from rest_framework import status
from rest_framework.test import APIClient
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType

from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository


@pytest.fixture
def actor():
    return CastMember(
        name="John Doe",
        type=CastMemberType.ACTOR,
    )


@pytest.fixture
def director():
    return CastMember(
        name="John Krasinski",
        type=CastMemberType.DIRECTOR,
    )


@pytest.fixture
def cast_member_repository() -> DjangoORMCastMemberRepository:
    return DjangoORMCastMemberRepository()


@pytest.mark.django_db
class TestCreateAPI:

    def test_when_request_data_is_invalid_then_return_400(self) -> None:
        url = reverse("cast_member-list")
        data = {
            "name": "",
            "type": "",
        }
        response = APIClient().post(url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            "name": ["This field may not be blank."],
            "type": ['"" is not a valid choice.'],
        }


@pytest.mark.django_db
class TestUpdateAPI:

    def test_when_request_data_is_invalid_then_return_400(self) -> None:
        url = reverse("cast_member-detail", kwargs={"pk": "invalid-uuid"})
        data = {
            "name": "",
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            "id": ["Must be a valid UUID."],
            "name": ["This field may not be blank."],
            "type": ["This field is required."],
        }

    def test_when_cast_member_with_id_does_not_exist_then_return_404(
        self,
    ) -> None:
        url = reverse("cast_member-detail", kwargs={"pk": uuid4()})
        data = {
            "name": "Not Actor",
            "type": "DIRECTOR",
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestDeleteAPI:
    def test_when_cast_member_pk_is_invalid_then_return_400(self) -> None:
        url = reverse("cast_member-detail", kwargs={"pk": "invalid-uuid"})
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {"id": ["Must be a valid UUID."]}

    def test_when_cast_member_not_found_then_return_404(self) -> None:
        url = reverse("cast_member-detail", kwargs={"pk": uuid4()})
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
