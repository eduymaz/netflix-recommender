# 🔄 Veri İşleme Modülü

Bu modül, film öneri sisteminin veri işleme katmanını içerir. Ham verileri işleyerek özellik mühendisliği yapar ve makine öğrenimi modeli için hazırlar.

## 🎯 Amaç

- Ham verileri temizleme ve dönüştürme
- Özellik mühendisliği
- Veri normalizasyonu
- Model için veri hazırlama

## 📋 İşlenen Veriler

### 👥 Kullanıcı Verileri
- Kullanıcı demografik bilgileri
- İzleme alışkanlıkları
- Tercih edilen türler
- Zaman tercihleri

### 🎬 Film Verileri
- Film özellikleri
- Tür bilgileri
- Yayın yılı
- Puanlar

### 📊 İzleme Geçmişi
- İzleme süreleri
- Puanlar
- İzleme tarihleri

## 🛠️ Kullanılan Teknolojiler

- **Pandas**: Veri işleme ve analiz
- **NumPy**: Sayısal işlemler
- **Scikit-learn**: Özellik dönüşümü
- **Python 3.8+**: Programlama dili

## 🔄 İşlem Adımları

1. **Veri Temizleme**
   - Eksik değerlerin doldurulması
   - Aykırı değerlerin tespiti
   - Veri tutarlılığının kontrolü

2. **Özellik Mühendisliği**
   - Kategorik değişkenlerin kodlanması
   - Sayısal özelliklerin ölçeklendirilmesi
   - Yeni özelliklerin oluşturulması

3. **Veri Dönüşümü**
   - One-hot encoding
   - Min-max normalizasyon
   - Standart skaler

4. **Veri Hazırlama**
   - Eğitim/test ayrımı
   - Cross-validation
   - Veri dengesizliğinin giderilmesi

## 📈 Özellik Vektörü

```
Kullanıcı Özellikleri:
- Yaş
- Cinsiyet
- İzleme sıklığı
- Tercih edilen türler
- Ortalama izleme süresi

Film Özellikleri:
- Tür
- Yayın yılı
- Süre
- Oyuncular
- Yönetmen
```

## 📊 İstatistikler

- Toplam özellik sayısı: 20
- Kategorik özellikler: 8
- Sayısal özellikler: 12
- Boyut azaltma oranı: %30

## 🚀 Çalıştırma

```bash
python process_data.py
```

## 📝 Çıktılar

- İşlenmiş veri seti
- Özellik vektörleri
- Normalizasyon parametreleri
- İşlem logları

## 🔍 Doğrulama

- Veri kalitesi kontrolü
- Özellik korelasyonu
- Varyans analizi
- Cross-validation sonuçları

---

<div align="center">
  <sub>Built with ❤️ by <a href="https://github.com/eduymaz">eduymaz</a></sub>
</div> 