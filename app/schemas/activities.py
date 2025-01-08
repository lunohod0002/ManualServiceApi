from app.schemas.base import Base


class ActivitySchema(Base):
    type_of_activity: str
    parent_id: int | None
