# -*- coding: utf-8 -*-

from sqlalchemy.orm import relationship
import sqlalchemy

from .session import Base


    
from datetime import datetime
    



class user(Base):
    __tablename__ = "user"

    # fields
    

    user_id = Column(
        sqlalchemy.Integer
        
        
        , primary_key=True
        
        , nullable=False
        
        
    )

    

    username = Column(
        sqlalchemy.Text
        
        
        , nullable=False
        
        
    )

    

    password = Column(
        sqlalchemy.Text
        
        
        , nullable=False
        
        
    )

    

    created_at = Column(
        sqlalchemy.DateTime
        
        
        , nullable=False
        
        , default=datetime.utcnow
        
        
    )

    

    updated_at = Column(
        sqlalchemy.DateTime
        
        
        , nullable=False
        
        , default=datetime.utcnow
        
        
        , onupdate=datetime.utcnow
        
    )

    

    

    
        

    reviews = relationship(
        review
        
        , backref="user"
        
    )

        
    

class restaurant(Base):
    __tablename__ = "restaurant"

    # fields
    

    restaurant_id = Column(
        sqlalchemy.Integer
        
        
        , primary_key=True
        
        , nullable=False
        
        
    )

    

    name = Column(
        sqlalchemy.Text
        
        
        , nullable=False
        
        
    )

    

    address = Column(
        sqlalchemy.Text
        
        
        , nullable=False
        
        
    )

    

    cuisine = Column(
        sqlalchemy.Text
        
        
        , nullable=False
        
        
    )

    

    average_rating = Column(
        sqlalchemy.Numeric(asdecimal=True)
        
        
        , nullable=False
        
        
    )

    

    created_at = Column(
        sqlalchemy.DateTime
        
        
        , nullable=False
        
        , default=datetime.utcnow
        
        
    )

    

    updated_at = Column(
        sqlalchemy.DateTime
        
        
        , nullable=False
        
        , default=datetime.utcnow
        
        
        , onupdate=datetime.utcnow
        
    )

    

    

    
        

    reviews = relationship(
        review
        
        , backref="restaurant"
        
    )

        
    

class review(Base):
    __tablename__ = "review"

    # fields
    

    review_id = Column(
        sqlalchemy.Integer
        
        
        , primary_key=True
        
        , nullable=False
        
        
    )

    

    restaurant_id = Column(
        sqlalchemy.Integer
        
        , ForeignKey("restaurant.restaurant_id")
        
        
        , nullable=False
        
        
    )

    

    user_id = Column(
        sqlalchemy.Integer
        
        , ForeignKey("user.user_id")
        
        
        , nullable=False
        
        
    )

    

    rating = Column(
        sqlalchemy.Integer
        
        
        , nullable=False
        
        
    )

    

    visit_date = Column(
        sqlalchemy.Date
        
        
        , nullable=False
        
        
    )

    

    comment = Column(
        sqlalchemy.Integer
        
        
        , nullable=False
        
        
    )

    

    created_at = Column(
        sqlalchemy.DateTime
        
        
        , nullable=False
        
        , default=datetime.utcnow
        
        
    )

    

    updated_at = Column(
        sqlalchemy.DateTime
        
        
        , nullable=False
        
        , default=datetime.utcnow
        
        
        , onupdate=datetime.utcnow
        
    )

    

    
    __table_args__ = (
        
        sqlalchemy.Index("review_restaurant_idx", "restaurant_id" ),
        
    )
    

    
