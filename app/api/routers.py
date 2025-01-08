from fastapi import APIRouter, status, HTTPException
from fastapi.params import Depends, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_api_key
from app.database.db_session import db_helper
from app.schemas.organizations import OrganizationSchema
from app.schemas.activities import ActivitySchema
from app.services.organizations_service import (
    get_organizations_by_location,
    get_organizations_by_activity_tree,
    get_organization_by_title,
    get_organization_by_id,
    get_organizations_by_building,
    get_organizations_by_activity,
    create_activity
)

router = APIRouter(tags=["Organizations"], prefix="/organizations", dependencies=[Depends(get_api_key)])


@router.get("/building/{building_id}", response_model=list[OrganizationSchema])
async def search_organizations_by_building(
        building_id: int,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
) -> list[OrganizationSchema]:
    try:
        result = await get_organizations_by_building(building_id, session)
        return result
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organizations was not found"
        )


@router.get("/activity/{activity_type}/", response_model=list[OrganizationSchema])
async def search_organizations_by_activity(
        activity_type: str,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    try:
        result = await get_organizations_by_activity(activity_type, session)
        return result
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity was not found"
        )


@router.get("/activities/{activity_name}/", response_model=list[OrganizationSchema])
async def search_organizations_by_activity_tree(
        activity_name: str,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    try:
        result = await get_organizations_by_activity_tree(activity_name, session)
        return result
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization was not found"
        )


@router.get("/location")
async def search_by_location(
        latitude: float = Query(..., description="Широта центра области для радиуса"),
        longitude: float = Query(..., description="Долгота центра области для радиуса"),
        radius: float = Query(None, description="Радиус поиска в километрах (в случае, если задан)"),
        min_latitude: float = Query(None, description="Минимальная широта прямоугольной области"),
        max_latitude: float = Query(None, description="Максимальная широта прямоугольной области"),
        min_longitude: float = Query(None, description="Минимальная долгота прямоугольной области"),
        max_longitude: float = Query(None, description="Максимальная долгота прямоугольной области"),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> dict:
    try:
        result = await get_organizations_by_location(
            latitude=latitude,
            longitude=longitude,
            radius=radius,
            min_longitude=min_longitude,
            max_longitude=max_longitude,
            min_latitude=min_latitude,
            max_latitude=max_latitude,
            session=session
        )
        return result
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organizations was not found"
        )


@router.get("/get_by_id/{organization_id}")
async def search_by_id(
        organization_id: int,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
) -> OrganizationSchema:
    try:
        result = await get_organization_by_id(organization_id=organization_id, session=session)
        return result
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization was not found")


@router.get("/get_by_title/{organization_title}")
async def search_by_title(
        organization_title: str,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
) -> OrganizationSchema:
    try:
        result = await get_organization_by_title(organization_title=organization_title, session=session)
        return result
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization was not found")


@router.post("/add_activity/")
async def add_activity(activity: ActivitySchema,
                       session: AsyncSession = Depends(db_helper.scoped_session_dependency)
                       ):
    try:
        result = await create_activity(activity=activity, session=session)
        return result
    except ValueError as ex:
        raise HTTPException(status_code=400, detail=str(ex))

    except IntegrityError as ex:
        raise HTTPException(status_code=500, detail="Parent id is not exists")

    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
