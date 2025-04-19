# 🗄️ Veritabanı Modülü

Bu modül, film öneri sisteminin veritabanı katmanını içerir. SQLAlchemy ORM kullanılarak PostgreSQL veritabanı ile etkileşim sağlanır.

## 📊 Veritabanı Şeması

### 👥 Users Tablosu
```sql
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);
```

### 🎬 Movies Tablosu
```sql
CREATE TABLE movies (
    movie_id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    genre VARCHAR(100),
    release_year INTEGER,
    rating FLOAT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 📝 WatchHistory Tablosu
```sql
CREATE TABLE watch_history (
    history_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    movie_id INTEGER REFERENCES movies(movie_id),
    watch_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    rating INTEGER,
    watch_duration INTEGER
);
```

### ⭐ UserPreferences Tablosu
```sql
CREATE TABLE user_preferences (
    preference_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    favorite_genres VARCHAR(200),
    preferred_actors VARCHAR(200),
    watch_time_preference VARCHAR(20)
);
```

## 🔗 İlişkiler

```
users (1) ──── (N) watch_history
  │
  └── (1) ──── (1) user_preferences

movies (1) ──── (N) watch_history
```

## 🛠️ Teknik Detaylar

- **ORM**: SQLAlchemy
- **Veritabanı**: PostgreSQL
- **Bağlantı Havuzu**: SQLAlchemy Pool
- **Migration**: Alembic

## 🔒 Güvenlik

- Şifre hash'leme (bcrypt)
- SQL injection koruması
- Bağlantı şifreleme (SSL)

## 📈 Performans

- İndeksler
- Bağlantı havuzu
- Sorgu optimizasyonu

## 📝 Sorgu Örnekleri

### Kullanıcı İzleme Geçmişi
```sql
SELECT m.title, wh.rating, wh.watch_date
FROM watch_history wh
JOIN movies m ON wh.movie_id = m.movie_id
WHERE wh.user_id = :user_id
ORDER BY wh.watch_date DESC;
```

### Film Önerileri
```sql
SELECT m.*
FROM movies m
JOIN watch_history wh ON m.movie_id = wh.movie_id
WHERE wh.user_id IN (
    SELECT user_id
    FROM watch_history
    WHERE movie_id IN (
        SELECT movie_id
        FROM watch_history
        WHERE user_id = :user_id
        AND rating >= 4
    )
    AND rating >= 4
)
AND m.movie_id NOT IN (
    SELECT movie_id
    FROM watch_history
    WHERE user_id = :user_id
)
GROUP BY m.movie_id
ORDER BY AVG(wh.rating) DESC
LIMIT 10;
```

## 🚀 Bağlantı Ayarları

```python
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost:5432/netflix_recommender"
```

## 📊 İstatistikler

- Tablo sayısı: 4
- İlişki sayısı: 3
- Toplam indeks: 6
- Ortalama sorgu süresi: < 100ms

---

<div align="center">
  <sub>Built with ❤️ by <a href="https://github.com/eduymaz">eduymaz</a></sub>
</div> 