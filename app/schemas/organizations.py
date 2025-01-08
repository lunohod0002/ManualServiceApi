from app.schemas.base import Base
from app.schemas.activities import ActivitySchema


class BuildingInfo(Base):
    address: str
    latitude: float
    longitude: float


class OrganizationSchema(Base):
    title: str
    phone_number: str
    building: BuildingInfo
    activities: list[ActivitySchema]
