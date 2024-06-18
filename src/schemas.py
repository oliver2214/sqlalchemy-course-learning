from pydantic import BaseModel


class PersonAddDTO(BaseModel):
    name: str


class PersonDTO(PersonAddDTO):
    id: int


class ProfileAddDTO(BaseModel):
    age: int


class ProfileDTO(ProfileAddDTO):
    id: int
