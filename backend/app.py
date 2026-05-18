# backend/app.py
from flask import Flask, request, jsonify, send_from_directory, session
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, User, SoilType, Crop, CropDetails, History, Recommendation, Feedback
import joblib
import numpy as np
import os
from flask_mail import Mail, Message
from dotenv import load_dotenv
import subprocess
from datetime import datetime
import bcrypt

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app, supports_credentials=True)

load_dotenv()

# ============================================
# DATABASE CONFIGURATION
# ============================================
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'cropsense.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here-change-in-production')

# Initialize database
db.init_app(app)
migrate = Migrate(app, db)

# Create tables (run once)
with app.app_context():
    db.create_all()
    print("✅ Database tables created")

# ============================================
# EMAIL CONFIGURATION
# ============================================
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', 'no-reply@cropsense.in')
app.config['MAIL_RECIPIENTS'] = os.getenv('MAIL_RECIPIENTS', 'support@cropsense.in').split(',')

if not app.config['MAIL_USERNAME'] or app.config['MAIL_USERNAME'] == 'your-email@gmail.com':
    app.config['TESTING'] = True
    print("ℹ️ Email disabled (no .env creds). Set MAIL_USERNAME/PASSWORD for contact form.")

mail = Mail(app)

# ============================================
# ML MODEL LOADING
# ============================================
model = None

def get_model():
    global model
    if model is None:
        model_path = 'crop_model.pkl'
        joblib_path = 'crop_model.joblib'
        
        if os.path.exists(joblib_path):
            try:
                model = joblib.load(joblib_path)
                print("✅ Model loaded from joblib")
                return model
            except:
                pass
        
        if not os.path.exists(model_path):
            print("🔄 Auto-training model...")
            subprocess.check_call(['python', 'model.py'])
        
        try:
            model = joblib.load(model_path)
            print("✅ Model loaded successfully")
            try:
                joblib.dump(model, joblib_path)
                print("💾 Saved as joblib format")
            except:
                pass
        except Exception as e:
            print(f"❌ Model load failed: {e}")
            model = None
    return model

# ============================================
# FRONTEND ROUTES
# ============================================

@app.route('/')
def serve_index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def serve_frontend(path):
    frontend_path = os.path.join('../frontend', path)
    if os.path.exists(frontend_path):
        return send_from_directory('../frontend', path)
    if not path.endswith('.html'):
        html_path = path + '.html'
        if os.path.exists(os.path.join('../frontend', html_path)):
            return send_from_directory('../frontend', html_path)
    return send_from_directory('../frontend', 'index.html')

# ============================================
# CROP INFORMATION DATABASE (In-memory)
# ============================================

