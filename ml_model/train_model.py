import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import seaborn as sns
import logging
import joblib
from pathlib import Path

# Logging ayarları
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='model_training.log'
)

def load_data():
    """İşlenmiş verileri yükle"""
    try:
        user_features = pd.read_csv('processed_data/user_features.csv')
        movie_features = pd.read_csv('processed_data/movie_features.csv')
        logging.info("Veriler başarıyla yüklendi")
        return user_features, movie_features
    except Exception as e:
        logging.error(f"Veri yükleme hatası: {str(e)}")
        raise

def find_optimal_clusters(X, max_clusters=10):
    """Optimal küme sayısını bul"""
    try:
        silhouette_scores = []
        for n_clusters in range(2, max_clusters + 1):
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            cluster_labels = kmeans.fit_predict(X)
            silhouette_avg = silhouette_score(X, cluster_labels)
            silhouette_scores.append(silhouette_avg)
            logging.info(f"Küme sayısı: {n_clusters}, Silhouette skoru: {silhouette_avg:.4f}")
        
        # En iyi küme sayısını bul
        optimal_clusters = np.argmax(silhouette_scores) + 2
        logging.info(f"Optimal küme sayısı: {optimal_clusters}")
        
        # Silhouette skorlarını görselleştir
        plt.figure(figsize=(10, 6))
        plt.plot(range(2, max_clusters + 1), silhouette_scores, marker='o')
        plt.title('Silhouette Skorları')
        plt.xlabel('Küme Sayısı')
        plt.ylabel('Silhouette Skoru')
        plt.savefig('model_results/silhouette_scores.png')
        plt.close()
        
        return optimal_clusters
    
    except Exception as e:
        logging.error(f"Optimal küme bulma hatası: {str(e)}")
        raise

def train_kmeans(X, n_clusters):
    """KMeans modelini eğit"""
    try:
        kmeans = KMeans(
            n_clusters=n_clusters,
            init='k-means++',
            max_iter=300,
            random_state=42
        )
        
        # Modeli eğit
        kmeans.fit(X)
        logging.info("KMeans modeli eğitildi")
        
        return kmeans
    
    except Exception as e:
        logging.error(f"Model eğitimi hatası: {str(e)}")
        raise

def analyze_clusters(X, kmeans, user_features):
    """Kümeleri analiz et"""
    try:
        # Kümeleri tahmin et
        cluster_labels = kmeans.predict(X)
        
        # Kümelerin özelliklerini analiz et
        cluster_analysis = pd.DataFrame(X)
        cluster_analysis['cluster'] = cluster_labels
        cluster_analysis['user_id'] = user_features['user_id']
        
        # Her küme için ortalama özellikler
        cluster_stats = cluster_analysis.groupby('cluster').mean()
        
        # Kümeleri görselleştir
        plt.figure(figsize=(12, 8))
        sns.heatmap(cluster_stats, annot=True, cmap='YlGnBu')
        plt.title('Küme Özellikleri')
        plt.savefig('model_results/cluster_features.png')
        plt.close()
        
        logging.info("Küme analizi tamamlandı")
        return cluster_analysis
    
    except Exception as e:
        logging.error(f"Küme analizi hatası: {str(e)}")
        raise

def save_model(model, cluster_analysis):
    """Modeli ve analiz sonuçlarını kaydet"""
    try:
        # Modeli kaydet
        joblib.dump(model, 'model_results/kmeans_model.pkl')
        
        # Küme analizini kaydet
        cluster_analysis.to_csv('model_results/cluster_analysis.csv', index=False)
        
        logging.info("Model ve analiz sonuçları kaydedildi")
    
    except Exception as e:
        logging.error(f"Model kaydetme hatası: {str(e)}")
        raise

def main():
    """Ana işlem fonksiyonu"""
    try:
        # Gerekli klasörleri oluştur
        Path('model_results').mkdir(exist_ok=True)
        
        logging.info("Model eğitimi başlıyor...")
        
        # Verileri yükle
        user_features, movie_features = load_data()
        
        # Kullanıcı özelliklerini hazırla
        X = user_features.drop(['user_id'], axis=1)
        
        # Optimal küme sayısını bul
        optimal_clusters = find_optimal_clusters(X)
        
        # Modeli eğit
        kmeans = train_kmeans(X, optimal_clusters)
        
        # Kümeleri analiz et
        cluster_analysis = analyze_clusters(X, kmeans, user_features)
        
        # Modeli ve analiz sonuçlarını kaydet
        save_model(kmeans, cluster_analysis)
        
        logging.info("Model eğitimi tamamlandı!")
    
    except Exception as e:
        logging.error(f"Model eğitimi hatası: {str(e)}")
        raise

if __name__ == "__main__":
    main() 