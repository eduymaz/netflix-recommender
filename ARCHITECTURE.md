# 🏗️ Film Recommendation System Architecture

## 📋 Overview

This document outlines the architecture of our Film Recommendation System, which is built using modern technologies and follows best practices in software development.

## 🎯 System Components

### 1. Data Generation (`data_generation/`)
- Generates sample user, movie, and viewing data
- Uses Faker library for realistic data generation
- Creates initial database schema and populates tables

### 2. Data Processing (`data_processing/`)
- Processes raw data and performs feature engineering
- Handles data cleaning and normalization
- Prepares data for machine learning model

### 3. Machine Learning Model (`ml_model/`)
- Implements KMeans clustering algorithm
- Trains model on user preferences and viewing history
- Generates personalized movie recommendations

### 4. API Layer (`api/`)
- FastAPI-based RESTful API service
- Handles user authentication and authorization
- Provides endpoints for recommendations and user management

### 5. Database Layer (`database/`)
- PostgreSQL database with SQLAlchemy ORM
- Manages data persistence and relationships
- Implements efficient querying and indexing

## 🔄 Data Flow

```
User Request → API Layer → Database Layer → ML Model → Recommendations
```

## 🛠️ Technology Stack

- **Backend**: Python 3.12+
- **API Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **ML Library**: Scikit-learn
- **Authentication**: JWT
- **Data Processing**: Pandas, NumPy

## 📊 Database Schema

### Users Table
```sql
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Movies Table
```sql
CREATE TABLE movies (
    movie_id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    genre VARCHAR(100),
    release_year INTEGER,
    rating FLOAT,
    description TEXT
);
```

### Watch History Table
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

## 🔒 Security Measures

- JWT-based authentication
- Password hashing with bcrypt
- SQL injection protection
- Input validation
- Rate limiting

## 📈 Performance Considerations

- Database indexing
- Connection pooling
- Caching strategies
- Asynchronous processing
- Query optimization

## 🚀 Deployment Architecture

```
[Load Balancer]
      ↓
[API Servers] → [Database Cluster]
      ↓
[ML Model Servers]
```

## 📝 API Endpoints

### User Management
- `POST /api/users/register` - User registration
- `POST /api/users/login` - User authentication
- `GET /api/users/me` - User profile

### Movie Operations
- `GET /api/movies/recommendations` - Get recommendations
- `POST /api/movies/rate` - Rate a movie
- `GET /api/movies` - List movies

## 🔍 Monitoring and Logging

- Application logs
- Performance metrics
- Error tracking
- User activity monitoring

## 📊 System Requirements

- Python 3.8+
- PostgreSQL 12+
- 4GB RAM minimum
- 20GB disk space
- Network connectivity

## 🚀 Getting Started

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up database:
```bash
python data_generation/generate_data.py
```

3. Process data:
```bash
python data_processing/process_data.py
```

4. Train model:
```bash
python ml_model/train_model.py
```

5. Start API:
```bash
python api/main.py
```

## 📈 Future Enhancements

- Real-time recommendations
- A/B testing framework
- Advanced ML models
- Microservices architecture
- Containerization with Docker

---

<div align="center">
  <sub>Built with ❤️ by <a href="https://github.com/eduymaz">eduymaz</a></sub>
</div> 