CROP_INFO = {
    'rice': {'icon': '🌾', 'season': 'Kharif', 'soil': 'Clay/Alluvial', 'fert': 'Urea 100kg/ha, DAP 50kg/ha', 'price': 4024, 'min_temp': 20, 'max_temp': 35, 'min_rain': 1000, 'max_rain': 2500},
    'wheat': {'icon': '🌿', 'season': 'Rabi', 'soil': 'Loamy', 'fert': 'Urea 120kg/ha, DAP 60kg/ha', 'price': 2164, 'min_temp': 10, 'max_temp': 25, 'min_rain': 300, 'max_rain': 1000},
    'maize': {'icon': '🌽', 'season': 'Kharif', 'soil': 'Loamy/Sandy', 'fert': 'Urea 120kg/ha, DAP 60kg/ha', 'price': 1700, 'min_temp': 18, 'max_temp': 32, 'min_rain': 500, 'max_rain': 1200},
    'potato': {'icon': '🥔', 'season': 'Rabi', 'soil': 'Loamy', 'fert': 'Urea 120kg/ha, DAP 80kg/ha', 'price': 1240, 'min_temp': 15, 'max_temp': 25, 'min_rain': 500, 'max_rain': 1000},
    'tomato': {'icon': '🍅', 'season': 'Zaid/Kharif/Rabi', 'soil': 'Loamy', 'fert': 'Urea 120kg/ha, DAP 80kg/ha', 'price': 1848, 'min_temp': 18, 'max_temp': 27, 'min_rain': 400, 'max_rain': 800},
    'onion': {'icon': '🧅', 'season': 'Rabi', 'soil': 'Loamy', 'fert': 'Urea 100kg/ha, DAP 50kg/ha', 'price': 1728, 'min_temp': 12, 'max_temp': 28, 'min_rain': 350, 'max_rain': 700},
    'cotton': {'icon': '🌸', 'season': 'Kharif', 'soil': 'Black cotton', 'fert': 'Urea 100kg/ha, DAP 50kg/ha', 'price': 7767, 'min_temp': 20, 'max_temp': 40, 'min_rain': 500, 'max_rain': 1000},
    'sugarcane': {'icon': '🎋', 'season': 'Zaid', 'soil': 'Loamy', 'fert': 'Urea 250kg/ha, DAP 100kg/ha', 'price': 205, 'min_temp': 20, 'max_temp': 35, 'min_rain': 1000, 'max_rain': 2000},
    'tea': {'icon': '🍵', 'season': 'Zaid', 'soil': 'Acidic/Sandy', 'fert': 'Urea 60kg/ha, DAP 30kg/ha', 'price': 27000, 'min_temp': 13, 'max_temp': 32, 'min_rain': 1500, 'max_rain': 2500},
    'coffee': {'icon': '☕', 'season': 'Zaid', 'soil': 'Volcanic/Acidic', 'fert': 'Urea 80kg/ha, DAP 40kg/ha', 'price': 20200, 'min_temp': 15, 'max_temp': 28, 'min_rain': 1500, 'max_rain': 2400},
    'groundnut': {'icon': '🥜', 'season': 'Kharif', 'soil': 'Sandy', 'fert': 'Urea 20kg/ha, DAP 60kg/ha', 'price': 6619, 'min_temp': 25, 'max_temp': 35, 'min_rain': 500, 'max_rain': 800},
    'soybean': {'icon': '🫘', 'season': 'Kharif', 'soil': 'Loamy', 'fert': 'Urea 30kg/ha, DAP 60kg/ha', 'price': 5423, 'min_temp': 20, 'max_temp': 30, 'min_rain': 500, 'max_rain': 1000},
    'pulse': {'icon': '🫛', 'season': 'Rabi', 'soil': 'Clay/Loamy', 'fert': 'Urea 25kg/ha, DAP 50kg/ha', 'price': 6000, 'min_temp': 20, 'max_temp': 30, 'min_rain': 300, 'max_rain': 600},
    'millets': {'icon': '🌾', 'season': 'Kharif', 'soil': 'Loamy/Sandy', 'fert': 'Urea 40kg/ha, DAP 40kg/ha', 'price': 3100, 'min_temp': 25, 'max_temp': 40, 'min_rain': 300, 'max_rain': 800},
    'jute': {'icon': '🌿', 'season': 'Kharif', 'soil': 'Loamy', 'fert': 'Urea 60kg/ha, DAP 30kg/ha', 'price': 11300, 'min_temp': 24, 'max_temp': 37, 'min_rain': 1000, 'max_rain': 2000},
    'mustard': {'icon': '🌼', 'season': 'Rabi', 'soil': 'Loamy', 'fert': 'Urea 60kg/ha, DAP 40kg/ha', 'price': 6076, 'min_temp': 10, 'max_temp': 25, 'min_rain': 300, 'max_rain': 600},
    'banana': {'icon': '🍌', 'season': 'Zaid', 'soil': 'Loamy', 'fert': 'Urea 200kg/ha, DAP 100kg/ha', 'price': 3639, 'min_temp': 25, 'max_temp': 35, 'min_rain': 1000, 'max_rain': 2500},
    'turmeric': {'icon': '🟡', 'season': 'Kharif', 'soil': 'Loamy', 'fert': 'Urea 80kg/ha, DAP 50kg/ha', 'price': 10424, 'min_temp': 20, 'max_temp': 35, 'min_rain': 1500, 'max_rain': 2500},
    'sunflower': {'icon': '🌻', 'season': 'Rabi', 'soil': 'Clay/Sandy', 'fert': 'Urea 60kg/ha, DAP 40kg/ha', 'price': 7500, 'min_temp': 20, 'max_temp': 35, 'min_rain': 400, 'max_rain': 800},
    'sesame': {'icon': '🌱', 'season': 'Kharif', 'soil': 'Sandy loam', 'fert': 'Urea 40kg/ha, DAP 40kg/ha', 'price': 9316, 'min_temp': 25, 'max_temp': 35, 'min_rain': 400, 'max_rain': 800},
    'apple': {'icon': '🍎', 'season': 'Rabi', 'soil': 'Loamy', 'fert': 'Urea 120kg/ha, DAP 80kg/ha', 'price': 12871, 'min_temp': 15, 'max_temp': 25, 'min_rain': 700, 'max_rain': 1200},
    'papaya': {'icon': '🍈', 'season': 'Zaid', 'soil': 'Loamy', 'fert': 'Urea 150kg/ha, DAP 80kg/ha', 'price': 3087, 'min_temp': 22, 'max_temp': 32, 'min_rain': 1000, 'max_rain': 2000},
    'guava': {'icon': '🍐', 'season': 'Zaid', 'soil': 'Sandy/Loamy', 'fert': 'Urea 100kg/ha, DAP 50kg/ha', 'price': 5290, 'min_temp': 20, 'max_temp': 30, 'min_rain': 800, 'max_rain': 1500},
    'watermelon': {'icon': '🍉', 'season': 'Zaid', 'soil': 'Sandy', 'fert': 'Urea 80kg/ha, DAP 50kg/ha', 'price': 1526, 'min_temp': 21, 'max_temp': 35, 'min_rain': 300, 'max_rain': 600},
    'cucumber': {'icon': '🥒', 'season': 'Zaid', 'soil': 'Loamy', 'fert': 'Urea 100kg/ha, DAP 50kg/ha', 'price': 2250, 'min_temp': 21, 'max_temp': 30, 'min_rain': 400, 'max_rain': 800},
    'pumpkin': {'icon': '🎃', 'season': 'Kharif', 'soil': 'Loamy', 'fert': 'Urea 100kg/ha, DAP 60kg/ha', 'price': 1580, 'min_temp': 18, 'max_temp': 35, 'min_rain': 400, 'max_rain': 800},
    'brinjal': {'icon': '🍆', 'season': 'Zaid', 'soil': 'Sandy/Loamy', 'fert': 'Urea 100kg/ha, DAP 60kg/ha', 'price': 2660, 'min_temp': 21, 'max_temp': 32, 'min_rain': 400, 'max_rain': 800},
    'cabbage': {'icon': '🥬', 'season': 'Rabi', 'soil': 'Loamy', 'fert': 'Urea 120kg/ha, DAP 60kg/ha', 'price': 1631, 'min_temp': 15, 'max_temp': 21, 'min_rain': 400, 'max_rain': 800},
    'cauliflower': {'icon': '🥦', 'season': 'Rabi', 'soil': 'Sandy/Loamy', 'fert': 'Urea 120kg/ha, DAP 60kg/ha', 'price': 2572, 'min_temp': 15, 'max_temp': 21, 'min_rain': 400, 'max_rain': 800},
    'spinach': {'icon': '🌿', 'season': 'Rabi', 'soil': 'Loamy', 'fert': 'Urea 80kg/ha, DAP 50kg/ha', 'price': 1280, 'min_temp': 10, 'max_temp': 24, 'min_rain': 300, 'max_rain': 600},
    'carrot': {'icon': '🥕', 'season': 'Rabi', 'soil': 'Sandy/Loamy', 'fert': 'Urea 100kg/ha, DAP 60kg/ha', 'price': 3294, 'min_temp': 15, 'max_temp': 25, 'min_rain': 300, 'max_rain': 600},
    'beetroot': {'icon': '🟣', 'season': 'Rabi', 'soil': 'Loamy', 'fert': 'Urea 100kg/ha, DAP 60kg/ha', 'price': 3584, 'min_temp': 15, 'max_temp': 25, 'min_rain': 300, 'max_rain': 600},
    'radish': {'icon': '⚪', 'season': 'Rabi', 'soil': 'Sandy', 'fert': 'Urea 100kg/ha, DAP 50kg/ha', 'price': 2321, 'min_temp': 15, 'max_temp': 25, 'min_rain': 300, 'max_rain': 600},
    'peas': {'icon': '🟢', 'season': 'Rabi', 'soil': 'Loamy', 'fert': 'Urea 60kg/ha, DAP 40kg/ha', 'price': 5168, 'min_temp': 10, 'max_temp': 25, 'min_rain': 300, 'max_rain': 600},
    'lentil': {'icon': '🫘', 'season': 'Rabi', 'soil': 'Loamy', 'fert': 'Urea 40kg/ha, DAP 30kg/ha', 'price': 6505, 'min_temp': 15, 'max_temp': 21, 'min_rain': 300, 'max_rain': 600},
    'blackgram': {'icon': '⚫', 'season': 'Kharif', 'soil': 'Sandy loam', 'fert': 'Urea 30kg/ha, DAP 20kg/ha', 'price': 7132, 'min_temp': 25, 'max_temp': 35, 'min_rain': 400, 'max_rain': 800},
    'greengram': {'icon': '🟢', 'season': 'Kharif', 'soil': 'Sandy loam', 'fert': 'Urea 25kg/ha, DAP 20kg/ha', 'price': 2828, 'min_temp': 25, 'max_temp': 35, 'min_rain': 400, 'max_rain': 800},
    'ragi': {'icon': '🌾', 'season': 'Kharif', 'soil': 'Red/Loamy', 'fert': 'Urea 40kg/ha, DAP 40kg/ha', 'price': 3934, 'min_temp': 20, 'max_temp': 35, 'min_rain': 500, 'max_rain': 1000},
    'coriander': {'icon': '🌿', 'season': 'Rabi', 'soil': 'Loamy', 'fert': 'Urea 60kg/ha, DAP 40kg/ha', 'price': 9569, 'min_temp': 15, 'max_temp': 25, 'min_rain': 400, 'max_rain': 800},
    'cumin': {'icon': '🌱', 'season': 'Rabi', 'soil': 'Sandy Loam', 'fert': 'Urea 60kg/ha, DAP 40kg/ha', 'price': 7639, 'min_temp': 15, 'max_temp': 25, 'min_rain': 300, 'max_rain': 600},
    'strawberry': {'icon': '🍓', 'season': 'Rabi', 'soil': 'Acidic/Loamy', 'fert': 'Urea 60kg/ha, DAP 40kg/ha', 'price': 19000, 'min_temp': 15, 'max_temp': 26, 'min_rain': 600, 'max_rain': 1000},
    'custardapple': {'icon': '🍏', 'season': 'Zaid', 'soil': 'Loamy', 'fert': 'Urea 100kg/ha, DAP 50kg/ha', 'price': 5200, 'min_temp': 20, 'max_temp': 35, 'min_rain': 500, 'max_rain': 1000},
    'lemon': {'icon': '🍋', 'season': 'Zaid', 'soil': 'Loamy', 'fert': 'Urea 80kg/ha, DAP 50kg/ha', 'price': 12845, 'min_temp': 20, 'max_temp': 38, 'min_rain': 600, 'max_rain': 1200},
    'bottlegourd': {'icon': '🎃', 'season': 'Zaid', 'soil': 'Loamy', 'fert': 'Urea 100kg/ha, DAP 60kg/ha', 'price': 1722, 'min_temp': 21, 'max_temp': 35, 'min_rain': 400, 'max_rain': 800},
    'bittergourd': {'icon': '🥒', 'season': 'Zaid', 'soil': 'Sandy', 'fert': 'Urea 100kg/ha, DAP 60kg/ha', 'price': 3802, 'min_temp': 25, 'max_temp': 35, 'min_rain': 400, 'max_rain': 800},
    'ridgegourd': {'icon': '🥒', 'season': 'Zaid', 'soil': 'Clay/Loamy', 'fert': 'Urea 100kg/ha, DAP 60kg/ha', 'price': 3000, 'min_temp': 24, 'max_temp': 35, 'min_rain': 400, 'max_rain': 800},
    'okra': {'icon': '🌿', 'season': 'Kharif', 'soil': 'Loamy', 'fert': 'Urea 120kg/ha, DAP 60kg/ha', 'price': 2500, 'min_temp': 24, 'max_temp': 35, 'min_rain': 400, 'max_rain': 800},
    'fenugreek': {'icon': '🌿', 'season': 'Rabi', 'soil': 'Sandy/Loamy', 'fert': 'Urea 60kg/ha, DAP 40kg/ha', 'price': 5638, 'min_temp': 15, 'max_temp': 30, 'min_rain': 300, 'max_rain': 600},
    'mint': {'icon': '🌿', 'season': 'Zaid', 'soil': 'Loamy', 'fert': 'Urea 60kg/ha, DAP 40kg/ha', 'price': 2000, 'min_temp': 18, 'max_temp': 25, 'min_rain': 500, 'max_rain': 1000},
    'aloe_vera': {'icon': '🌵', 'season': 'Zaid', 'soil': 'Sandy', 'fert': 'Urea 40kg/ha, DAP 30kg/ha', 'price': 1000, 'min_temp': 20, 'max_temp': 35, 'min_rain': 200, 'max_rain': 400},
    'rubber': {'icon': '🌳', 'season': 'Zaid', 'soil': 'Loamy', 'fert': 'Urea 80kg/ha, DAP 40kg/ha', 'price': 20700, 'min_temp': 25, 'max_temp': 34, 'min_rain': 2000, 'max_rain': 3500},
    'avocado': {'icon': '🥑', 'season': 'Zaid', 'soil': 'Sandy/Loamy', 'fert': 'Urea 100kg/ha, DAP 50kg/ha', 'price': 17500, 'min_temp': 15, 'max_temp': 29, 'min_rain': 1000, 'max_rain': 2000},
    'cherry': {'icon': '🍒', 'season': 'Rabi', 'soil': 'Loamy', 'fert': 'Urea 60kg/ha, DAP 40kg/ha', 'price': 75000, 'min_temp': 20, 'max_temp': 25, 'min_rain': 600, 'max_rain': 1000},
    'jackfruit': {'icon': '🍈', 'season': 'Zaid', 'soil': 'Loamy', 'fert': 'Urea 100kg/ha, DAP 50kg/ha', 'price': 3052, 'min_temp': 22, 'max_temp': 35, 'min_rain': 1000, 'max_rain': 2500},
    'pear': {'icon': '🍐', 'season': 'Rabi', 'soil': 'Loamy', 'fert': 'Urea 60kg/ha, DAP 40kg/ha', 'price': 10603, 'min_temp': 18, 'max_temp': 23, 'min_rain': 600, 'max_rain': 1000},
    'apricot': {'icon': '🍑', 'season': 'Rabi', 'soil': 'Loamy', 'fert': 'Urea 60kg/ha, DAP 40kg/ha', 'price': 10000, 'min_temp': 20, 'max_temp': 25, 'min_rain': 500, 'max_rain': 800},
    'oatpea': {'icon': '🌾', 'season': 'Rabi', 'soil': 'Loamy', 'fert': 'Urea 80kg/ha, DAP 40kg/ha', 'price': 3000, 'min_temp': 7, 'max_temp': 24, 'min_rain': 300, 'max_rain': 600},
    'pigeonpea': {'icon': '🫘', 'season': 'Kharif', 'soil': 'Sandy loam', 'fert': 'Urea 30kg/ha, DAP 20kg/ha', 'price': 3198, 'min_temp': 25, 'max_temp': 35, 'min_rain': 500, 'max_rain': 1000},
    'horsegram': {'icon': '🫘', 'season': 'Kharif', 'soil': 'Sandy loam', 'fert': 'Urea 30kg/ha, DAP 20kg/ha', 'price': 3702, 'min_temp': 25, 'max_temp': 30, 'min_rain': 300, 'max_rain': 600},
    'chickoo': {'icon': '🟤', 'season': 'Zaid', 'soil': 'Loamy', 'fert': 'Urea 80kg/ha, DAP 50kg/ha', 'price': 3000, 'min_temp': 20, 'max_temp': 35, 'min_rain': 800, 'max_rain': 1500},
    'grapes': {'icon': '🍇', 'season': 'Zaid', 'soil': 'Loamy', 'fert': 'Urea 120kg/ha, DAP 60kg/ha', 'price': 8942, 'min_temp': 20, 'max_temp': 35, 'min_rain': 600, 'max_rain': 1000},
    'litchi': {'icon': '🍒', 'season': 'Zaid', 'soil': 'Loamy', 'fert': 'Urea 80kg/ha, DAP 50kg/ha', 'price': 17500, 'min_temp': 20, 'max_temp': 35, 'min_rain': 1000, 'max_rain': 1500},
    'muskmelon': {'icon': '🍈', 'season': 'Zaid', 'soil': 'Sandy', 'fert': 'Urea 80kg/ha, DAP 50kg/ha', 'price': 2500, 'min_temp': 20, 'max_temp': 35, 'min_rain': 300, 'max_rain': 600},
    'capsicum': {'icon': '🫑', 'season': 'Zaid', 'soil': 'Loamy', 'fert': 'Urea 120kg/ha, DAP 60kg/ha', 'price': 3189, 'min_temp': 18, 'max_temp': 30, 'min_rain': 400, 'max_rain': 800},
    'cardamom': {'icon': '🟢', 'season': 'Zaid', 'soil': 'Loamy', 'fert': 'Urea 60kg/ha, DAP 40kg/ha', 'price': 217800, 'min_temp': 15, 'max_temp': 35, 'min_rain': 1500, 'max_rain': 4000},
    'fennel': {'icon': '🌿', 'season': 'Rabi', 'soil': 'Loamy', 'fert': 'Urea 60kg/ha, DAP 40kg/ha', 'price': 7810, 'min_temp': 15, 'max_temp': 25, 'min_rain': 400, 'max_rain': 800},
    'clove': {'icon': '🟤', 'season': 'Zaid', 'soil': 'Loamy', 'fert': 'Urea 50kg/ha, DAP 40kg/ha', 'price': 85500, 'min_temp': 20, 'max_temp': 30, 'min_rain': 1500, 'max_rain': 2500},
    'saffron': {'icon': '🟣', 'season': 'Rabi', 'soil': 'Loamy', 'fert': 'Urea 40kg/ha, DAP 30kg/ha', 'price': 200000, 'min_temp': 15, 'max_temp': 25, 'min_rain': 300, 'max_rain': 500},
    'tamarind': {'icon': '🟤', 'season': 'Zaid', 'soil': 'Loamy', 'fert': 'Urea 60kg/ha, DAP 40kg/ha', 'price': 7690, 'min_temp': 20, 'max_temp': 35, 'min_rain': 500, 'max_rain': 1500},
    'fig': {'icon': '🪴', 'season': 'Zaid', 'soil': 'Loamy', 'fert': 'Urea 80kg/ha, DAP 60kg/ha', 'price': 14000, 'min_temp': 18, 'max_temp': 27, 'min_rain': 500, 'max_rain': 800},
    'flaxseed': {'icon': '🌾', 'season': 'Rabi', 'soil': 'Sandy', 'fert': 'Urea 60kg/ha, DAP 40kg/ha', 'price': 5540, 'min_temp': 13, 'max_temp': 20, 'min_rain': 300, 'max_rain': 600},
    'sweetpotato': {'icon': '🍠', 'season': 'Kharif', 'soil': 'Loamy', 'fert': 'Urea 120kg/ha, DAP 60kg/ha', 'price': 3071, 'min_temp': 21, 'max_temp': 26, 'min_rain': 500, 'max_rain': 1000},
    'yamcorn': {'icon': '🌽', 'season': 'Kharif', 'soil': 'Loamy', 'fert': 'Urea 100kg/ha, DAP 50kg/ha', 'price': 3000, 'min_temp': 20, 'max_temp': 30, 'min_rain': 1000, 'max_rain': 1500},
    'broccoli': {'icon': '🥦', 'season': 'Rabi', 'soil': 'Loamy', 'fert': 'Urea 120kg/ha, DAP 60kg/ha', 'price': 750, 'min_temp': 15, 'max_temp': 21, 'min_rain': 400, 'max_rain': 800},
    'rosemary': {'icon': '🌿', 'season': 'Zaid', 'soil': 'Well drained', 'fert': 'Urea 50kg/ha, DAP 30kg/ha', 'price': 8000, 'min_temp': 15, 'max_temp': 25, 'min_rain': 300, 'max_rain': 600},
    'cocoa': {'icon': '🟤', 'season': 'Zaid', 'soil': 'Loamy', 'fert': 'Urea 80kg/ha, DAP 50kg/ha', 'price': 12000, 'min_temp': 19, 'max_temp': 30, 'min_rain': 1500, 'max_rain': 2500},
    'beans': {'icon': '🫘', 'season': 'Kharif', 'soil': 'Sandy loam', 'fert': 'Urea 25kg/ha, DAP 60kg/ha', 'price': 6951, 'min_temp': 21, 'max_temp': 29, 'min_rain': 400, 'max_rain': 800},
    'coconut': {'icon': '🥥', 'season': 'Zaid', 'soil': 'Sandy', 'fert': 'Urea 200kg/ha, DAP 100kg/ha', 'price': 6135, 'min_temp': 20, 'max_temp': 32, 'min_rain': 1300, 'max_rain': 2300},
}

