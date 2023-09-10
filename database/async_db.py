from __future__ import annotations
import tracemalloc
import asyncio
from sqlalchemy import NullPool, delete, MetaData
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import and_
from sqlalchemy.orm import contains_eager
from tqdm import tqdm

from random import choice

from database.Db_objects import Product, Attribute, Base, Rate, User

import configparser
import pathlib
meta = MetaData()

p = pathlib.Path(__file__).parent.parent.joinpath('config.ini')

config = configparser.ConfigParser()
config.read(p)

BDCONNECTION = config['DEFAULT']["BDCONNECTION"]


def async_to_tread(fun):
    def wrapper(*args, **kwargs):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(fun(*args, **kwargs))
        loop.close()

    return wrapper


def Session(fun):
    async def wrapper(*args):
        engine = create_async_engine(
            BDCONNECTION,
            echo=False,
            poolclass=NullPool,
        )
        async with async_sessionmaker(engine, expire_on_commit=True)() as session:
            async with session.begin():
                result = await fun(session, *args)
                await session.commit()
        return result

    return wrapper


class asyncHandler:
    @staticmethod
    async def init_db() -> None:
        engine = create_async_engine(
            BDCONNECTION,
            echo=False,
            poolclass=NullPool,
        )
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        await engine.dispose()

    @staticmethod
    @Session
    async def add_product(session, product, attributes) -> None:
        prod = Product(product[0], product[1], product[2])
        session.add(prod)
        await session.flush()
        p_id = prod.id
        for i in attributes:
            attribute = Attribute(p_id, i[0], None, str(i[1]), None)
            session.add(attribute)

    @staticmethod
    @Session
    async def add_some_products(session, products) -> None:
        for i in tqdm(products):
            prod = Product(i[0][0], i[0][1], i[0][2])
            session.add(prod)
            await session.flush()
            for j in i[1]:
                attribute = Attribute(prod.id, j[0], None, str(j[1]), None)
                session.add(attribute)

    @staticmethod
    @Session
    async def add_attribute(session, product_id, name, value_type, value, value_description) -> None:
        attribute = Attribute(product_id, name, value_type, value, value_description)
        session.add(attribute)


    @staticmethod
    @Session
    async def get_all_films(session):
        result = await session.execute(select(Product))
        products = result.scalars().all()
        res = []

        for i in products:
            res.append(i)

        return res


    @staticmethod
    @Session
    async def get_all_description(session) -> list:
        result = await session.execute(select(Product))
        products = result.scalars().all()
        res = []
        for prod in tqdm(products):
            if prod.description != '':
                res.append([prod.id, prod.description])
        return res

    @staticmethod
    @Session
    async def get_all_short_description(session) -> list:
        q = select(Product). \
            join(Attribute,
                 and_(Attribute.product_id == Product.id, Attribute.name == "short_desription")). \
            options(contains_eager(Product.attribute))

        result = await session.execute(q)

        products = result.scalars().unique().all()
        res = []
        for prod in tqdm(products):
            res.append([prod.id, prod.attribute[0].value])
        return res


    @staticmethod
    @Session
    async def add_user(session, name, password) -> bool | int:
        result = await session.execute(select(User).filter(User.name == name))
        result = result.scalars().all()
        if result:
            return False
        else:
            user = User(name, password)
            session.add(user)
            await session.flush()
            return user.id

    @staticmethod
    @Session
    async def get_user(session, name, password) -> bool | dict:
        result = await session.execute(select(User).filter(User.name == name))
        result = result.scalars().all()
        if result:
            if result[0].password == password:
                return result[0].__dict__
            else:
                return False
        else:
            return False


    @staticmethod
    @Session
    async def rate_product(session, user_id: int, product_id: int, u_rate: bool):
        rates = await session.execute(select(Rate).filter(and_(Rate.user_id == user_id, Rate.product_id == product_id)))
        rates = rates.scalars().all()
        if rates:
            return False
        else:
            rate = Rate(user_id, product_id, u_rate)
            session.add(rate)


    @staticmethod
    @Session
    async def get_user_rate_id(session, user_id: int, rtype: bool) -> list:
        q = select(Rate).filter(and_(Rate.user_id == user_id, Rate.rate == rtype))
        query_vectors = await session.execute(q)
        query_vectors = query_vectors.scalars().all()
        ids = []
        for i in query_vectors:
            ids.append(i.product_id)

        return ids

    @staticmethod
    @Session
    async def get_random_product(session) -> Product:
        result = await session.execute(select(Product))
        products = result.scalars().all()
        res = choice(products).__dict__
        return res

    @staticmethod
    @Session
    async def get_product_by_req(session, param) -> list[dict] | None:
        result = await session.execute(select(Product))
        products = result.scalars().all()
        res = []
        for i in products:
            if param in i.name:
                res.append(i)
        if len(res) == 0:
            return None
        else:
            res = [i.__dict__ for i in res]
            return res

    @staticmethod
    @Session
    async def get_product_by_id(session, product_id: int) -> dict | None:
        result = await session.execute(select(Product).where(Product.id == product_id))
        product = result.scalars().first()
        if product is None:
            return None
        else:
            return product.__dict__


    @staticmethod
    @Session
    async def clear_products_without_short_description(session):
        statement = delete(Product).where(
            and_(Attribute.name == "short_desription", Attribute.value == "None"))
        # toDel = await session.execute(select(Product).join(Attribute).where(
        #     and_(Attribute.name == "short_desription", Attribute.value != "None")))
        await session.execute(statement)

        # for i in tqdm(products):
        #         await session.delete(i)

    @staticmethod
    async def drop_all() -> None:
        engine = create_async_engine(
            BDCONNECTION,
            echo=False,
            poolclass=NullPool,
        )

        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)



if __name__ == "__main__":
    tracemalloc.start()
    asyncio.run(asyncHandler.init_db())
