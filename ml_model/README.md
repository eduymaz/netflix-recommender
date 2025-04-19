# Makine Öğrenmesi Modeli

Bu modül, KMeans algoritması kullanılarak kullanıcı tercihlerine göre film önerileri yapmaktadır.

## Kullanılan Kütüphaneler
- Scikit-learn
- NumPy
- Pandas
- Matplotlib
- Seaborn

## Model Detayları

### KMeans Algoritması
- Küme sayısı: 5 (Elbow metodu ile belirlenmiştir)
- Maksimum iterasyon: 300
- Başlangıç noktası seçimi: k-means++
- Ölçüm metriği: Euclidean distance

### Özellik Vektörü
1. Kullanıcı Tercihleri
   - Favori türler
   - Tercih edilen oyuncular
   - İzleme zamanı tercihi

2. İzleme Davranışları
   - Ortalama izleme süresi
   - Puanlama alışkanlıkları
   - İzleme sıklığı

3. Demografik Bilgiler
   - Yaş
   - Cinsiyet
   - Bölge

## Model Eğitimi

1. Veri Hazırlama
   - Özellik vektörünün oluşturulması
   - Veri normalizasyonu
   - Eksik değerlerin doldurulması

2. Model Eğitimi
   - KMeans modelinin oluşturulması
   - Optimal küme sayısının belirlenmesi
   - Model parametrelerinin ayarlanması

3. Model Değerlendirmesi
   - Silhouette skoru
   - Calinski-Harabasz indeksi
   - Davies-Bouldin indeksi

## Öneri Sistemi

1. Kullanıcı Kümesi Belirleme
   - Kullanıcı özelliklerinin vektörleştirilmesi
   - En yakın kümenin belirlenmesi

2. Film Önerileri
   - Küme içindeki diğer kullanıcıların beğendiği filmler
   - Benzer özellikteki filmler
   - Popüler filmler

## Çalıştırma Talimatları

1. Gerekli kütüphaneleri yükleyin:
```bash
pip install scikit-learn numpy pandas matplotlib seaborn
```

2. Model eğitim scriptini çalıştırın:
```bash
python train_model.py
```

3. Model değerlendirme scriptini çalıştırın:
```bash
python evaluate_model.py
```

## Notlar
- Model her hafta yeniden eğitilmektedir
- Performans metrikleri düzenli olarak raporlanmaktadır
- Model parametreleri A/B testleri ile optimize edilmektedir 