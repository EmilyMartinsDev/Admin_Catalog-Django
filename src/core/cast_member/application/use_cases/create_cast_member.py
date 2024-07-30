

from dataclasses import dataclass
from uuid import UUID
from core.cast_member.application.use_cases.exceptions import InvalidCastMember
from core.cast_member.domain.cast_member import CastMember, CastMemberType
from core.cast_member.domain.cat_member_repository import CastMemberRepository

@dataclass
class CreateCastMemberResponse:
    id:UUID

@dataclass
class CreateCastMemberRequest:
    name:str
    type: CastMemberType


class CreateCastMember():
    def __init__(
            self,
            repository: CastMemberRepository
            
            ) -> None:
       self.repository = repository
    
    def execute(self, request: CreateCastMemberRequest) -> CreateCastMemberResponse:    
        try:
            cast_member = CastMember(name=request.name, type=request.type)
        except ValueError as exc:    
            raise InvalidCastMember(exc)
        
        self.repository.save(cast_member)
        return CreateCastMemberResponse(id=cast_member.id) 
    
