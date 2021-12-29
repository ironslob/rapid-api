# -*- coding: utf-8 -*-

import logging
import os

from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

logger = logging.getLogger(__name__)

SQLALCHEMY_DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,
)

Base = declarative_base()


# SessionManager is an alternative way to get a DB connection
# as an alternative to FastApi Depends that seems to quickly
# exhaust the Postgres open connections:
# https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/104
@contextmanager
def SessionManager():
    db = SessionLocal()

    try:
        yield db

    except Exception as e:
        logger.warning(e)
        db.rollback()
        raise

    finally:
        db.close()