# ============================================
# CROP FAMILIES FOR ROTATION
# ============================================

CROP_FAMILIES = {
    'Rice': 'Cereal', 'Wheat': 'Cereal', 'Maize': 'Cereal', 'Barley': 'Cereal',
    'Millets': 'Cereal', 'Cotton': 'Fiber', 'Jute': 'Fiber', 'Sugarcane': 'Cash',
    'Tea': 'Plantation', 'Coffee': 'Plantation', 'Groundnut': 'Legume',
    'Soybean': 'Legume', 'Pulses': 'Legume', 'Chickpea': 'Legume',
    'Kidneybeans': 'Legume', 'Pigeonpeas': 'Legume', 'Mothbeans': 'Legume',
    'Mungbean': 'Legume', 'Blackgram': 'Legume', 'Lentil': 'Legume',
    'Potato': 'Solanaceae', 'Mustard': 'Oilseed', 'Pomegranate': 'Fruit',
    'Banana': 'Fruit', 'Mango': 'Fruit', 'Grapes': 'Fruit',
    'Watermelon': 'Fruit', 'Muskmelon': 'Fruit', 'Apple': 'Fruit',
    'Orange': 'Fruit', 'Papaya': 'Fruit', 'Coconut': 'Plantation'
}

# ============================================
# AUTHENTICATION ROUTES (DATABASE)
# ============================================

