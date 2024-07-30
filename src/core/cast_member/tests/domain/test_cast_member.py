import pytest
from uuid import UUID

from core.cast_member.domain.cast_member import CastMember, CastMemberType


def test_cast_member_initialization():
    cast_member = CastMember(name="John Doe", type=CastMemberType.ACTOR)
    assert isinstance(cast_member.id, UUID)
    assert cast_member.name == "John Doe"
    assert cast_member.type == CastMemberType.ACTOR


def test_cast_member_update():
    cast_member = CastMember(name="John Doe", type=CastMemberType.ACTOR)
    cast_member.update_cast_member(name="Jane Doe", type=CastMemberType.DIRECTOR)
    assert cast_member.name == "Jane Doe"
    assert cast_member.type == CastMemberType.DIRECTOR

def test_cast_member_str_repr():
    cast_member = CastMember(name="John Doe", type=CastMemberType.ACTOR)
    assert str(cast_member) == "John Doe - CastMemberType.ACTOR"
    assert repr(cast_member) == f"<CastMember John Doe CastMemberType.ACTOR ({cast_member.id})>"

if __name__ == "__main__":
    pytest.main()
