from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

# Veritabanı bağlantı ayarları
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123456@localhost:5432/netflix_recommender"

# Veritabanı motoru
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

# Session oluşturucu
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base model
Base = declarative_base()

# Veritabanı modelleri
class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    # İlişkiler
    watch_history = relationship("WatchHistory", back_populates="user")
    preferences = relationship("UserPreferences", back_populates="user")

class Movie(Base):
    __tablename__ = "movies"

    movie_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    genre = Column(String(100))
    release_year = Column(Integer)
    rating = Column(Float)
    description = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)

    # İlişkiler
    watch_history = relationship("WatchHistory", back_populates="movie")

class WatchHistory(Base):
    __tablename__ = "watch_history"

    history_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    movie_id = Column(Integer, ForeignKey("movies.movie_id"))
    watch_date = Column(DateTime, default=datetime.utcnow)
    rating = Column(Integer)
    watch_duration = Column(Integer)

    # İlişkiler
    user = relationship("User", back_populates="watch_history")
    movie = relationship("Movie", back_populates="watch_history")

class UserPreferences(Base):
    __tablename__ = "user_preferences"

    preference_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    favorite_genres = Column(String(200))
    preferred_actors = Column(String(200))
    watch_time_preference = Column(String(20))

    # İlişkiler
    user = relationship("User", back_populates="preferences")

# Veritabanı bağlantısı
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 