@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        full_name = data.get('full_name')
        
        # Check if user exists
        if User.query.filter_by(username=username).first():
            return jsonify({'success': False, 'error': 'Username already exists'}), 400
        
        if User.query.filter_by(email=email).first():
            return jsonify({'success': False, 'error': 'Email already exists'}), 400
        
        # Hash password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Create new user
        new_user = User(
            username=username,
            password=hashed_password.decode('utf-8'),
            email=email,
            full_name=full_name
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({'success': True, 'user': new_user.to_dict()})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 401
        
        if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return jsonify({'success': False, 'error': 'Invalid password'}), 401
        
        return jsonify({'success': True, 'user_id': user.user_id, 'user': user.to_dict()})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/history/<int:user_id>', methods=['GET'])
def get_user_history(user_id):
    try:
        histories = History.query.filter_by(user_id=user_id).order_by(History.timestamp.desc()).all()
        return jsonify({'success': True, 'history': [h.to_dict() for h in histories]})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================
# PREDICTION ROUTE (UPDATED WITH DATABASE)
# ============================================

@app.route('/predict', methods=['POST'])
def predict():
    mdl = get_model()
    if mdl is None:
        return jsonify({'error': 'Model not available. Try refreshing.'}), 500
    
    try:
        data = request.json
        print("📥 Received data:", data)
        
        # Get user inputs
        # IMPORTANT: if user provides all-zero sensor values (or invalid placeholders), model still returns top-3.
        # We must block that and ask for real values.
        required_keys = ['N', 'P', 'K', 'ph', 'humidity', 'temperature', 'rainfall']
        missing = [k for k in required_keys if k not in data]
        if missing:
            return jsonify({'success': False, 'error': f"Missing inputs: {', '.join(missing)}"}), 400

        user_N = float(data['N'])
        user_P = float(data['P'])
        user_K = float(data['K'])
        user_temp = float(data['temperature'])
        user_humidity = float(data['humidity'])
        user_ph = float(data['ph'])
        user_rainfall = float(data['rainfall'])

        # Treat 0 as invalid for these fields (0 pH / 0 rainfall / 0 temp / etc. are placeholders in UI).
        # If everything is 0 (or effectively 0), block recommendation.
        # If user selects ALL-zero OR ANY subset includes 0, the UI/UX expectation is to block.
        # Your requirement: if everything is zero OR 2+ parameters are zero -> show message.
        values = [
            ('N', user_N),
            ('P', user_P),
            ('K', user_K),
            ('pH', user_ph),
            ('humidity', user_humidity),
            ('temperature', user_temp),
            ('rainfall', user_rainfall),
        ]
        zero_fields = [name for name, v in values if v == 0]
        if len(zero_fields) >= 2:
            # Provide a friendly message instead of recommendations
            if len(zero_fields) == 7:
                msg = 'Please select valid inputs for ALL parameters (N, P, K, pH, humidity, temperature, rainfall).'
            else:
                msg = f"Please select valid values. Detected 0 for: {', '.join(zero_fields)}"
            return jsonify({'success': False, 'error': msg}), 400

        # Also block impossible/placeholder pH (redundant safety)
        if user_ph == 0:
            return jsonify({'success': False, 'error': 'Invalid pH value (0). Please provide a valid soil pH.'}), 400


        features = np.array([[
            user_N,
            user_P,
            user_K,
            user_temp,
            user_humidity,
            user_ph,
            user_rainfall
        ]])
        
        # Get probabilities from model
        probabilities = mdl.predict_proba(features)[0]
        all_crops = list(mdl.classes_)
        
        # ============================================
        # STEP 1: SCORE ALL CROPS (NO FILTERING YET)
        # ============================================
        
        scored_crops = []
        
        for i, crop in enumerate(all_crops):
            prob = probabilities[i]
            crop_info = CROP_INFO.get(crop, {})
            
            # Get crop requirements (with defaults)
            crop_min_rain = crop_info.get('min_rain', 0)
            crop_max_rain = crop_info.get('max_rain', 5000)
            crop_min_temp = crop_info.get('min_temp', 0)
            crop_max_temp = crop_info.get('max_temp', 50)
            
            # Start with ML probability (convert to percentage)
            score = prob * 100
            
            # ============================================
            # STEP 2: RAINFALL PENALTY
            # ============================================
            
            rainfall_penalty = 0
            
            # Severe penalty for low-rainfall crops in high rainfall (>1500mm)
            if user_rainfall > 1500 and crop_max_rain < 1000:
                rainfall_penalty = 50
                print(f"⚠️ Heavy rain penalty for {crop}: needs only {crop_max_rain}mm")
            
            # Moderate penalty if rainfall exceeds crop's max
            elif user_rainfall > crop_max_rain:
                excess_ratio = (user_rainfall - crop_max_rain) / max(crop_max_rain, 1)
                rainfall_penalty = min(40, excess_ratio * 25)
            
            # Penalty if too dry
            elif user_rainfall < crop_min_rain and crop_min_rain > 0:
                deficit_ratio = (crop_min_rain - user_rainfall) / crop_min_rain
                rainfall_penalty = min(40, deficit_ratio * 25)
            
            score = max(0, score - rainfall_penalty)
            
            # ============================================
            # STEP 3: TEMPERATURE PENALTY
            # ============================================
            
            temp_penalty = 0
            if user_temp < crop_min_temp:
                temp_penalty = min(35, (crop_min_temp - user_temp) * 4)
            elif user_temp > crop_max_temp:
                temp_penalty = min(35, (user_temp - crop_max_temp) * 4)
            
            score = max(0, score - temp_penalty)
            
            # ============================================
            # STEP 4: pH PENALTY (if available)
            # ============================================
            
            crop_min_ph = crop_info.get('min_ph', 4.0)
            crop_max_ph = crop_info.get('max_ph', 8.5)
            
            ph_penalty = 0
            if user_ph < crop_min_ph:
                ph_penalty = min(30, (crop_min_ph - user_ph) * 12)
            elif user_ph > crop_max_ph:
                ph_penalty = min(30, (user_ph - crop_max_ph) * 12)
            
            score = max(0, score - ph_penalty)
            
            # Store all crops (even low scores)
            scored_crops.append({
                'name': crop,
                'score': score,
                'prob': prob,
                'crop_info': crop_info
            })
        
        # ============================================
        # STEP 5: SORT AND GET TOP 3 (GUARANTEED)
        # ============================================
        
        # Sort by score (highest first)
        scored_crops.sort(key=lambda x: x['score'], reverse=True)
        
        # ALWAYS take top 3 (if less than 3 exist, use what's available)
        top_3 = scored_crops[:3]
        
        # If still less than 3, add fallback crops
        fallback_crops = ['rice', 'wheat', 'maize']
        while len(top_3) < 3:
            fallback = fallback_crops[len(top_3)]
            top_3.append({
                'name': fallback,
                'score': 50,
                'prob': 0.5,
                'crop_info': CROP_INFO.get(fallback, {})
            })
            print(f"⚠️ Added fallback crop: {fallback}")
        
        # ============================================
        # STEP 6: BUILD RESPONSE
        # ============================================
        
        recommendations = []
        for i, crop_data in enumerate(top_3):
            crop = crop_data['name']
            score = crop_data['score']
            crop_info = crop_data['crop_info']
            
            recommendations.append({
                'rank': i + 1,
                'name': crop,
                'icon': crop_info.get('icon', '🌿'),
                'season': crop_info.get('season', 'General'),
                'fert': crop_info.get('fert', 'Standard fertilizer'),
                'price': crop_info.get('price', 0),
                'confidence': round(score, 2),
                'min_temp': crop_info.get('min_temp', 0),
                'max_temp': crop_info.get('max_temp', 0),
                'min_rain': crop_info.get('min_rain', 0),
                'max_rain': crop_info.get('max_rain', 0),
            })
        
        # ============================================
        # STEP 7: SAVE TO DATABASE (if user logged in)
        # ============================================
        
        user_id = data.get('user_id')
        if user_id:
            try:
                new_history = History(
                    user_id=user_id,
                    soil_type=data.get('soil_type', 'Unknown'),
                    temperature=user_temp,
                    rainfall=user_rainfall,
                    N_value=int(data['N']),
                    P_value=int(data['P']),
                    K_value=int(data['K']),
                    ph_value=user_ph,
                    humidity=int(data['humidity']),
                    top_crop_1=recommendations[0]['name'] if len(recommendations) > 0 else None,
                    top_crop_2=recommendations[1]['name'] if len(recommendations) > 1 else None,
                    top_crop_3=recommendations[2]['name'] if len(recommendations) > 2 else None
                )
                db.session.add(new_history)
                db.session.commit()
                print(f"✅ Saved to database - History ID: {new_history.history_id}")
            except Exception as db_error:
                print(f"⚠️ Database save error: {db_error}")
        
        print("✅ Recommendations generated:", [r['name'] for r in recommendations])
        
        return jsonify({'success': True, 'recommendations': recommendations})
        
    except Exception as e:
        print("❌ Error:", str(e))
        return jsonify({'error': str(e)}), 500
# ============================================
# OTHER API ROUTES (Unchanged)
# ============================================

@app.route('/health', methods=['GET'])
def health():
    mdl = get_model()
    return jsonify({'status': 'healthy', 'model_loaded': mdl is not None, 'database': 'connected'})


@app.route('/contact', methods=['POST'])
def contact():
    try:
        data = request.json
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')
        
        msg = Message(
            subject=f"New Contact Form Message from {name}",
            recipients=['support@cropsense.in'],
            body=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}",
            reply_to=email
        )
        
        if app.config.get('TESTING', False):
            print(f"📧 Mock email: {name} <{email}> - {message[:100]}...")
            return jsonify({'success': True, 'message': 'Email queued (dev mode)'})
        mail.send(msg)
        
        return jsonify({'success': True, 'message': 'Email sent successfully!'})
        
    except Exception as e:
        print("❌ Email error:", str(e))
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/model-metrics', methods=['GET'])
def model_metrics():
    return jsonify({
        'algorithm': 'Random Forest Classifier',
        'accuracy': '92.5%',
        'precision': '0.91',
        'recall': '0.90',
        'f1_score': '0.905',
        'training_samples': 1760,
        'testing_samples': 440,
        'total_crops': len(CROP_INFO),
        'features_used': ['N', 'P', 'K', 'Temperature', 'Humidity', 'pH', 'Rainfall']
    })


