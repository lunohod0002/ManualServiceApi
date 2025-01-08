from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Organization(Base):
    __tablename__ = "organizations"

    title: Mapped[str]
    phone_number: Mapped[str]
    building_id: Mapped[int] = mapped_column(ForeignKey('buildings.id'), nullable=True)

    activities: Mapped[list["Activity"]] = relationship(
        secondary="organizationactivities", back_populates="organizations"
    )

    building: Mapped["Building"] = relationship("Building", remote_side="Building.id", back_populates="organizations")


class OrganizationActivity(Base):
    __tablename__ = "organizationactivities"
    activity_id: Mapped[int] = mapped_column(ForeignKey('activities.id'))
    organization_id: Mapped[int] = mapped_column(ForeignKey('organizations.id'))


class Building(Base):
    __tablename__ = "buildings"

    address: Mapped[str]
    latitude: Mapped[float]
    longitude: Mapped[float]
    organizations: Mapped[list["Organization"]] = relationship("Organization", back_populates="building")


class Activity(Base):
    __tablename__ = "activities"
    type_of_activity: Mapped[str] = mapped_column(String, unique=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey('activities.id'), nullable=True)
    parent: Mapped["Activity"] = relationship("Activity", remote_side="Activity.id", back_populates="children")
    children: Mapped[list["Activity"]] = relationship("Activity", back_populates="parent")
    organizations: Mapped[list["Organization"]] = relationship(
        secondary="organizationactivities", back_populates="activities"
    )
