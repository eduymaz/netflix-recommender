# 🚀 API Servisi

Bu modül, film öneri sisteminin API katmanını içerir. FastAPI kullanılarak geliştirilmiş RESTful API servisi, kullanıcı yönetimi ve film önerileri sunar.

## 📋 Endpoint'ler

### 🔐 Kullanıcı İşlemleri

- **Kayıt Olma** (`POST /api/users/register`)
  - Yeni kullanıcı oluşturma
  - Kullanıcı adı ve email benzersizlik kontrolü
  - Şifre hash'leme

- **Giriş Yapma** (`POST /api/users/login`)
  - JWT token üretme
  - Kullanıcı doğrulama

- **Kullanıcı Bilgileri** (`GET /api/users/me`)
  - Mevcut kullanıcı bilgilerini getirme

### 🎥 Film İşlemleri

- **Film Önerileri** (`GET /api/movies/recommendations`)
  - Kullanıcının izleme geçmişine göre öneriler
  - Beğenilen türlere göre filtreleme
  - Henüz izlenmemiş filmleri önerme

- **Film Puanlama** (`POST /api/movies/rate`)
  - Film izleme kaydı oluşturma
  - Puan ve izleme süresi kaydetme

- **Film Listesi** (`GET /api/movies`)
  - Tüm filmleri listeleme
  - Tür bazlı filtreleme

## 🔒 Güvenlik

- JWT tabanlı kimlik doğrulama
- Şifre hash'leme (bcrypt)
- Token süresi kontrolü

## 📊 Veritabanı İlişkileri

```
users
  ├── watch_history (1:N)
  └── user_preferences (1:1)

movies
  └── watch_history (1:N)
```

## 🛠️ Teknik Detaylar

- FastAPI framework
- SQLAlchemy ORM
- Pydantic modeller
- JWT authentication
- Swagger UI dokümantasyonu

## 📝 Loglama

- Tüm API istekleri loglanır
- Hata durumları detaylı olarak kaydedilir
- Log dosyası: `api.log`

## 🔍 Hata Yönetimi

- HTTP durum kodları
- Detaylı hata mesajları
- Kullanıcı dostu hata yanıtları

## 🚀 Performans

- Asenkron işlemler
- Veritabanı bağlantı havuzu
- Önbellek kullanımı

---

<div align="center">
  <sub>Built with ❤️ by <a href="https://github.com/eduymaz">eduymaz</a></sub>
</div> 