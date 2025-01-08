from app.utils.utils import get_sub_activity_ids, haversine, check_activity_depth
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy import select
from app.models.organization import Building, Organization
from app.schemas.organizations import OrganizationSchema
from app.models.organization import Activity
from app.schemas.activities import ActivitySchema


async def get_organizations_by_building(
        building_id: int,
        session: AsyncSession
) -> list[OrganizationSchema]:
    query = select(Organization).options(
        selectinload(Organization.building),
        selectinload(Organization.activities)
    ).filter(Organization.building_id == building_id)
    res = await session.execute(query)
    result = res.scalars().all()
    return result


async def get_organizations_by_activity(
        activity_name: str,
        session: AsyncSession
) -> list[OrganizationSchema]:
    query = select(Organization).options(selectinload(Organization.building), selectinload(Organization.activities)
                                         ).join(Organization.activities).filter(
        Activity.type_of_activity == activity_name)
    res = await session.execute(query)
    result = res.scalars().all()
    return result


async def get_organizations_by_activity_tree(
        activity_name: str,
        session: AsyncSession
) -> list[OrganizationSchema]:
    sub_activities_ids = await get_sub_activity_ids(activity_name, session)
    query = select(Organization).options(
        selectinload(Organization.building), selectinload(Organization.activities)
    ).join(Organization.activities).filter(Activity.id.in_(sub_activities_ids))
    res = await session.execute(query)
    result = res.unique().scalars().all()
    return result


async def get_organizations_by_location(
        latitude: float,
        longitude: float,
        radius: float,
        min_latitude: float,
        max_latitude: float,
        min_longitude: float,
        max_longitude: float,
        session: AsyncSession
) -> dict:
    query = select(Building)
    buildings_data = await session.execute(query)
    buildings = buildings_data.scalars().all()

    building_ids = set()

    if radius is not None:
        for building in buildings:
            distance = haversine(latitude, longitude, building.latitude, building.longitude)
            if distance <= radius:
                building_ids.add(building.id)

    if min_latitude is not None and max_latitude is not None and min_longitude is not None and max_longitude is not None:
        buildings_in_box = [
            building.id for building in buildings
            if (min_latitude <= building.latitude <= max_latitude and
                min_longitude <= building.longitude <= max_longitude)
        ]
        building_ids.update(buildings_in_box)

    building_ids = list(building_ids)
    print(building_ids)

    if not building_ids:
        return {"organizations": [], "buildings": []}

    organizations_query = select(Organization).options(
            selectinload(Organization.building),
                    selectinload(Organization.activities)
                                                    ).where(Organization.building_id.in_(building_ids))
    organizations_data = await session.execute(organizations_query)
    result = organizations_data.scalars().all()
    organizations = [OrganizationSchema.model_validate(o) for o in result]
    buildings = [o.building for o in organizations]
    return {
        "organizations": organizations,
        "buildings": buildings
    }


async def get_organization_by_id(
        organization_id: int,
        session: AsyncSession
) -> OrganizationSchema:
    query = select(Organization).options(selectinload(Organization.building),
                                         selectinload(Organization.activities)).filter_by(id=organization_id)
    res = await session.execute(query)
    result = res.unique().scalar_one()
    return OrganizationSchema.model_validate(result)


async def get_organization_by_title(
        organization_title: str,
        session: AsyncSession
) -> OrganizationSchema:
    query = (select(Organization).options(selectinload(Organization.building), selectinload(Organization.activities)).
             filter_by(title=organization_title))
    res = await session.execute(query)
    result = res.unique().scalar_one()
    return result


async def create_activity(
        activity: ActivitySchema,
        session: AsyncSession
):
    if activity and activity.parent_id:
        await check_activity_depth(activity.parent_id, session)
    activity_data = activity.model_dump(exclude_unset=True)
    new_activity = Activity(**activity_data)
    session.add(new_activity)
    await session.commit()
    await session.refresh(new_activity)
    return new_activity
