import math

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import select
from app.models.organization import Activity


async def check_activity_depth(activity_id: int, session: AsyncSession) -> int:
    current_depth = 0
    while activity_id:
        query = select(Activity).filter(Activity.id == activity_id)
        res = await session.execute(query)
        activity = res.scalars().first()

        if not activity:
            break

        current_depth += 1
        activity_id = activity.parent_id
        if current_depth > 3:
            raise ValueError("Уровень вложенности не может превышать 3")

    return current_depth


async def get_sub_activity_ids(activity_name: str, session: AsyncSession) -> list[int]:
    try:
        result = await session.execute(
            select(Activity.id).filter(
                (Activity.type_of_activity == activity_name) | (Activity.parent.has(type_of_activity=activity_name))
            )
        )

        sub_activities = result.scalars().all()

        return list(sub_activities)

    except NoResultFound:
        return []


def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2)
    c = 2 * math.asin(math.sqrt(a))
    return R * c
