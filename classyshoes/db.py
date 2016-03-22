from contextlib import contextmanager

from sqlalchemy import create_engine, Column, Boolean, Integer, String, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Declarative base type
Base = declarative_base()


# Review in local database storage
class Review(Base):
    __tablename__ = 'review'
    id = Column(Integer, primary_key=True)
    reviewId = Column(String(16), nullable=False, unique=True)
    articleId = Column(String(16), nullable=False)
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    rating = Column(Integer, nullable=False)
    recommend = Column(Boolean, nullable=False)
    helpfulCount = Column(Integer, nullable=False)
    unhelpfulCount = Column(Integer, nullable=False)


# Creates a SQLite disk-baked engine based on path
def mkEngine(path):
    engine = create_engine('sqlite:///{}'.format(path))
    return engine


# Initializes a engine's storage; do this once
def mkStorage(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


# Creates a engine-dependent SQLite session
def mkSession(engine):
    Session = sessionmaker(engine)
    return Session()


# RAII for scoped sessions
@contextmanager
def mkScopedSession(engine):
    session = mkSession(engine)
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
