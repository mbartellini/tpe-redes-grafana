from sqlalchemy import Boolean, Column, Date, Float, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from database import Base

#User model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    password = Column(String, nullable=False)

#Media model
class Media(Base):
    __tablename__ = "media"

    mediaId = Column("mediaid",Integer, primary_key=True, index=True, autoincrement=True)
    type = Column(Boolean, nullable=False)
    name = Column(String(255), nullable=False)
    originalLanguage = Column("originallanguage",String(2), nullable=True)
    adult = Column(Boolean, nullable=False)
    releaseDate = Column("releasedate",Date, nullable=True)
    overview = Column(Text, nullable=False)
    backdropPath = Column("backdroppath",String(255), nullable=True)
    posterPath = Column("posterpath",String(255), nullable=True)
    trailerLink = Column("trailerlink",String(255), nullable=True)
    tmdbRating = Column("tmdbrating",Float, nullable=False)
    status = Column(String(20), nullable=False)

