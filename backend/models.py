# backend/models.py
from flask_sqlalchemy import SQLAlchemy  
from datetime import datetime

db = SQLAlchemy()

# 1. USERS TABLE
class User(db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    full_name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    language_pref = db.Column(db.String(10), default='en')
    
    # Relationships
    histories = db.relationship('History', backref='user', lazy=True, cascade='all, delete-orphan')
    feedbacks = db.relationship('Feedback', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'language_pref': self.language_pref
        }


# 2. SOIL_TYPE TABLE (Reference)
class SoilType(db.Model):
    __tablename__ = 'soil_type'
    
    soil_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    description = db.Column(db.Text)
    npk_profile = db.Column(db.String(50))
    ph_range = db.Column(db.String(20))
    best_crops = db.Column(db.Text)
    improvements = db.Column(db.Text)
    
    # Relationships
    crops = db.relationship('Crop', backref='soil', lazy=True)
    
    def to_dict(self):
        return {
            'soil_id': self.soil_id,
            'name': self.name,
            'description': self.description,
            'npk_profile': self.npk_profile,
            'ph_range': self.ph_range,
            'best_crops': self.best_crops,
            'improvements': self.improvements
        }


# 3. CROP TABLE (Master Table)
class Crop(db.Model):
    __tablename__ = 'crop'
    
    crop_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    icon = db.Column(db.String(10))
    season = db.Column(db.String(10), nullable=False)
    soil_id = db.Column(db.Integer, db.ForeignKey('soil_type.soil_id'), nullable=False)
    min_temp = db.Column(db.Integer, nullable=False)
    max_temp = db.Column(db.Integer, nullable=False)
    min_rain = db.Column(db.Integer, nullable=False)
    max_rain = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, default=0)
    fertilizer = db.Column(db.Text)
    npk_N = db.Column(db.Integer, default=50)
    npk_P = db.Column(db.Integer, default=30)
    npk_K = db.Column(db.Integer, default=30)
    
    # Relationships
    recommendations = db.relationship('Recommendation', backref='crop', lazy=True)
    details = db.relationship('CropDetails', backref='crop', uselist=False, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'crop_id': self.crop_id,
            'name': self.name,
            'icon': self.icon,
            'season': self.season,
            'soil_id': self.soil_id,
            'min_temp': self.min_temp,
            'max_temp': self.max_temp,
            'min_rain': self.min_rain,
            'max_rain': self.max_rain,
            'price': self.price,
            'fertilizer': self.fertilizer,
            'npk_N': self.npk_N,
            'npk_P': self.npk_P,
            'npk_K': self.npk_K
        }


# 4. CROP_DETAILS TABLE
class CropDetails(db.Model):
    __tablename__ = 'crop_details'
    
    detail_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    crop_id = db.Column(db.Integer, db.ForeignKey('crop.crop_id'), unique=True, nullable=False)
    varieties = db.Column(db.Text)
    diseases = db.Column(db.Text)
    pests = db.Column(db.Text)
    fertilizer_schedule = db.Column(db.Text)
    irrigation_method = db.Column(db.Text)
    harvesting_time = db.Column(db.String(50))
    storage_method = db.Column(db.Text)
    
    def to_dict(self):
        return {
            'detail_id': self.detail_id,
            'crop_id': self.crop_id,
            'varieties': self.varieties,
            'diseases': self.diseases,
            'pests': self.pests,
            'fertilizer_schedule': self.fertilizer_schedule,
            'irrigation_method': self.irrigation_method,
            'harvesting_time': self.harvesting_time,
            'storage_method': self.storage_method
        }


# 5. HISTORY TABLE
class History(db.Model):
    __tablename__ = 'history'
    
    history_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    soil_type = db.Column(db.String(30), nullable=False)
    temperature = db.Column(db.Float)
    rainfall = db.Column(db.Float)
    N_value = db.Column(db.Integer)
    P_value = db.Column(db.Integer)
    K_value = db.Column(db.Integer)
    ph_value = db.Column(db.Float)
    humidity = db.Column(db.Integer)
    top_crop_1 = db.Column(db.String(50), nullable=False)
    top_crop_2 = db.Column(db.String(50))
    top_crop_3 = db.Column(db.String(50))
    
    # Relationships
    recommendations = db.relationship('Recommendation', backref='history', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'history_id': self.history_id,
            'user_id': self.user_id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'soil_type': self.soil_type,
            'temperature': self.temperature,
            'rainfall': self.rainfall,
            'N_value': self.N_value,
            'P_value': self.P_value,
            'K_value': self.K_value,
            'ph_value': self.ph_value,
            'humidity': self.humidity,
            'top_crop_1': self.top_crop_1,
            'top_crop_2': self.top_crop_2,
            'top_crop_3': self.top_crop_3,
            'recommendations': [r.to_dict() for r in self.recommendations]
        }


# 6. RECOMMENDATION TABLE
class Recommendation(db.Model):
    __tablename__ = 'recommendation'
    
    rec_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    history_id = db.Column(db.Integer, db.ForeignKey('history.history_id'), nullable=False)
    crop_id = db.Column(db.Integer, db.ForeignKey('crop.crop_id'), nullable=False)
    rank = db.Column(db.Integer, nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    price_at_time = db.Column(db.Integer, default=0)
    
    def to_dict(self):
        return {
            'rec_id': self.rec_id,
            'history_id': self.history_id,
            'crop_id': self.crop_id,
            'crop_name': self.crop.name if self.crop else None,
            'rank': self.rank,
            'confidence': self.confidence,
            'price_at_time': self.price_at_time
        }


# 7. FEEDBACK TABLE
class Feedback(db.Model):
    __tablename__ = 'feedback'
    
    feedback_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')
    
    def to_dict(self):
        return {
            'feedback_id': self.feedback_id,
            'user_id': self.user_id,
            'rating': self.rating,
            'comment': self.comment,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'status': self.status
        }