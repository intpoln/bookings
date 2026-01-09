from pydantic import BaseModel


class FacilityAdd(BaseModel):
    title: str


class Facility(BaseModel):
    id: int
    title: str


class RoomFacilityAdd(BaseModel):
    room_id: int
    facility_id: int


class RoomFacility(RoomFacilityAdd):
    id: int