# ============================================
# HELPER FUNCTIONS
# ============================================

def get_crop_npk_requirements(crop):
    """Get NPK and pH requirements for a crop."""
    defaults = {
        'N_min': 60, 'N_max': 120, 'P_min': 30, 'P_max': 60,
        'K_min': 30, 'K_max': 60, 'pH_min': 5.5, 'pH_max': 7.5,
        'temp_min': 15, 'temp_max': 35, 'rain_min': 50, 'rain_max': 200
    }
    
    crop_specific = {
        'Rice': {'N_min': 80, 'N_max': 120, 'P_min': 40, 'P_max': 60, 'K_min': 40, 'K_max': 60, 
                 'temp_min': 20, 'temp_max': 35, 'rain_min': 100, 'rain_max': 300, 'pH_min': 5.0, 'pH_max': 7.0},
        'Wheat': {'N_min': 80, 'N_max': 120, 'P_min': 40, 'P_max': 60, 'K_min': 30, 'K_max': 50,
                  'temp_min': 10, 'temp_max': 25, 'rain_min': 50, 'rain_max': 150, 'pH_min': 6.0, 'pH_max': 7.5},
        'Maize': {'N_min': 100, 'N_max': 150, 'P_min': 50, 'P_max': 70, 'K_min': 40, 'K_max': 60,
                  'temp_min': 18, 'temp_max': 32, 'rain_min': 50, 'rain_max': 120, 'pH_min': 5.5, 'pH_max': 7.0},
        'Potato': {'N_min': 100, 'N_max': 150, 'P_min': 60, 'P_max': 90, 'K_min': 100, 'K_max': 150,
                   'temp_min': 15, 'temp_max': 25, 'rain_min': 50, 'rain_max': 120, 'pH_min': 5.0, 'pH_max': 6.5},
        'Cotton': {'N_min': 80, 'N_max': 120, 'P_min': 40, 'P_max': 60, 'K_min': 40, 'K_max': 60,
                   'temp_min': 20, 'temp_max': 40, 'rain_min': 50, 'rain_max': 100, 'pH_min': 6.0, 'pH_max': 7.5},
    }
    
    reqs = defaults.copy()
    if crop in crop_specific:
        reqs.update(crop_specific[crop])
    elif crop in CROP_INFO:
        info = CROP_INFO[crop]
        reqs.update({
            'temp_min': info.get('min_temp', defaults['temp_min']),
            'temp_max': info.get('max_temp', defaults['temp_max']),
            'rain_min': info.get('min_rain', defaults['rain_min']),
            'rain_max': info.get('max_rain', defaults['rain_max']),
        })
    
    return reqs


