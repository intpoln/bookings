from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAdd
from src.services.facilities import FacilityService

router = APIRouter(prefix="/facilities", tags=["Удобства в номер"])


@router.get("")
@cache(expire=10)
async def get_facilities(db: DBDep):
    return await FacilityService(db).get_facilities()


@router.post("", status_code=201)
async def post_facilities(db: DBDep, facility_data: FacilityAdd = Body()):
    facility = await FacilityService(db).create_facility(facility_data)
    return {"status": "OK", "data": facility}
