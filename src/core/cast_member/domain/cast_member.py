from dataclasses import dataclass, field
from enum import Enum
from uuid import UUID
import uuid

class CastMemberType(Enum):
    DIRECTOR = "DIRECTOR"
    ACTOR = "ACTOR"

@dataclass
class CastMember:
    name: str
    type: CastMemberType
    id: UUID = field(default_factory=uuid.uuid4)

    def validate(self):
        if len(self.name) > 255:
            raise ValueError("name cannot be longer than 255")

        if not self.name:
            raise ValueError("name cannot be empty")

        if not self.type in CastMemberType:
            raise ValueError("type must be a valid CastMemberType: actor or director")

    def __str__(self):
        return f"{self.name} - {self.type}"

    def __repr__(self):
        return f"<CastMember {self.name} {self.type} ({self.id})>"

    def update_cast_member(self, name, type):
        self.name = name
        self.type = type
        self.validate()
