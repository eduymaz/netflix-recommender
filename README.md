# 🎬 Netflix Benzeri Film Öneri Sistemi

Bu proje, kullanıcıların izleme geçmişlerine ve tercihlerine göre film önerileri sunan bir API servisidir. Kullanıcıların beğendiği film türlerini analiz ederek, henüz izlemedikleri benzer filmleri önermektedir.


## 🚀 Özellikler

- 📝 Kullanıcı kaydı ve girişi
- 🎥 Film izleme geçmişi takibi
- ⭐ Film puanlama sistemi
- 🎯 Kişiselleştirilmiş film önerileri
- 🔒 JWT tabanlı güvenlik
- 📊 PostgreSQL veritabanı entegrasyonu
- 📚 Swagger UI ile API dokümantasyonu

## 🛠️ Teknolojiler

- Python 3.8+
- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT Authentication
- Pydantic
- Swagger UI

## 📦 Kurulum

1. Repoyu klonlayın:
```bash
git clone https://github.com/eduymaz/netflix-recommender.git
cd netflix-recommender
```

2. Sanal ortam oluşturun ve aktifleştirin:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
.\venv\Scripts\activate  # Windows
```

3. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

4. PostgreSQL veritabanını oluşturun:
```bash
psql -U postgres -c "CREATE DATABASE netflix_recommender;"
```

## 🚀 Çalıştırma

1. Örnek verileri oluşturun:
```bash
python data_generation/generate_data.py
```

2. API'yi başlatın:
```bash
python api/main.py
```

3. Swagger UI'a erişin:
```
http://localhost:8001/docs
```

## 📝 API Kullanımı

### Kullanıcı İşlemleri

- **Kayıt Olma**
  - Endpoint: `POST /api/users/register`
  - Body:
  ```json
  {
    "username": "kullanici_adi",
    "email": "email@example.com",
    "password": "sifre"
  }
  ```

- **Giriş Yapma**
  - Endpoint: `POST /api/users/login`
  - Body:
  ```json
  {
    "username": "kullanici_adi",
    "password": "sifre"
  }
  ```

### Film İşlemleri

- **Film Önerileri**
  - Endpoint: `GET /api/movies/recommendations`
  - Header: `Authorization: Bearer <token>`

- **Film Puanlama**
  - Endpoint: `POST /api/movies/rate`
  - Body:
  ```json
  {
    "movie_id": 1,
    "rating": 5,
    "watch_duration": 120
  }
  ```

## 🧩 Sistem Mimarisi

```
📁 netflix-recommender/
├── 📁 api/
│   ├── 📄 main.py           # FastAPI uygulaması
│   └── 📄 README.md         # API dokümantasyonu
├── 📁 data_generation/
│   ├── 📄 generate_data.py  # Örnek veri oluşturma
│   └── 📄 README.md         # Veri oluşturma açıklaması
├── 📁 database/
│   ├── 📄 database.py       # Veritabanı modelleri
│   └── 📄 README.md         # Veritabanı şeması
├── 📁 ml_model/
│   ├── 📄 train_model.py    # Model eğitimi
│   └── 📄 README.md         # Model açıklaması
├── 📄 requirements.txt      # Bağımlılıklar
└── 📄 README.md            # Proje açıklaması
```


## 📞 İletişim

Sorularınız veya önerileriniz için:
- 📧 Email: duyymazelif@gmail.com
- 💬 GitHub Issues

---

<div align="center">
  <sub>Built with ❤️ by <a href="https://github.com/eduymaz">eduymaz</a></sub>
</div> 