def calculate_suitability_score(N, P, K, pH, crop_reqs):
    """Calculate overall suitability score (0-100)."""
    score = 100
    
    if N < crop_reqs['N_min']:
        deficit = crop_reqs['N_min'] - N
        score -= min(25, deficit / 2)
    elif N > crop_reqs['N_max']:
        excess = N - crop_reqs['N_max']
        score -= min(10, excess / 4)
    
    if P < crop_reqs['P_min']:
        deficit = crop_reqs['P_min'] - P
        score -= min(25, deficit / 1.5)
    
    if K < crop_reqs['K_min']:
        deficit = crop_reqs['K_min'] - K
        score -= min(25, deficit / 2)
    
    if pH < crop_reqs['pH_min']:
        deviation = crop_reqs['pH_min'] - pH
        score -= min(25, deviation * 15)
    elif pH > crop_reqs['pH_max']:
        deviation = pH - crop_reqs['pH_max']
        score -= min(25, deviation * 15)
    
    return max(0, round(score, 1))


# ============================================
# ADDITIONAL API ENDPOINTS (Unchanged)
# ============================================

@app.route('/api/fertilizer-plan', methods=['POST'])
def fertilizer_plan():
    """Get fertilizer recommendations based on soil NPK and selected crop."""
    try:
        data = request.json
        crop = data.get('crop')
        soil_n = float(data.get('N', 50))
        soil_p = float(data.get('P', 50))
        soil_k = float(data.get('K', 50))
        soil_ph = float(data.get('ph', 7.0))

        if crop not in CROP_INFO:
            return jsonify({'success': False, 'error': f'Crop {crop} not found'}), 400

        reqs = get_crop_npk_requirements(crop)
        recommendations = {'fertilizer': [], 'amendments': [], 'warnings': []}

        # Nitrogen
        n_deficit = reqs['N_min'] - soil_n
        if n_deficit > 0:
            urea_kg = round(n_deficit * 2.17, 1)
            recommendations['fertilizer'].append({
                'nutrient': 'Nitrogen (N)', 'deficit': round(n_deficit, 1),
                'product': 'Urea (46% N)', 'amount_kg_per_ha': urea_kg,
                'timing': 'Split: 50% at sowing, 50% at 30-40 days'
            })
        elif soil_n > reqs['N_max']:
            recommendations['warnings'].append(f"Nitrogen is high ({soil_n} mg/kg). Reduce N fertilizer.")

        # Phosphorus
        p_deficit = reqs['P_min'] - soil_p
        if p_deficit > 0:
            dap_kg = round(p_deficit * 2.17, 1)
            recommendations['fertilizer'].append({
                'nutrient': 'Phosphorus (P)', 'deficit': round(p_deficit, 1),
                'product': 'DAP (46% P2O5)', 'amount_kg_per_ha': dap_kg,
                'timing': 'Basal application at sowing'
            })

        # Potassium
        k_deficit = reqs['K_min'] - soil_k
        if k_deficit > 0:
            mop_kg = round(k_deficit * 1.67, 1)
            recommendations['fertilizer'].append({
                'nutrient': 'Potassium (K)', 'deficit': round(k_deficit, 1),
                'product': 'MOP (60% K2O)', 'amount_kg_per_ha': mop_kg,
                'timing': 'Basal application'
            })

        # pH Amendment
        if soil_ph < reqs['pH_min']:
            lime_kg = round((reqs['pH_min'] - soil_ph) * 2000, 0)
            recommendations['amendments'].append({
                'issue': f'Low pH ({soil_ph}) - Acidic Soil',
                'solution': f'Apply {lime_kg} kg/ha agricultural lime',
                'timing': 'Apply 3-4 weeks before planting'
            })
        elif soil_ph > reqs['pH_max']:
            sulfur_kg = round((soil_ph - reqs['pH_max']) * 500, 0)
            recommendations['amendments'].append({
                'issue': f'High pH ({soil_ph}) - Alkaline Soil',
                'solution': f'Apply {sulfur_kg} kg/ha elemental sulfur',
                'timing': 'Apply during land preparation'
            })

        suitability = calculate_suitability_score(soil_n, soil_p, soil_k, soil_ph, reqs)
        recommendations['suitability_score'] = suitability

        if not recommendations['fertilizer']:
            recommendations['fertilizer'].append({
                'nutrient': 'All', 'deficit': 0,
                'product': 'No additional fertilizer needed',
                'amount_kg_per_ha': 0, 'timing': 'Soil nutrients are sufficient'
            })

        return jsonify({'success': True, 'crop': crop, 'recommendations': recommendations})

    except Exception as e:
        print(f"❌ Fertilizer plan error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/crop-compatibility', methods=['POST'])
def crop_compatibility():
    """Check if selected crop is compatible with given conditions."""
    try:
        data = request.json
        crop = data.get('crop')
        temperature = float(data.get('temperature', 25))
        rainfall = float(data.get('rainfall', 100))
        soil_ph = float(data.get('ph', 7.0))
        soil_type = data.get('soil_type', 'Loamy')

        if crop not in CROP_INFO:
            return jsonify({'success': False, 'error': f'Crop {crop} not found'}), 400

        reqs = get_crop_npk_requirements(crop)
        crop_info = CROP_INFO[crop]

        issues = []
        warnings = []

        if temperature < reqs['temp_min']:
            issues.append(f"Temperature ({temperature}°C) below optimal ({reqs['temp_min']}-{reqs['temp_max']}°C)")
        elif temperature > reqs['temp_max']:
            issues.append(f"Temperature ({temperature}°C) above optimal ({reqs['temp_min']}-{reqs['temp_max']}°C)")

        if rainfall < reqs['rain_min']:
            warnings.append(f"Rainfall ({rainfall}mm) below recommended ({reqs['rain_min']}-{reqs['rain_max']}mm). Irrigation needed.")
        elif rainfall > reqs['rain_max']:
            warnings.append(f"Rainfall ({rainfall}mm) above recommended. Ensure good drainage.")

        if soil_ph < reqs['pH_min']:
            issues.append(f"Soil pH ({soil_ph}) too acidic for {crop}. Lime recommended.")
        elif soil_ph > reqs['pH_max']:
            issues.append(f"Soil pH ({soil_ph}) too alkaline for {crop}.")

        expected_soil = crop_info.get('soil', 'Loamy')
        if soil_type != expected_soil and expected_soil != 'Loamy':
            warnings.append(f"{crop} typically grows best in {expected_soil} soil.")

        compatibility = {
            'is_compatible': len(issues) == 0,
            'issues': issues,
            'warnings': warnings,
            'overall_score': max(0, 100 - (len(issues) * 25) - (len(warnings) * 10))
        }

        return jsonify({'success': True, 'crop': crop, 'compatibility': compatibility})

    except Exception as e:
        print(f"❌ Compatibility error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/alternative-crops', methods=['POST'])
def alternative_crops():
    """Find alternative crops matching the given conditions."""
    try:
        data = request.json
        temperature = float(data.get('temperature', 25))
        rainfall = float(data.get('rainfall', 100))
        soil_ph = float(data.get('ph', 7.0))
        soil_type = data.get('soil_type', 'Loamy')

        alternatives = []

        for crop, info in CROP_INFO.items():
            reqs = get_crop_npk_requirements(crop)

            temp_ok = reqs['temp_min'] <= temperature <= reqs['temp_max']
            rain_ok = reqs['rain_min'] - 20 <= rainfall <= reqs['rain_max'] + 20
            ph_ok = reqs['pH_min'] - 0.5 <= soil_ph <= reqs['pH_max'] + 0.5

            if temp_ok and rain_ok and ph_ok:
                score = 100
                if not (reqs['rain_min'] <= rainfall <= reqs['rain_max']):
                    score -= 15
                if not (reqs['pH_min'] <= soil_ph <= reqs['pH_max']):
                    score -= 10
                if soil_type != info.get('soil', 'Loamy'):
                    score -= 10

                alternatives.append({
                    'crop': crop, 'icon': info.get('icon', '🌿'),
                    'season': info.get('season', 'General'), 'score': max(0, score),
                    'price_per_quintal': info.get('price', 0)
                })

        alternatives.sort(key=lambda x: x['score'], reverse=True)

        return jsonify({'success': True, 'alternatives': alternatives[:5]})

    except Exception as e:
        print(f"❌ Alternatives error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/rotation-check', methods=['POST'])
def rotation_check():
    """Check crop rotation validity."""
    try:
        data = request.json
        current_crop = data.get('current_crop')
        previous_crops = data.get('previous_crops', [])

        if not current_crop:
            return jsonify({'success': False, 'error': 'No current crop provided'}), 400

        warnings = []
        recommendations = []

        current_family = CROP_FAMILIES.get(current_crop, 'Other')

        if current_crop in previous_crops:
            warnings.append(f"⚠️ {current_crop} was grown in previous season. Risk of pest/disease buildup.")
            recommendations.append(f"Consider a break crop like a legume before planting {current_crop} again.")

        for prev_crop in previous_crops:
            if not prev_crop:
                continue
            prev_family = CROP_FAMILIES.get(prev_crop, 'Other')
            if prev_family == current_family and current_family in ['Cereal', 'Solanaceae']:
                warnings.append(f"⚠️ {prev_crop} (same family as {current_crop}) was grown recently.")
                recommendations.append(f"Avoid planting crops from the {current_family} family consecutively.")
                break

        if current_family == 'Cereal':
            recommendations.append("✅ Good rotation: Cereal → Legume (fixes nitrogen) → Oilseed")
        elif current_family == 'Legume':
            recommendations.append("✅ Legumes are excellent rotation crops! Follow with cereals.")

        return jsonify({
            'success': True,
            'rotation_healthy': len(warnings) == 0,
            'warnings': warnings,
            'recommendations': recommendations[:3]
        })

    except Exception as e:
        print(f"❌ Rotation check error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/seed', methods=['POST'])
def seed_database():
    """Seed initial soil types into database."""
    try:
        soil_types = [
            {'name': 'Loamy', 'description': 'Ideal for most crops. Balanced sand, silt, and clay.', 
             'npk_profile': 'N:Medium, P:High, K:Medium', 'ph_range': '6.0-7.5',
             'best_crops': 'Wheat, Maize, Potato, Tomato, Onion', 
             'improvements': 'Maintain with crop rotation and organic matter'},
            {'name': 'Clay', 'description': 'Heavy, sticky when wet, hard when dry. High water holding capacity.',
             'npk_profile': 'N:High, P:Medium, K:High', 'ph_range': '6.5-7.5',
             'best_crops': 'Rice, Sugarcane, Wheat, Cotton',
             'improvements': 'Add organic matter, gypsum for better structure'},
            {'name': 'Sandy', 'description': 'Light, drains quickly, low nutrient retention.',
             'npk_profile': 'N:Low, P:Low, K:Low', 'ph_range': '5.5-7.0',
             'best_crops': 'Groundnut, Watermelon, Muskmelon, Carrot',
             'improvements': 'Add organic matter, mulching, drip irrigation'},
        ]
        
        for soil in soil_types:
            if not SoilType.query.filter_by(name=soil['name']).first():
                new_soil = SoilType(**soil)
                db.session.add(new_soil)
        
        db.session.commit()
        return jsonify({'success': True, 'message': 'Database seeded successfully'})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)