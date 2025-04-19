import os
from faker import Faker
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Faker nesnesini oluştur
fake = Faker('tr_TR')

# Veritabanı bağlantısı
engine = create_engine('postgresql://postgres:123456@localhost:5432/netflix_recommender')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Veritabanı modelleri
class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # İlişkiler
    watch_history = relationship("WatchHistory", back_populates="user")
    preferences = relationship("UserPreferences", back_populates="user")

class Movie(Base):
    __tablename__ = 'movies'
    movie_id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    genre = Column(String(100))
    release_year = Column(Integer)
    rating = Column(Float)
    description = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # İlişkiler
    watch_history = relationship("WatchHistory", back_populates="movie")

class WatchHistory(Base):
    __tablename__ = 'watch_history'
    history_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    movie_id = Column(Integer, ForeignKey('movies.movie_id'))
    watch_date = Column(DateTime, default=datetime.utcnow)
    rating = Column(Integer)
    watch_duration = Column(Integer)
    
    # İlişkiler
    user = relationship("User", back_populates="watch_history")
    movie = relationship("Movie", back_populates="watch_history")

class UserPreferences(Base):
    __tablename__ = 'user_preferences'
    preference_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    favorite_genres = Column(String(200))
    preferred_actors = Column(String(200))
    watch_time_preference = Column(String(20))
    
    # İlişkiler
    user = relationship("User", back_populates="preferences")

# Veritabanı tablolarını oluştur
Base.metadata.create_all(engine)

# Film türleri
genres = [
    "Aksiyon", "Macera", "Animasyon", "Komedi", "Suç", "Belgesel",
    "Drama", "Aile", "Fantastik", "Korku", "Müzikal", "Gizem",
    "Romantik", "Bilim Kurgu", "Gerilim", "Savaş", "Western"
]

# Film başlıkları
movie_titles = [
    "Yıldızlararası", "Başlangıç", "Kara Şövalye", "Prestij", "Dövüş Kulübü",
    "Zindan Adası", "Yeşil Yol", "Esaretin Bedeli", "Forrest Gump", "Piyanist",
    "Gladyatör", "Titanik", "Matrix", "Yüzüklerin Efendisi", "Harry Potter",
    "Yıldız Savaşları", "Terminatör", "Jurassic Park", "Jaws", "E.T."
]

# Kullanıcı verilerini oluştur
def generate_users(n=50):
    users = []
    for _ in range(n):
        user = User(
            username=fake.user_name(),
            email=fake.email(),
            password_hash=fake.password(),
            created_at=fake.date_time_this_year()
        )
        users.append(user)
    session.add_all(users)
    session.commit()
    return users

# Film verilerini oluştur
def generate_movies(n=100):
    movies = []
    for _ in range(n):
        movie = Movie(
            title=f"{fake.random_element(movie_titles)} {fake.random_int(min=1, max=10)}",
            genre=fake.random_element(genres),
            release_year=fake.random_int(min=1980, max=2023),
            rating=round(fake.random.uniform(1, 10), 1),
            description=fake.text(max_nb_chars=200)
        )
        movies.append(movie)
    session.add_all(movies)
    session.commit()
    return movies

# İzleme geçmişi verilerini oluştur
def generate_watch_history(users, movies):
    watch_history = []
    for user in users:
        # Her kullanıcı için 5-10 izleme kaydı
        n_watches = fake.random_int(min=5, max=10)
        user_movies = fake.random_elements(elements=movies, length=n_watches, unique=True)
        
        for movie in user_movies:
            history = WatchHistory(
                user_id=user.user_id,
                movie_id=movie.movie_id,
                watch_date=fake.date_time_this_year(),
                rating=fake.random_int(min=1, max=5),
                watch_duration=fake.random_int(min=30, max=180)
            )
            watch_history.append(history)
    
    session.add_all(watch_history)
    session.commit()
    return watch_history

# Kullanıcı tercihlerini oluştur
def generate_user_preferences(users):
    preferences = []
    for user in users:
        preference = UserPreferences(
            user_id=user.user_id,
            favorite_genres=",".join(fake.random_elements(elements=genres, length=3, unique=True)),
            preferred_actors=",".join([fake.name() for _ in range(3)]),
            watch_time_preference=fake.random_element(elements=("morning", "afternoon", "evening", "night"))
        )
        preferences.append(preference)
    
    session.add_all(preferences)
    session.commit()
    return preferences

# Ana fonksiyon
def main():
    print("Veri üretme başlıyor...")
    
    # Verileri oluştur
    users = generate_users()
    print(f"{len(users)} kullanıcı oluşturuldu.")
    
    movies = generate_movies()
    print(f"{len(movies)} film oluşturuldu.")
    
    watch_history = generate_watch_history(users, movies)
    print(f"{len(watch_history)} izleme kaydı oluşturuldu.")
    
    preferences = generate_user_preferences(users)
    print(f"{len(preferences)} kullanıcı tercihi oluşturuldu.")
    
    print("Veri üretme tamamlandı!")

if __name__ == "__main__":
    main() 