# 📊 Veri Üretimi

Bu modül, film öneri sistemi için örnek veriler oluşturur. Faker kütüphanesi kullanılarak gerçekçi kullanıcı, film ve izleme geçmişi verileri üretilir.

## 🎯 Amaç

- Örnek kullanıcı verileri oluşturma
- Örnek film verileri oluşturma
- İzleme geçmişi ve puan verileri üretme
- Sistem testi için gerçekçi veri seti hazırlama

## 📋 Üretilen Veriler

### 👥 Kullanıcılar
- 50 adet örnek kullanıcı
- Benzersiz kullanıcı adları
- Gerçekçi email adresleri
- Güvenli şifre hash'leri

### 🎬 Filmler
- 100 adet örnek film
- Gerçekçi film başlıkları
- Çeşitli türlerde filmler
- Farklı yıllarda yayınlanmış filmler

### 📝 İzleme Geçmişi
- Her kullanıcı için 5-10 izleme kaydı
- 1-5 arası puanlar
- 30-180 dakika arası izleme süreleri
- Rastgele izleme tarihleri

## 🛠️ Kullanılan Teknolojiler

- Faker (Türkçe veri üretimi)
- SQLAlchemy (Veritabanı işlemleri)
- PostgreSQL (Veritabanı)
- Python 3.8+

## 📊 Veri Yapısı

```
users
  ├── user_id (PK)
  ├── username
  ├── email
  ├── password_hash
  └── created_at

movies
  ├── movie_id (PK)
  ├── title
  ├── genre
  ├── release_year
  ├── rating
  └── description

watch_history
  ├── history_id (PK)
  ├── user_id (FK)
  ├── movie_id (FK)
  ├── watch_date
  ├── rating
  └── watch_duration
```

## 🚀 Çalıştırma

```bash
python generate_data.py
```

## 📝 Çıktılar

- Veritabanı tabloları oluşturulur
- Örnek veriler eklenir
- İşlem logları konsola yazdırılır

## 🔍 Doğrulama

- Benzersizlik kontrolleri
- Veri bütünlüğü kontrolleri
- İlişkisel bütünlük kontrolleri

## 📈 İstatistikler

- Toplam kullanıcı sayısı: 50
- Toplam film sayısı: 100
- Toplam izleme kaydı: ~300-500
- Ortalama izleme süresi: 90 dakika

---

<div align="center">
  <sub>Built with ❤️ by <a href="https://github.com/eduymaz">eduymaz</a></sub>
</div> 