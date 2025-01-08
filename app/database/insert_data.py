import asyncio

from app.models.organization import Organization, Activity, Building, OrganizationActivity
from app.database.db_session import db_helper


async def insert_data():
    async with db_helper.scoped_session_dependency_context() as session:
        async with session.begin():
            food = Activity(type_of_activity="Еда")
            meat_products = Activity(type_of_activity="Мясная продукция", parent=food)
            dairy_products = Activity(type_of_activity="Молочная продукция", parent=food)
            cars = Activity(type_of_activity="Автомобили")
            cargo_cars = Activity(type_of_activity="Грузовые", parent=cars)
            passenger_cars = Activity(type_of_activity="Легковые", parent=cars)
            spare_parts = Activity(type_of_activity="Запчасти", parent=passenger_cars)
            accessories = Activity(type_of_activity="Аксессуары", parent=passenger_cars)

            session.add_all([food, meat_products, dairy_products, cars,
                             cargo_cars, passenger_cars, spare_parts, accessories])
            await session.commit()

        async with session.begin():
            building1 = Building(address="Улица Пищевая, 1", latitude=55.7558, longitude=37.6173)
            building2 = Building(address="Улица Автомобильная, 2", latitude=55.7600, longitude=37.6200)
            building3 = Building(address="Улица Аксессуарная, 3", latitude=55.7650, longitude=37.6250)

            session.add_all([building1, building2, building3])
            await session.commit()

        async with session.begin():
            org1 = Organization(title="Магазин продуктов", phone_number="89851611586;89162964845", building=building1)
            org2 = Organization(title="Автосалон", phone_number="89851611586;89104414232", building=building2)
            org3 = Organization(title="Сервис по продаже аксессуаров", phone_number="89162964845", building=building2)

            session.add_all([org1, org2, org3])
            await session.commit()

        async with session.begin():
            org_building1 = OrganizationActivity(activity_id=food.id, organization_id=org1.id)
            org_building2 = OrganizationActivity(activity_id=meat_products.id, organization_id=org2.id)
            org_building3 = OrganizationActivity(activity_id=accessories.id, organization_id=org3.id)

            session.add_all([org_building1, org_building2, org_building3])
            await session.commit()


if __name__ == "__main__":
    asyncio.run(insert_data())
