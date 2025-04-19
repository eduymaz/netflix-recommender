from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Optional
import joblib
import pandas as pd
import numpy as np
from pydantic import BaseModel
import jwt
from jose import jwt
from passlib.context import CryptContext
from database.database import SessionLocal, engine, Base
from database.database import User, Movie, WatchHistory, UserPreferences
import logging
import os

# Logging ayarları
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='api.log'
)

# FastAPI uygulaması
app = FastAPI(title="Netflix Benzeri Öneri Sistemi API")

# Veritabanı modellerini oluştur
Base.metadata.create_all(bind=engine)

# Güvenlik ayarları
SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Pydantic modelleri
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserResponse(BaseModel):
    user_id: int
    username: str
    email: str
    created_at: datetime

class MovieResponse(BaseModel):
    movie_id: int
    title: str
    genre: str
    release_year: int
    rating: float
    description: str

class WatchHistoryCreate(BaseModel):
    movie_id: int
    rating: int
    watch_duration: int

class UserPreferencesCreate(BaseModel):
    favorite_genres: str
    preferred_actors: str
    watch_time_preference: str

# Veritabanı bağlantısı
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Yardımcı fonksiyonlar
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user

# API Endpoint'leri
@app.post("/api/users/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Kullanıcı adı ve email kontrolü
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already registered")
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Yeni kullanıcı oluştur
    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=get_password_hash(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/api/users/login")
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == login_data.username).first()
    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/users/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@app.put("/api/users/preferences")
def update_preferences(
    preferences: UserPreferencesCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_preferences = db.query(UserPreferences).filter(
        UserPreferences.user_id == current_user.user_id
    ).first()
    
    if user_preferences:
        user_preferences.favorite_genres = preferences.favorite_genres
        user_preferences.preferred_actors = preferences.preferred_actors
        user_preferences.watch_time_preference = preferences.watch_time_preference
    else:
        user_preferences = UserPreferences(
            user_id=current_user.user_id,
            **preferences.dict()
        )
        db.add(user_preferences)
    
    db.commit()
    return {"message": "Preferences updated successfully"}

@app.get("/api/movies", response_model=List[MovieResponse])
def get_movies(
    skip: int = 0,
    limit: int = 10,
    genre: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Movie)
    if genre:
        query = query.filter(Movie.genre.contains(genre))
    movies = query.offset(skip).limit(limit).all()
    return movies

@app.get("/api/movies/recommendations", response_model=List[MovieResponse])
def get_recommendations(
    token: str,
    db: Session = Depends(get_db)
):
    try:
        logging.info("Öneri isteği başladı")
        current_user = get_current_user(token, db)
        logging.info(f"Kullanıcı doğrulandı: {current_user.username}")
        
        # Kullanıcının izleme geçmişini al
        user_history = db.query(WatchHistory).filter(
            WatchHistory.user_id == current_user.user_id
        ).all()
        
        if not user_history:
            logging.info("Kullanıcının izleme geçmişi yok, rastgele filmler öneriliyor")
            # İzleme geçmişi yoksa, rastgele filmler öner
            recommended_movies = db.query(Movie).order_by(
                Movie.rating.desc()
            ).limit(10).all()
            return recommended_movies
        
        # Kullanıcının beğendiği film türlerini bul
        favorite_genres = {}
        for history in user_history:
            if history.rating >= 4:  # 4 ve üzeri puan verdiği filmler
                movie = db.query(Movie).filter(
                    Movie.movie_id == history.movie_id
                ).first()
                if movie and movie.genre:
                    favorite_genres[movie.genre] = favorite_genres.get(movie.genre, 0) + 1
        
        # En çok beğenilen türleri bul
        top_genres = sorted(favorite_genres.items(), key=lambda x: x[1], reverse=True)[:3]
        top_genre_names = [genre for genre, _ in top_genres]
        
        logging.info(f"Kullanıcının favori türleri: {top_genre_names}")
        
        # Bu türlerdeki, kullanıcının henüz izlemediği filmleri öner
        watched_movie_ids = [history.movie_id for history in user_history]
        recommended_movies = db.query(Movie).filter(
            Movie.genre.in_(top_genre_names),
            ~Movie.movie_id.in_(watched_movie_ids)
        ).order_by(
            Movie.rating.desc()
        ).limit(10).all()
        
        logging.info(f"{len(recommended_movies)} film önerisi bulundu")
        return recommended_movies
    
    except Exception as e:
        logging.error(f"Öneri hatası: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Recommendation error: {str(e)}")

@app.post("/api/movies/rate")
def rate_movie(
    watch_data: WatchHistoryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # İzleme kaydı oluştur
    watch_history = WatchHistory(
        user_id=current_user.user_id,
        movie_id=watch_data.movie_id,
        rating=watch_data.rating,
        watch_duration=watch_data.watch_duration
    )
    db.add(watch_history)
    db.commit()
    
    return {"message": "Rating added successfully"}

@app.get("/api/history", response_model=List[WatchHistoryCreate])
def get_watch_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    history = db.query(WatchHistory).filter(
        WatchHistory.user_id == current_user.user_id
    ).all()
    return history

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 