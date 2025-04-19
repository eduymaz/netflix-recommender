import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import logging
from datetime import datetime
import os

# Logging ayarları
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='data_processing.log'
)

# Veritabanı bağlantısı
engine = create_engine('sqlite:///netflix_recommender.db')

def load_data():
    """Veritabanından verileri yükle"""
    try:
        # Kullanıcı verilerini yükle
        users_df = pd.read_sql('SELECT * FROM users', engine)
        
        # Film verilerini yükle
        movies_df = pd.read_sql('SELECT * FROM movies', engine)
        
        # İzleme geçmişini yükle
        watch_history_df = pd.read_sql('SELECT * FROM watch_history', engine)
        
        # Kullanıcı tercihlerini yükle
        preferences_df = pd.read_sql('SELECT * FROM user_preferences', engine)
        
        logging.info("Veriler başarıyla yüklendi")
        return users_df, movies_df, watch_history_df, preferences_df
    
    except Exception as e:
        logging.error(f"Veri yükleme hatası: {str(e)}")
        raise

def clean_data(users_df, movies_df, watch_history_df, preferences_df):
    """Verileri temizle ve dönüştür"""
    try:
        # Eksik değerleri kontrol et
        logging.info("Eksik değerler kontrol ediliyor...")
        for df, name in [(users_df, 'users'), (movies_df, 'movies'), 
                        (watch_history_df, 'watch_history'), (preferences_df, 'preferences')]:
            missing_values = df.isnull().sum()
            if missing_values.any():
                logging.warning(f"{name} tablosunda eksik değerler bulundu:\n{missing_values}")
        
        # Kullanıcı verilerini temizle
        users_df['created_at'] = pd.to_datetime(users_df['created_at'])
        users_df['age'] = np.random.randint(18, 65, size=len(users_df))
        
        # Film verilerini temizle
        movies_df['release_year'] = pd.to_numeric(movies_df['release_year'], errors='coerce')
        movies_df['rating'] = pd.to_numeric(movies_df['rating'], errors='coerce')
        movies_df['genre'] = movies_df['genre'].fillna('Bilinmiyor')
        
        # İzleme geçmişini temizle
        watch_history_df['watch_date'] = pd.to_datetime(watch_history_df['watch_date'])
        watch_history_df['rating'] = pd.to_numeric(watch_history_df['rating'], errors='coerce')
        watch_history_df['watch_duration'] = pd.to_numeric(watch_history_df['watch_duration'], errors='coerce')
        
        # Kullanıcı tercihlerini temizle
        preferences_df['favorite_genres'] = preferences_df['favorite_genres'].fillna('')
        preferences_df['preferred_actors'] = preferences_df['preferred_actors'].fillna('')
        preferences_df['watch_time_preference'] = preferences_df['watch_time_preference'].fillna('evening')
        
        logging.info("Veri temizleme tamamlandı")
        return users_df, movies_df, watch_history_df, preferences_df
    
    except Exception as e:
        logging.error(f"Veri temizleme hatası: {str(e)}")
        raise

def feature_engineering(users_df, movies_df, watch_history_df, preferences_df):
    """Özellik mühendisliği yap"""
    try:
        # Kullanıcı özellikleri
        user_features = pd.DataFrame()
        user_features['user_id'] = users_df['user_id']
        
        # İzleme istatistikleri
        watch_stats = watch_history_df.groupby('user_id').agg({
            'rating': ['mean', 'count'],
            'watch_duration': ['mean', 'sum']
        }).reset_index()
        watch_stats.columns = ['user_id', 'avg_rating', 'watch_count', 'avg_duration', 'total_duration']
        
        # Kullanıcı özelliklerini birleştir
        user_features = user_features.merge(watch_stats, on='user_id', how='left')
        
        # Film özellikleri
        movie_features = pd.DataFrame()
        movie_features['movie_id'] = movies_df['movie_id']
        movie_features['release_year'] = movies_df['release_year']
        movie_features['rating'] = movies_df['rating']
        
        # Tür özellikleri
        genre_dummies = movies_df['genre'].str.get_dummies(sep=',')
        movie_features = pd.concat([movie_features, genre_dummies], axis=1)
        
        logging.info("Özellik mühendisliği tamamlandı")
        return user_features, movie_features
    
    except Exception as e:
        logging.error(f"Özellik mühendisliği hatası: {str(e)}")
        raise

def normalize_features(user_features, movie_features):
    """Özellikleri normalizasyon yap"""
    try:
        # Kullanıcı özelliklerini normalizasyon
        user_scaler = StandardScaler()
        user_numeric_cols = ['avg_rating', 'watch_count', 'avg_duration', 'total_duration']
        user_features[user_numeric_cols] = user_scaler.fit_transform(user_features[user_numeric_cols])
        
        # Film özelliklerini normalizasyon
        movie_scaler = StandardScaler()
        movie_numeric_cols = ['release_year', 'rating']
        movie_features[movie_numeric_cols] = movie_scaler.fit_transform(movie_features[movie_numeric_cols])
        
        logging.info("Özellik normalizasyonu tamamlandı")
        return user_features, movie_features
    
    except Exception as e:
        logging.error(f"Özellik normalizasyonu hatası: {str(e)}")
        raise

def save_processed_data(user_features, movie_features):
    """İşlenmiş verileri kaydet"""
    try:
        # processed_data klasörünü oluştur
        os.makedirs('processed_data', exist_ok=True)
        
        # İşlenmiş verileri CSV olarak kaydet
        user_features.to_csv('processed_data/user_features.csv', index=False)
        movie_features.to_csv('processed_data/movie_features.csv', index=False)
        
        logging.info("İşlenmiş veriler kaydedildi")
    
    except Exception as e:
        logging.error(f"Veri kaydetme hatası: {str(e)}")
        raise

def main():
    """Ana işlem fonksiyonu"""
    try:
        logging.info("Veri işleme başlıyor...")
        
        # Verileri yükle
        users_df, movies_df, watch_history_df, preferences_df = load_data()
        
        # Verileri temizle
        users_df, movies_df, watch_history_df, preferences_df = clean_data(
            users_df, movies_df, watch_history_df, preferences_df
        )
        
        # Özellik mühendisliği
        user_features, movie_features = feature_engineering(
            users_df, movies_df, watch_history_df, preferences_df
        )
        
        # Özellikleri normalizasyon
        user_features, movie_features = normalize_features(user_features, movie_features)
        
        # İşlenmiş verileri kaydet
        save_processed_data(user_features, movie_features)
        
        logging.info("Veri işleme tamamlandı!")
    
    except Exception as e:
        logging.error(f"Veri işleme hatası: {str(e)}")
        raise

if __name__ == "__main__":
    main() 