from __future__ import annotations
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from typing import List


class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = 'product_table'
    id: Mapped[int] = mapped_column(primary_key=True)
    attribute: Mapped[List[Attribute]] = relationship()
    rates: Mapped[List[Rate]] = relationship(back_populates="product")
    name: Mapped[str]
    photo: Mapped[str]
    description: Mapped[str]

    def __init__(self, name, photo, description):
        self.name = name
        self.photo = photo
        self.description = description


class Attribute(Base):
    __tablename__ = 'attribute_table'
    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("product_table.id"))
    name: Mapped[str]
    value_type: Mapped[str] = mapped_column(nullable=True)
    value: Mapped[str]
    value_description: Mapped[str] = mapped_column(nullable=True)

    def __init__(self, product_id, name, value_type, value, value_description):
        self.product_id = product_id
        self.name = name
        self.value_type = value_type
        self.value = value
        self.value_description = value_description


class User(Base):
    __tablename__ = 'user_table'
    id: Mapped[int] = mapped_column(primary_key=True)
    rates: Mapped[List[Rate]] = relationship(back_populates="user")
    name: Mapped[str]
    password: Mapped[str]

    def __init__(self, name, password):
        self.name = name
        self.password = password


class Rate(Base):
    __tablename__ = "rate_table"
    user_id: Mapped[int] = mapped_column(ForeignKey("user_table.id"), primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("product_table.id"), primary_key=True)
    rate: Mapped[bool]
    product: Mapped[Product] = relationship(back_populates="rates")
    user: Mapped[User] = relationship(back_populates="rates")

    def __init__(self, user_id, product_id, rate):
        self.user_id = user_id
        self.product_id = product_id
        self.rate = rate
