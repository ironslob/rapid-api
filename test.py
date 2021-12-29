# -*- coding: utf-8 -*-

from sqlalchemy.orm import relationship, Session
import sqlalchemy
from datetime import datetime

from .session import Base


from datetime import datetime


class User(Base):
    __tablename__ = "user"

    # fields

    user_id = Column(sqlalchemy.Integer, primary_key=True)

    username = Column(sqlalchemy.Text)

    password = Column(sqlalchemy.Text)

    created_at = Column(sqlalchemy.Integer, default=datetime.utcnow)

    updated_at = Column(
        sqlalchemy.Integer, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # indexes

    # relations

    reviews = relationship(Review, backref="user")


class Restaurant(Base):
    __tablename__ = "restaurant"

    # fields

    restaurant_id = Column(sqlalchemy.Integer, primary_key=True)

    name = Column(sqlalchemy.Text)

    address = Column(sqlalchemy.Text)

    cuisine = Column(sqlalchemy.Text)

    average_rating = Column(sqlalchemy.Numeric(asdecimal=True))

    created_at = Column(sqlalchemy.Integer, default=datetime.utcnow)

    updated_at = Column(
        sqlalchemy.Integer, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # indexes

    # relations

    reviews = relationship(Review, backref="restaurant")


class Review(Base):
    __tablename__ = "review"

    # fields

    review_id = Column(sqlalchemy.Integer, primary_key=True)

    restaurant_id = Column(sqlalchemy.Integer, ForeignKey("restaurant.restaurant_id"))

    user_id = Column(sqlalchemy.Integer, ForeignKey("user.user_id"))

    rating = Column(sqlalchemy.Integer)

    visit_date = Column(sqlalchemy.Integer)

    comment = Column(sqlalchemy.Integer)

    created_at = Column(sqlalchemy.Integer, default=datetime.utcnow)

    updated_at = Column(
        sqlalchemy.Integer, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # indexes

    __table_args__ = (Index("review_restaurant_idx", "restaurant_id"),)

    # relations
