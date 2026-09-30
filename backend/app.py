# backend/app.py
from flask import Flask, request, jsonify, send_from_directory, session
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, User, SoilType, Crop, CropDetails, History, Recommendation, Feedback
import joblib
import numpy as np
import os
import json
from flask_mail import Mail, Message
from dotenv import load_dotenv
import subprocess
from datetime import datetime
import bcrypt
import uuid
from crop_knowledge import get_crop_diseases_info, get_crop_pests_info, get_crop_varieties_info, get_crop_growing_info, get_crop_npk_info

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app, supports_credentials=True)

load_dotenv()

# Load native crop name translations (used to fix mistranslated crop names like fig → ಚಿತ್ರ)
CROP_NATIVE_NAMES = {}
for lang_code in ['kn', 'hi', 'mr', 'ta', 'te']:
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'{lang_code}_crop_names.json')
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            CROP_NATIVE_NAMES[lang_code] = json.load(f)

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
    print("[OK] Database tables created")

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
    print("[INFO] Email disabled (no .env creds). Set MAIL_USERNAME/PASSWORD for contact form.")

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

        if not os.path.exists(model_path):
            print("[TRAIN] Auto-training model...")
            subprocess.check_call(['python', 'model.py'])

        try:
            model = joblib.load(model_path)
            print("[OK] Model loaded successfully")
            # Cache as joblib for faster next load
            try:
                joblib.dump(model, joblib_path)
                print("[SAVE] Saved as joblib format")
            except:
                pass
        except Exception as e:
            print(f"[ERR] Model load failed: {e}")
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
    'ginger': {'icon': '🫚', 'season': 'Kharif', 'soil': 'Loamy', 'fert': 'Urea 60kg/ha, DAP 40kg/ha', 'price': 8600, 'min_temp': 22, 'max_temp': 30, 'min_rain': 800, 'max_rain': 1500},
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
    'barley': {'icon': '🌾', 'season': 'Rabi', 'soil': 'Loamy', 'fert': 'Urea 80kg/ha, DAP 40kg/ha', 'price': 1950, 'min_temp': 10, 'max_temp': 25, 'min_rain': 300, 'max_rain': 800},
    'castor': {'icon': '🌱', 'season': 'Kharif', 'soil': 'Sandy loam', 'fert': 'Urea 60kg/ha, DAP 30kg/ha', 'price': 6200, 'min_temp': 20, 'max_temp': 35, 'min_rain': 400, 'max_rain': 800},
    'chickpea': {'icon': '🫘', 'season': 'Rabi', 'soil': 'Loamy', 'fert': 'Urea 20kg/ha, DAP 40kg/ha', 'price': 5200, 'min_temp': 18, 'max_temp': 30, 'min_rain': 400, 'max_rain': 800},
    'mango': {'icon': '🥭', 'season': 'Zaid', 'soil': 'Loamy', 'fert': 'Urea 100kg/ha, DAP 50kg/ha', 'price': 35000, 'min_temp': 18, 'max_temp': 35, 'min_rain': 500, 'max_rain': 1000},
    'orange': {'icon': '🍊', 'season': 'Zaid', 'soil': 'Loamy', 'fert': 'Urea 80kg/ha, DAP 40kg/ha', 'price': 7500, 'min_temp': 15, 'max_temp': 30, 'min_rain': 600, 'max_rain': 1200},
    'pomegranate': {'icon': '🔴', 'season': 'Zaid', 'soil': 'Loamy', 'fert': 'Urea 60kg/ha, DAP 40kg/ha', 'price': 15000, 'min_temp': 20, 'max_temp': 35, 'min_rain': 400, 'max_rain': 800},
    'yam': {'icon': '🍠', 'season': 'Kharif', 'soil': 'Loamy', 'fert': 'Urea 100kg/ha, DAP 50kg/ha', 'price': 3000, 'min_temp': 20, 'max_temp': 30, 'min_rain': 1000, 'max_rain': 1500},
    'kidneybeans': {'icon': '🫘', 'season': 'Rabi', 'soil': 'Loamy', 'fert': 'Urea 30kg/ha, DAP 60kg/ha', 'price': 6951, 'min_temp': 18, 'max_temp': 25, 'min_rain': 400, 'max_rain': 800},
    'mothbeans': {'icon': '🫘', 'season': 'Kharif', 'soil': 'Sandy loam', 'fert': 'Urea 25kg/ha, DAP 20kg/ha', 'price': 5500, 'min_temp': 25, 'max_temp': 35, 'min_rain': 300, 'max_rain': 600},
    'mungbean': {'icon': '🟢', 'season': 'Kharif', 'soil': 'Sandy loam', 'fert': 'Urea 25kg/ha, DAP 20kg/ha', 'price': 6132, 'min_temp': 25, 'max_temp': 35, 'min_rain': 400, 'max_rain': 800},
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
        print("[IN] Received data:", data)
        
        # Whether to return all scored crops or just top 3
        show_all = data.get('show_all', False)
        
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

        # Treat 0 or slider-minimum values as invalid (placeholder indicators).
        # Block when ALL parameters are at minimum (user hasn't entered real data).
        values = [
            ('N', user_N, 20),
            ('P', user_P, 0),
            ('K', user_K, 0),
            ('pH', user_ph, 3.0),
            ('humidity', user_humidity, 40),
            ('temperature', user_temp, 5),
            ('rainfall', user_rainfall, 250),
        ]
        zero_fields = [name for name, v, _ in values if v == 0]
        at_minimum = sum(1 for _, v, m in values if v <= m)
        if len(zero_fields) >= 2 or at_minimum >= 6:
            if len(zero_fields) == 7 or at_minimum == 7:
                msg = 'Please select valid inputs for ALL parameters (N, P, K, pH, humidity, temperature, rainfall).'
            elif at_minimum >= 6:
                msg = 'Most values are at minimum. Please provide realistic soil and climate values for accurate recommendations.'
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
                print(f"[WARN] Heavy rain penalty for {crop}: needs only {crop_max_rain}mm")
            
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
        # STEP 5: SORT AND SELECT CROPS
        # ============================================
        
        # Sort by score (highest first)
        scored_crops.sort(key=lambda x: x['score'], reverse=True)
        
        # Filter out crops with zero score (irrelevant for extreme inputs)
        valid_crops = [c for c in scored_crops if c['score'] > 0]
        
        # If show_all, return all scored crops; otherwise just top valid crops (max 3)
        selected = scored_crops if show_all else valid_crops[:3]
        
        # In top-3 mode, ensure exactly 3 (use fallbacks if needed)
        fallback_crops = ['rice', 'wheat', 'maize']
        if not show_all:
            while len(selected) < 3:
                fallback = fallback_crops[len(selected)]
                selected.append({
                    'name': fallback,
                    'score': 50,
                    'prob': 0.5,
                    'crop_info': CROP_INFO.get(fallback, {})
                })
                print(f"[WARN] Added fallback crop: {fallback}")
        
        # ============================================
        # STEP 6: BUILD RESPONSE
        # ============================================
        
        recommendations = []
        for i, crop_data in enumerate(selected):
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
        top_3_recs = recommendations[:3]  # for database, always top 3
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
                    top_crop_1=top_3_recs[0]['name'] if len(top_3_recs) > 0 else None,
                    top_crop_2=top_3_recs[1]['name'] if len(top_3_recs) > 1 else None,
                    top_crop_3=top_3_recs[2]['name'] if len(top_3_recs) > 2 else None
                )
                db.session.add(new_history)
                db.session.commit()
                print(f"[OK] Saved to database - History ID: {new_history.history_id}")
            except Exception as db_error:
                print(f"[WARN] Database save error: {db_error}")
        
        print(f"[OK] Recommendations generated: {len(recommendations)} crops (show_all={show_all})")
        if not show_all:
            print("[OK] Top:", [r['name'] for r in recommendations])
        
        return jsonify({'success': True, 'recommendations': recommendations})
        
    except Exception as e:
        print("[ERR] Error:", str(e))
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
            print(f"[MAIL] Mock email: {name} <{email}> - {message[:100]}...")
            return jsonify({'success': True, 'message': 'Email queued (dev mode)'})
        mail.send(msg)
        
        return jsonify({'success': True, 'message': 'Email sent successfully!'})
        
    except Exception as e:
        print("[ERR] Email error:", str(e))
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/model-metrics', methods=['GET'])
def model_metrics():
    try:
        metrics_path = os.path.join(basedir, 'model_metrics.json')
        if os.path.exists(metrics_path):
            with open(metrics_path, 'r') as f:
                metrics = json.load(f)
            return jsonify(metrics)
    except:
        pass
    return jsonify({
        'algorithm': 'Random Forest Classifier',
        'accuracy': 'N/A',
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
        print(f"[ERR] Fertilizer plan error: {e}")
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
        print(f"[ERR] Compatibility error: {e}")
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
        print(f"[ERR] Alternatives error: {e}")
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
            warnings.append(f"[WARN] {current_crop} was grown in previous season. Risk of pest/disease buildup.")
            recommendations.append(f"Consider a break crop like a legume before planting {current_crop} again.")

        for prev_crop in previous_crops:
            if not prev_crop:
                continue
            prev_family = CROP_FAMILIES.get(prev_crop, 'Other')
            if prev_family == current_family and current_family in ['Cereal', 'Solanaceae']:
                warnings.append(f"[WARN] {prev_crop} (same family as {current_crop}) was grown recently.")
                recommendations.append(f"Avoid planting crops from the {current_family} family consecutively.")
                break

        if current_family == 'Cereal':
            recommendations.append("[OK] Good rotation: Cereal → Legume (fixes nitrogen) → Oilseed")
        elif current_family == 'Legume':
            recommendations.append("[OK] Legumes are excellent rotation crops! Follow with cereals.")

        return jsonify({
            'success': True,
            'rotation_healthy': len(warnings) == 0,
            'warnings': warnings,
            'recommendations': recommendations[:3]
        })

    except Exception as e:
        print(f"[ERR] Rotation check error: {e}")
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


# ============================================
# CHATBOT KNOWLEDGE BASE & API
# ============================================

PROJECT_INFO = {
    'en': {
        'name': 'CropSense',
        'tagline': 'AI-Powered Crop Recommendation System',
        'description': 'CropSense is a web-based platform that helps farmers and agriculturalists make smart decisions about crop selection. It uses machine learning (Random Forest with 97.5% accuracy) to recommend the best crops based on your soil NPK values, pH, temperature, humidity, and rainfall.',
        'features': [
            'Smart Crop Recommendation - ML-powered predictions based on soil and climate conditions',
            'Fertilizer Planning - Get customized fertilizer plans for your crops',
            'Crop Compatibility Check - Check if a crop suits your conditions',
            'Crop Rotation Planning - Plan crop rotation to maintain soil health',
            'Alternative Crop Suggestions - Find alternative crops that match your conditions',
            'Interactive Dashboard - Visualize your farm data and history',
            'AI Chatbot Assistant - Get instant answers to all your farming questions',
            'Multi-language Support - Available in English, Hindi, Marathi, Kannada, Tamil, Telugu',
            'Email Contact Form - Get in touch with the team'
        ],
        'how_to_use': [
            '1. Register an account or log in',
            '2. Enter your soil NPK values (N, P, K), pH, temperature, humidity, and rainfall',
            '3. Click "Get Recommendation" to see the top 3 crops for your conditions',
            '4. Use the Fertilizer Plan tool to get detailed fertilizer advice',
            '5. Check crop compatibility before planting',
            '6. Track your prediction history on the dashboard'
        ],
        'tech': 'Built with Flask (Python), scikit-learn Random Forest, SQLite database, and JavaScript frontend'
    },
    'hi': {
        'name': 'क्रॉपसेंस',
        'tagline': 'एआई-संचालित फसल अनुशंसा प्रणाली',
        'description': 'क्रॉपसेंस एक वेब-आधारित प्लेटफॉर्म है जो किसानों और कृषिविदों को फसल चयन के बारे में स्मार्ट निर्णय लेने में मदद करता है। यह आपकी मिट्टी के NPK मान, pH, तापमान, आर्द्रता और वर्षा के आधार पर सर्वोत्तम फसलों की सिफारिश करने के लिए मशीन लर्निंग (97.5% सटीकता के साथ रैंडम फॉरेस्ट) का उपयोग करता है।',
        'features': [
            'स्मार्ट फसल अनुशंसा - मिट्टी और जलवायु की स्थितियों पर आधारित ML-संचालित भविष्यवाणियां',
            'उर्वरक योजना - अपनी फसलों के लिए अनुकूलित उर्वरक योजनाएं प्राप्त करें',
            'फसल अनुकूलता जांच - जांचें कि कोई फसल आपकी स्थितियों के लिए उपयुक्त है या नहीं',
            'फसल चक्र योजना - मिट्टी के स्वास्थ्य को बनाए रखने के लिए फसल चक्र की योजना बनाएं',
            'वैकल्पिक फसल सुझाव - अपनी स्थितियों से मेल खाने वाली वैकल्पिक फसलें खोजें',
            'इंटरएक्टिव डैशबोर्ड - अपने फार्म डेटा और इतिहास को विज़ुअलाइज़ करें',
            'एआई चैटबॉट सहायक - अपने सभी कृषि प्रश्नों के तुरंत उत्तर प्राप्त करें',
            'बहु-भाषा समर्थन - हिंदी, अंग्रेजी, मराठी, कन्नड़, तमिल, तेलुगु में उपलब्ध',
            'ईमेल संपर्क फॉर्म - टीम से संपर्क करें'
        ],
        'how_to_use': [
            '1. एक खाता पंजीकृत करें या लॉग इन करें',
            '2. अपनी मिट्टी के NPK मान (N, P, K), pH, तापमान, आर्द्रता और वर्षा दर्ज करें',
            '3. अपनी स्थितियों के लिए शीर्ष 3 फसलें देखने के लिए "अनुशंसा प्राप्त करें" पर क्लिक करें',
            '4. विस्तृत उर्वरक सलाह प्राप्त करने के लिए उर्वरक योजना उपकरण का उपयोग करें',
            '5. रोपण से पहले फसल अनुकूलता जांचें',
            '6. डैशबोर्ड पर अपना पूर्वानुमान इतिहास देखें'
        ],
        'tech': 'फ्लास्क (पायथन), scikit-learn रैंडम फॉरेस्ट, SQLite डेटाबेस, और जावास्क्रिप्ट फ्रंटएंड के साथ निर्मित'
    }
}

AGRICULTURE_KNOWLEDGE = {
    'en': {
        'npk': 'NPK stands for Nitrogen (N), Phosphorus (P), and Potassium (K) - the three primary nutrients plants need.\n\n🟢 **Nitrogen (N):** Promotes leafy growth and green color. Needed for photosynthesis. Deficiency causes yellowing of leaves.\n🔵 **Phosphorus (P):** Promotes root development, flowering, and fruit set. Essential for energy transfer in plants.\n🔴 **Potassium (K):** Improves overall plant health, disease resistance, and fruit quality. Regulates water uptake.\n\n💡 Soil testing is recommended before applying fertilizers.',
        'ph': 'Soil pH measures how acidic or alkaline your soil is, on a scale of 0-14.\n\n• **pH 6.0-7.0 (Slightly acidic to neutral):** Ideal for most crops (rice, wheat, maize, vegetables)\n• **pH < 6.0 (Acidic):** Suitable for tea, coffee, potato, strawberry. Add lime to raise pH.\n• **pH > 7.5 (Alkaline):** Suitable for chickpea, mustard, barley. Add sulfur or organic matter to lower pH.\n\n💡 Most nutrients are optimally available to plants in the pH range of 6.0-7.5.',
        'seasons': 'Indian agriculture has three main cropping seasons:\n\n🌧 **Kharif (Monsoon):** June-October. Sown with monsoon rains. Crops: Rice, Maize, Cotton, Groundnut, Soybean, Sugarcane, Millets, Turmeric, Okra\n❄️ **Rabi (Winter):** October-March. Sown after monsoon. Crops: Wheat, Barley, Mustard, Peas, Lentil, Chickpea, Potato, Onion, Cabbage, Cauliflower\n☀️ **Zaid (Summer):** March-June. Short summer season. Crops: Watermelon, Muskmelon, Cucumber, Pumpkin, Fruits, Vegetables',
        'soil_types': 'Main soil types in India:\n\n🟫 **Alluvial Soil:** Found in river plains (Indus-Ganga). Best for wheat, rice, sugarcane. Most fertile.\n🟥 **Red Soil:** Found in Tamil Nadu, Karnataka. Good for groundnut, millets, potato.\n⬛ **Black Soil (Regur):** Found in Maharashtra, Gujarat. Best for cotton. Also good for wheat, sugarcane.\n🟨 **Laterite Soil:** Found in Kerala, Karnataka. Good for tea, coffee, rubber, coconut.\n🪨 **Desert Soil:** Found in Rajasthan. Suitable for drought-resistant crops like millets, barley.\n🏔 **Mountain Soil:** Found in Himalayan regions. Good for fruits like apple, pear, apricot.\n\n💡 **Loamy soil** is considered ideal for most crops due to balanced texture and nutrients.',
        'irrigation': 'Irrigation methods:\n\n💧 **Drip Irrigation:** Water delivered directly to roots. Saves 30-50% water. Best for vegetables, fruits, cash crops.\n🌊 **Flood Irrigation:** Traditional method. Fields are flooded. Used for rice, sugarcane.\n💦 **Sprinkler Irrigation:** Water sprayed like rain. Good for wheat, gram, vegetables.\n🌧 **Rainfed Farming:** Relies on monsoon rainfall. Common for millets, pulses, cotton.\n\n💡 Drip irrigation is most efficient with 90% water use efficiency.',
        'crop_rotation': 'Crop rotation is the practice of growing different crops in sequence on the same land.\n\n**Benefits:**\n• Improves soil fertility\n• Reduces pest and disease buildup\n• Controls weeds naturally\n• Better water utilization\n\n**Basic Rules:**\n• Follow legumes (add nitrogen) with cereals (need nitrogen)\n• Avoid planting same crop family repeatedly\n• Include deep-rooted and shallow-rooted crops alternately\n• Allow at least 2 years between same crop family',
    },
    'hi': {
        'npk': 'NPK का अर्थ है नाइट्रोजन (N), फॉस्फोरस (P), और पोटैशियम (K) - पौधों को आवश्यक तीन प्राथमिक पोषक तत्व।\n\n🟢 **नाइट्रोजन (N):** पत्तियों की वृद्धि और हरे रंग को बढ़ावा देता है। प्रकाश संश्लेषण के लिए आवश्यक। कमी से पत्तियां पीली हो जाती हैं।\n🔵 **फॉस्फोरस (P):** जड़ विकास, फूल आने और फल लगने को बढ़ावा देता है। पौधों में ऊर्जा स्थानांतरण के लिए आवश्यक।\n🔴 **पोटैशियम (K):** समग्र पौध स्वास्थ्य, रोग प्रतिरोधक क्षमता और फल की गुणवत्ता में सुधार करता है।\n\n💡 उर्वरक लगाने से पहले मिट्टी परीक्षण की सिफारिश की जाती है।',
        'ph': 'मिट्टी का pH 0-14 के पैमाने पर मापता है कि आपकी मिट्टी कितनी अम्लीय या क्षारीय है।\n\n• **pH 6.0-7.0 (थोड़ा अम्लीय से तटस्थ):** अधिकांश फसलों के लिए आदर्श\n• **pH < 6.0 (अम्लीय):** चाय, कॉफी, आलू, स्ट्रॉबेरी के लिए उपयुक्त। pH बढ़ाने के लिए चूना डालें।\n• **pH > 7.5 (क्षारीय):** चना, सरसों, जौ के लिए उपयुक्त। pH कम करने के लिए सल्फर या कार्बनिक पदार्थ डालें।',
        'seasons': 'भारतीय कृषि में तीन मुख्य मौसम हैं:\n\n🌧 **खरीफ (मानसून):** जून-अक्टूबर। मानसून की बारिश के साथ बोआई। फसलें: चावल, मक्का, कपास, मूंगफली, सोयाबीन, गन्ना\n❄️ **रबी (सर्दी):** अक्टूबर-मार्च। मानसून के बाद बोआई। फसलें: गेहूं, जौ, सरसों, मटर, मसूर, चना, आलू\n☀️ **ज़ायद (गर्मी):** मार्च-जून। छोटा ग्रीष्मकालीन मौसम। फसलें: तरबूज, खरबूजा, खीरा, कद्दू',
        'soil_types': 'भारत में मुख्य मिट्टी के प्रकार:\n\n🟫 **जलोढ़ मिट्टी:** नदी के मैदानों में पाई जाती है। गेहूं, चावल, गन्ना के लिए सर्वोत्तम।\n🟥 **लाल मिट्टी:** तमिलनाडु, कर्नाटक में पाई जाती है। मूंगफली, बाजरा, आलू के लिए अच्छी।\n⬛ **काली मिट्टी (रेगुर):** महाराष्ट्र, गुजरात में पाई जाती है। कपास के लिए सर्वोत्तम।\n🟨 **लैटेराइट मिट्टी:** केरल, कर्नाटक में पाई जाती है। चाय, कॉफी, रबर के लिए अच्छी।',
        'crop_rotation': 'फसल चक्र एक ही भूमि पर क्रमिक रूप से विभिन्न फसलें उगाने की प्रथा है।\n\n**लाभ:**\n• मिट्टी की उर्वरता में सुधार करता है\n• कीट और रोग निर्माण को कम करता है\n• खरपतवारों को प्राकृतिक रूप से नियंत्रित करता है\n\n**बुनियादी नियम:**\n• दलहन (नाइट्रोजन जोड़ते हैं) के बाद अनाज (नाइट्रोजन चाहिए) लगाएं\n• एक ही फसल परिवार को बार-बार लगाने से बचें',
    }
}

# Agriculture concept patterns for intent detection
CONCEPT_PATTERNS = {
    'npk': r'npk|nitrogen|phosphorus|potassium|नाइट्रोजन|फॉस्फोरस|पोटैशियम|n pk|एनपीके',
    'ph': r'\bph\b|अम्लीय|क्षारीय|acidic|alkaline|acidity|alkalinity',
    'seasons': r'kharif|rabi|zaid|season|monsoon|खरीफ|रबी|ज़ायद|मौसम',
    'soil_types': r'soil type|types of soil|मिट्टी के प्रकार|soil classification',
    'irrigation': r'irrigation|सिंचाई|drip|flood|sprinkler|rainfed',
    'crop_rotation': r'crop rotation|rotation|फसल चक्र|चक्र',
}

# Project-related patterns
PROJECT_PATTERNS = {
    'what_is': r'what is cropsense|cropsense kya hai|cropsense क्या है|about cropsense|cropsense के बारे में',
    'features': r'features|सुविधाएं|what can you do|आप क्या कर सकते हैं|capabilities',
    'how_to_use': r'how to use|how does it work|का उपयोग कैसे करें|use cropsense|getting started',
    'tech': r'technology|tech stack|built with|algorithm|model|किस तकनीक से बना है',
    'accuracy': r'accuracy|सटीकता|how accurate|कितना सटीक',
}

# Additional crop-related patterns
CROP_QUERY_PATTERNS = {
    'price': r'price|rate|cost|market|₹|rs|दाम|रेट|कीमत|भाव|मूल्य|ಬೆಲೆ|ದರ|ధర|రేటు|விலை|किंमत|दर',
    'soil': r'soil|मिट्टी|clay|loamy|sandy|alluvial|black soil|ಮಣ್ಣು|నేల|மண்|माती',
    'fertilizer': r'npk|fertilizer|urea|dap|उर्वरक|एनपीके|ಯುರಿಯಾ|डीएपी|ఎరువు|உரம்|खत',
    'season': r'season|kharif|rabi|zaid|when to grow|कब उगाएं|मौसम|ಋತು|కాలం|பருவம்|हंगाम',
    'disease': r'disease|रोग|बीमारी|blight|rust|mildew|wilt|spot|ರೋಗ|వ్యాధి|நோய்|आजार',
    'pest': r'pest|कीट|borer|aphid|moth|thrips|locust|ಕೀಟ|తెగులు|பூச்சி|कीड',
    'variety': r'variet|किस्म|breed|cultivar|प्रजाति|ತಳಿ|రకం|இனம்|जात',
    'growing': r'grow|growing|cultivation|खेती|उगाना|planting|बोआई|ಬೆಳೆ|సాగు|சாகுபடி|लागवड|पीक',
}

SUPPORTED_LANGS = {'en', 'hi', 'kn', 'mr', 'ta', 'te'}

# Crop name dictionaries for Indian languages (fallback when Azure translation unavailable)
KN_CROP_NAMES = {
    'ಅಕ್ಕಿ': 'rice', 'ಭತ್ತ': 'rice', 'ಗೋಧಿ': 'wheat', 'ಮೆಕ್ಕೆಜೋಳ': 'maize',
    'ರಾಗಿ': 'ragi', 'ಸಿರಿಧಾನ್ಯ': 'millets', 'ಆಲೂಗಡ್ಡೆ': 'potato',
    'ಟೊಮೇಟೊ': 'tomato', 'ಟೊಮ್ಯಾಟೋ': 'tomato', 'ಈರುಳ್ಳಿ': 'onion',
    'ಬದನೆಕಾಯಿ': 'brinjal', 'ಎಲೆಕೋಸು': 'cabbage', 'ಹೂಕೋಸು': 'cauliflower',
    'ಕ್ಯಾರೆಟ್': 'carrot', 'ಮೂಲಂಗಿ': 'radish', 'ಪಾಲಕ್': 'spinach',
    'ಬಟಾಣಿ': 'peas', 'ಭಿಂಡಿ': 'okra', 'ಸೌತೆಕಾಯಿ': 'cucumber',
    'ಕುಂಬಳಕಾಯಿ': 'pumpkin', 'ಬಾಳೆ': 'banana', 'ಸೇಬು': 'apple',
    'ಮಾವು': 'mango', 'ದ್ರಾಕ್ಷಿ': 'grapes', 'ಪೇರಲ': 'guava',
    'ಪಪ್ಪಾಯಿ': 'papaya', 'ನಿಂಬೆ': 'lemon', 'ಕಿತ್ತಳೆ': 'orange',
    'ದಾಳಿಂಬೆ': 'pomegranate', 'ತೆಂಗಿನಕಾಯಿ': 'coconut', 'ಕಲ್ಲಂಗಡಿ': 'watermelon',
    'ಕರಬೂಜ': 'muskmelon', 'ಹತ್ತಿ': 'cotton', 'ಕಬ್ಬು': 'sugarcane',
    'ಚಹಾ': 'tea', 'ಕಾಫಿ': 'coffee', 'ಕಡಲೆಕಾಯಿ': 'groundnut',
    'ಸೋಯಾಬೀನ್': 'soybean', 'ಸಾಸಿವೆ': 'mustard', 'ಕಡಲೆ': 'chickpea',
    'ಮಸೂರ್': 'lentil', 'ಅರಿಶಿನ': 'turmeric', 'ಶುಂಠಿ': 'ginger',
    'ಬಾರ್ಲಿ': 'barley', 'ಸೆಣಬು': 'jute', 'ಎಳ್ಳು': 'sesame',
    'ಸೂರ್ಯಕಾಂತಿ': 'sunflower', 'ಹರಳು': 'castor',
    'ಹುರಳಿಕಾಯಿ': 'kidneybeans', 'ಅವರೆ': 'pigeonpeas', 'ಹೆಸರು': 'mungbean',
    'ತೊಗರಿ': 'mothbeans', 'ಬೀನ್ಸ್': 'beans',
}

TE_CROP_NAMES = {
    'వరి': 'rice', 'బియ్యం': 'rice', 'గోధుమ': 'wheat', 'మొక్కజొన్న': 'maize',
    'రాగులు': 'ragi', 'చిరుధాన్యం': 'millets', 'బంగాళాదుంప': 'potato',
    'టమోటా': 'tomato', 'ఉల్లిపాయ': 'onion', 'వంకాయ': 'brinjal',
    'క్యాబేజీ': 'cabbage', 'కాలీఫ్లవర్': 'cauliflower', 'క్యారెట్': 'carrot',
    'ముల్లంగి': 'radish', 'పాలకూర': 'spinach', 'బటానీ': 'peas',
    'భిండి': 'okra', 'దోసకాయ': 'cucumber', 'గుమ్మడికాయ': 'pumpkin',
    'అరటి': 'banana', 'ఆపిల్': 'apple', 'మామిడి': 'mango',
    'ద్రాక్ష': 'grapes', 'జామ': 'guava', 'బొప్పాయి': 'papaya',
    'నిమ్మకాయ': 'lemon', 'నారింజ': 'orange', 'దానిమ్మ': 'pomegranate',
    'కొబ్బరి': 'coconut', 'పుచ్చకాయ': 'watermelon', 'ఖర్బూజ': 'muskmelon',
    'పత్తి': 'cotton', 'చెరకు': 'sugarcane', 'టీ': 'tea', 'కాఫీ': 'coffee',
    'వేరుశెనగ': 'groundnut', 'సోయా': 'soybean', 'ఆవాలు': 'mustard',
    'సెనగలు': 'chickpea', 'మసూర్': 'lentil', 'పసుపు': 'turmeric',
    'అల్లం': 'ginger', 'బార్లీ': 'barley', 'జనప': 'jute',
    'నువ్వులు': 'sesame', 'సూర్యకాంతి': 'sunflower', 'ఆముదం': 'castor',
}

TA_CROP_NAMES = {
    'அரிசி': 'rice', 'நெல்': 'rice', 'கோதுமை': 'wheat', 'மக்காச்சோளம்': 'maize',
    'கேழ்வரகு': 'ragi', 'சிறுதானியம்': 'millets', 'உருளைக்கிழங்கு': 'potato',
    'தக்காளி': 'tomato', 'வெங்காயம்': 'onion', 'கத்தரி': 'brinjal',
    'கத்திரிக்காய்': 'brinjal', 'முட்டைகோஸ்': 'cabbage', 'காலிஃபிளவர்': 'cauliflower',
    'காரட்': 'carrot', 'முள்ளங்கி': 'radish', 'கீரை': 'spinach',
    'பட்டாணி': 'peas', 'வெண்டை': 'okra', 'வெள்ளரி': 'cucumber',
    'பூசணி': 'pumpkin', 'வாழை': 'banana', 'ஆப்பிள்': 'apple',
    'மாம்பழம்': 'mango', 'திராட்சை': 'grapes', 'ப்பாளி': 'guava',
    'ப்பாளி': 'papaya', 'எலுமிச்சை': 'lemon', 'ஆரஞ்சு': 'orange',
    'மாதுளை': 'pomegranate', 'தேங்காய்': 'coconut', 'தர்ப்பூசணி': 'watermelon',
    'முலாம்பழம்': 'muskmelon', 'ப்பருத்தி': 'cotton', 'கரும்பு': 'sugarcane',
    'தேயிலை': 'tea', 'காபி': 'coffee', 'வேர்க்கடலை': 'groundnut',
    'சோயா': 'soybean', 'கடுகு': 'mustard', 'கொண்டைக்கடலை': 'chickpea',
    'ப்பருப்பு': 'lentil', 'மஞ்சள்': 'turmeric', 'இஞ்சி': 'ginger',
    'ப்பார்லி': 'barley', 'சணல்': 'jute', 'எள்': 'sesame',
    'சூரியகாந்தி': 'sunflower', 'ஆமணக்கு': 'castor',
}

MR_CROP_NAMES = {
    'तांदूळ': 'rice', 'तांदळा': 'rice', 'भात': 'rice', 'गहू': 'wheat',
    'गव्हा': 'wheat', 'गव्हाचा': 'wheat', 'गव्हाला': 'wheat', 'मका': 'maize', 'मक्याचा': 'maize',
    'नाचणी': 'ragi', 'बाजरी': 'millets', 'बटाटा': 'potato',
    'टोमॅटो': 'tomato', 'कांदा': 'onion', 'वांगी': 'brinjal',
    'कोबी': 'cabbage', 'फुलकोबी': 'cauliflower', 'गाजर': 'carrot',
    'मुळा': 'radish', 'पालक': 'spinach', 'वाटाणे': 'peas',
    'भेंडी': 'okra', 'काकडी': 'cucumber', 'भोपळा': 'pumpkin',
    'केळी': 'banana', 'सफरचंद': 'apple', 'आंबा': 'mango',
    'द्राक्षे': 'grapes', 'पेरू': 'guava', 'पपई': 'papaya',
    'लिंबू': 'lemon', 'संत्रे': 'orange', 'डाळिंब': 'pomegranate',
    'नारळ': 'coconut', 'कलिंगड': 'watermelon', 'खरबूज': 'muskmelon',
    'कापूस': 'cotton', 'ऊस': 'sugarcane', 'चहा': 'tea', 'कॉफी': 'coffee',
    'शेंगदाणा': 'groundnut', 'सोयाबीन': 'soybean', 'मोहरी': 'mustard',
    'हरबरा': 'chickpea', 'चणा': 'chickpea', 'मसूर': 'lentil',
    'हळद': 'turmeric', 'आले': 'ginger', 'जव': 'barley',
    'ताग': 'jute', 'तीळ': 'sesame', 'सूर्यफूल': 'sunflower',
    'एरंडी': 'castor',
}

# All non-Hindi language crop name maps
LANG_CROP_MAP = {
    'kn': KN_CROP_NAMES,
    'te': TE_CROP_NAMES,
    'ta': TA_CROP_NAMES,
    'mr': MR_CROP_NAMES,
}

_TRANSLATE_CACHE = {}

def _azure_translate(text, to_lang, from_lang=None):
    """Translate text. Uses Azure Translator if TRANSLATOR_KEY is set, else falls back to Google Translate (free)."""
    if not text:
        return None
    cache_key = f'{from_lang or "auto"}:{to_lang}:{text}'
    cached = _TRANSLATE_CACHE.get(cache_key)
    if cached:
        return cached
    translator_key = os.getenv('TRANSLATOR_KEY')
    translator_region = os.getenv('TRANSLATOR_REGION', 'global')
    # Try Azure if configured
    if translator_key and translator_key != 'your-azure-translator-key':
        import urllib.request, urllib.error
        url = f'https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&to={to_lang}'
        if from_lang:
            url += f'&from={from_lang}'
        body = json.dumps([{'Text': text}]).encode('utf-8')
        req = urllib.request.Request(url, data=body, method='POST')
        req.add_header('Ocp-Apim-Subscription-Key', translator_key)
        req.add_header('Ocp-Apim-Subscription-Region', translator_region)
        req.add_header('Content-Type', 'application/json')
        try:
            resp = urllib.request.urlopen(req, timeout=15)
            results = json.loads(resp.read().decode('utf-8'))
            result = results[0]['translations'][0]['text']
            _TRANSLATE_CACHE[cache_key] = result
            return result
        except Exception as e:
            print(f"[ERR] Azure translate failed: {e}")
    # Fallback: use Google Translate (free, no API key required)
    try:
        from deep_translator import GoogleTranslator
        source = from_lang if from_lang else 'auto'
        result = GoogleTranslator(source=source, target=to_lang).translate(text)
        if result:
            _TRANSLATE_CACHE[cache_key] = result
            return result
    except Exception as e:
        print(f"[ERR] Google translate fallback failed: {e}")
    return None


@app.after_request
def translate_chat_response(response):
    """After-request hook: translate /api/chat responses, preserving crop names."""
    if request.path == '/api/chat' and response.status_code == 200 and response.content_type and 'application/json' in response.content_type:
        try:
            data = response.get_json()
            if data and data.get('success') and data.get('response'):
                req_data = request.get_json(silent=True) or {}
                lang = req_data.get('language', 'en')
                if lang != 'en' and lang in SUPPORTED_LANGS:
                    text = data['response']
                    # Replace crop names with placeholders so Google Translate doesn't mangle them (e.g., fig → ಚಿತ್ರ)
                    placeholder_map = {}
                    for crop_key in sorted(CROP_INFO.keys(), key=len, reverse=True):
                        name = crop_key.title()
                        if name in text:
                            pid = f'__CRP_{len(placeholder_map)}__'
                            native = CROP_NATIVE_NAMES.get(lang, {}).get(crop_key, name)
                            placeholder_map[pid] = native
                            text = text.replace(name, pid)
                    trans = _azure_translate(text, lang)
                    if trans:
                        for pid, native_name in placeholder_map.items():
                            trans = trans.replace(pid, native_name)
                        data['response'] = trans
                        response.set_data(json.dumps(data, ensure_ascii=False))
        except Exception as e:
            print(f"[ERR] after_request translate failed: {e}")
    return response


@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        message = data.get('message', '').strip()
        lang = data.get('language', 'en')
        if lang not in SUPPORTED_LANGS:
            lang = 'en'

        if not message:
            return jsonify({'success': True, 'response': _chat_greeting(lang), 'intent': 'GREETING'})

        # For non-English languages: translate user message to English for processing
        # Uses 'auto' source so English input works even when page is in Kannada/etc.
        if lang != 'en':
            eng_msg = _azure_translate(message, 'en')
            if eng_msg:
                message = eng_msg

        msg_lower = message.lower()
        pi = PROJECT_INFO.get(lang if lang in PROJECT_INFO else 'en', {})
        ak = AGRICULTURE_KNOWLEDGE.get(lang if lang in AGRICULTURE_KNOWLEDGE else 'en', {})

        # 1. Check for project-related queries
        import re as re_mod

        for key, pattern in PROJECT_PATTERNS.items():
            if re_mod.search(pattern, msg_lower):
                if key == 'what_is':
                    resp = f"**🌾 {pi['name']} - {pi['tagline']}**\n\n{pi['description']}\n\n**✨ Key Features:**\n" + "\n".join(f"• {f}" for f in pi['features'][:5])
                    return jsonify({'success': True, 'response': resp, 'intent': 'PROJECT'})
                elif key == 'features':
                    resp = f"**✨ {pi['name']} Features**\n\n" + "\n".join(f"• {f}" for f in pi['features'])
                    return jsonify({'success': True, 'response': resp, 'intent': 'PROJECT'})
                elif key == 'how_to_use':
                    resp = f"**📖 How to Use {pi['name']}**\n\n" + "\n".join(pi['how_to_use'])
                    return jsonify({'success': True, 'response': resp, 'intent': 'PROJECT'})
                elif key == 'tech':
                    resp = f"**🔧 Technology**\n\n{pi['tech']}\n\n🌾 The ML model achieves **97.5% accuracy** using Random Forest classifier trained on 216,000 samples across 72 crops."
                    return jsonify({'success': True, 'response': resp, 'intent': 'PROJECT'})
                elif key == 'accuracy':
                    import json as json_mod
                    try:
                        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'model_metrics.json')) as f:
                            m = json_mod.load(f)
                        resp = f"**📊 Model Accuracy: {m.get('accuracy', '97.5')}%**\n\n🎯 Precision: {m.get('precision', '0.976')}\n📈 Recall: {m.get('recall', '0.975')}\n🔢 F1 Score: {m.get('f1_score', '0.975')}\n🌾 Crops: {m.get('total_crops', 72)}\n📚 Training Samples: {m.get('training_samples', '172,800')}\n🧠 Algorithm: {m.get('algorithm', 'Random Forest')}"
                    except:
                        resp = "**📊 Model Accuracy: 97.5%** (Random Forest, 72 crops, 216K samples)"
                    return jsonify({'success': True, 'response': resp, 'intent': 'PROJECT'})

        # 2. Extract crop name from message (English + Hindi)
        HINDI_CROP_NAMES = {
            'चावल': 'rice', 'धान': 'rice', 'गेहूं': 'wheat', 'गेहूँ': 'wheat',
            'मक्का': 'maize', 'आलू': 'potato', 'टमाटर': 'tomato', 'प्याज': 'onion',
            'कपास': 'cotton', 'गन्ना': 'sugarcane', 'चाय': 'tea', 'कॉफी': 'coffee',
            'मूंगफली': 'groundnut', 'सोयाबीन': 'soybean', 'सरसों': 'mustard',
            'केला': 'banana', 'आम': 'mango', 'सेब': 'apple', 'अंगूर': 'grapes',
            'संतरा': 'orange', 'अनार': 'pomegranate', 'पपीता': 'papaya',
            'नारियल': 'coconut', 'तरबूज': 'watermelon', 'खरबूज': 'muskmelon',
            'चना': 'chickpea', 'मसूर': 'lentil', 'बैंगन': 'brinjal',
            'पत्ता गोभी': 'cabbage', 'फूल गोभी': 'cauliflower', 'गाजर': 'carrot',
            'मूली': 'radish', 'पालक': 'spinach', 'मटर': 'peas',
            'भिंडी': 'okra', 'खीरा': 'cucumber', 'कद्दू': 'pumpkin',
            'हल्दी': 'turmeric', 'अदरक': 'ginger', 'जौ': 'barley',
            'जूट': 'jute', 'तिल': 'sesame', 'सूरजमुखी': 'sunflower',
            'अरंडी': 'castor', 'रागी': 'ragi',
        }

        crop_match = None
        # Check Hindi names first
        for hindi_name, eng_name in HINDI_CROP_NAMES.items():
            if hindi_name in message:
                crop_match = eng_name
                break
        # Check other Indian language names (fallback when Azure translation unavailable)
        if not crop_match and lang in LANG_CROP_MAP:
            for native_name, eng_name in LANG_CROP_MAP[lang].items():
                if native_name in message:
                    crop_match = eng_name
                    break
        # Check English names
        if not crop_match:
            all_crops = sorted(CROP_INFO.keys(), key=len, reverse=True)
            msg_nospace = msg_lower.replace(' ', '')
            for c in all_crops:
                if c in msg_lower or c in msg_nospace:
                    crop_match = c
                    break

        # Check aliases for common misspellings
        if not crop_match:
            CROP_ALIASES = {
                'bitter guard': 'bittergourd', 'bitter gourd': 'bittergourd',
                'bottle guard': 'bottlegourd', 'bottle gourd': 'bottlegourd',
                'cauli flower': 'cauliflower', 'sweet potato': 'sweetpotato',
                'ground nut': 'groundnut', 'horse gram': 'horsegram',
                'pigeon pea': 'pigeonpea', 'pigeonpeas': 'pigeonpea',
                'kidney beans': 'kidneybeans', 'moth beans': 'mothbeans',
                'mung bean': 'mungbean', 'mung beans': 'mungbean',
                'black gram': 'blackgram', 'green gram': 'greengram',
                'chickoo': 'sapota', 'aloe vera': 'aloe_vera',
                'cabbage': 'cabbage', 'brinjal': 'brinjal',
                'fenugreek': 'fenugreek',
            }
            for alias, actual in CROP_ALIASES.items():
                if alias in msg_lower:
                    crop_match = actual
                    break

        # 3. Handle crop-specific queries (BEFORE general concepts)
        if crop_match:
            info = CROP_INFO.get(crop_match, {})

            # Price query
            if re_mod.search(CROP_QUERY_PATTERNS['price'], msg_lower):
                price = info.get('price', 0)
                resp = f"💰 **{crop_match.title()} - Market Price**\n\n📊 Current Price: **₹{price:,}/quintal**\n📅 Season: {info.get('season', 'N/A')}\n💡 Prices vary by region and demand."
                return jsonify({'success': True, 'response': resp, 'intent': 'PRICE'})

            # Soil query
            if re_mod.search(CROP_QUERY_PATTERNS['soil'], msg_lower):
                resp = f"🪴 **Soil Requirements for {crop_match.title()}**\n\n[OK] Suitable Soil: {info.get('soil', 'Loamy')}\n🌡 Temp: {info.get('min_temp', 'N/A')}-{info.get('max_temp', 'N/A')}°C\n🌧 Rainfall: {info.get('min_rain', 'N/A')}-{info.get('max_rain', 'N/A')}mm"
                return jsonify({'success': True, 'response': resp, 'intent': 'SOIL'})

            # Fertilizer/NPK query
            if re_mod.search(CROP_QUERY_PATTERNS['fertilizer'], msg_lower):
                resp = f"🧪 **Fertilizer for {crop_match.title()}**\n\n📊 Recommended: {info.get('fert', 'Standard fertilizer')}\n💡 Apply based on soil test results for best yields."
                return jsonify({'success': True, 'response': resp, 'intent': 'FERTILIZER'})

            # Season query
            if re_mod.search(CROP_QUERY_PATTERNS['season'], msg_lower):
                resp = f"📅 **{crop_match.title()} Growing Season**\n\n🌾 Season: {info.get('season', 'General')}\n🌡 Temperature: {info.get('min_temp', 'N/A')}-{info.get('max_temp', 'N/A')}°C\n🌧 Rainfall: {info.get('min_rain', 'N/A')}-{info.get('max_rain', 'N/A')}mm"
                return jsonify({'success': True, 'response': resp, 'intent': 'SEASON'})

            # Disease query
            if re_mod.search(CROP_QUERY_PATTERNS['disease'], msg_lower):
                detailed = get_crop_diseases_info(crop_match, info)
                if detailed:
                    return jsonify({'success': True, 'response': detailed, 'intent': 'DISEASE'})

            # Pest query
            if re_mod.search(CROP_QUERY_PATTERNS['pest'], msg_lower):
                detailed = get_crop_pests_info(crop_match, info)
                if detailed:
                    return jsonify({'success': True, 'response': detailed, 'intent': 'PEST'})

            # Variety query
            if re_mod.search(CROP_QUERY_PATTERNS['variety'], msg_lower):
                detailed = get_crop_varieties_info(crop_match, info)
                if detailed:
                    return jsonify({'success': True, 'response': detailed, 'intent': 'VARIETY'})

            # Growing period query
            if re_mod.search(CROP_QUERY_PATTERNS['growing'], msg_lower):
                detailed = get_crop_growing_info(crop_match, info)
                if detailed:
                    return jsonify({'success': True, 'response': detailed, 'intent': 'GROWING'})

            # NPK range query (within crop context)
            if re_mod.search(r'npk|nitrogen|phosphorus|potassium|एनपीके|ಎನ್ಪಿಕೆ|పొటాష్|సారజనక|मातीचे पोषक', msg_lower):
                detailed = get_crop_npk_info(crop_match, info)
                if detailed:
                    return jsonify({'success': True, 'response': detailed, 'intent': 'NPK_RANGE'})

            # General crop info (default for crop mentions)
            soil_info = info.get('soil', 'Loamy')
            season = info.get('season', 'General')
            fert = info.get('fert', 'Standard')
            price = info.get('price', 0)
            resp = (
                f"{info.get('icon', '🌾')} **{crop_match.title()} - Complete Guide**\n\n"
                f"📅 **Season:** {season}\n"
                f"🌡 **Temperature:** {info.get('min_temp', 'N/A')}-{info.get('max_temp', 'N/A')}°C\n"
                f"🌧 **Rainfall:** {info.get('min_rain', 'N/A')}-{info.get('max_rain', 'N/A')}mm\n"
                f"🪴 **Soil:** {soil_info}\n"
                f"💰 **Price:** ₹{price:,}/quintal\n"
                f"🧪 **Fertilizer:** {fert}\n\n"
                f"💡 Ask me about price, soil, NPK, season, or diseases for {crop_match.title()}!"
            )
            return jsonify({'success': True, 'response': resp, 'intent': 'CROP_INFO'})

        # 4. Crops by season (before concept patterns for priority)
        if re_mod.search(r'(what|which|कौन|क्या).*(grow|crop|plant|उगाएं|बोएं|फसल).*(kharif|rabi|zaid|खरीफ|रबी|ज़ायद)|(kharif|rabi|zaid|खरीफ|रबी|ज़ायद).*crop|^crops (for|of) (kharif|rabi|zaid|खरीफ|रबी|ज़ायद)|(kharif|rabi|zaid|खरीफ|रबी|ज़ायद).*(क्या|कौन).*(उगाएं|बोएं|फसल)', msg_lower):
            season_map = {'kharif': [], 'rabi': [], 'zaid': []}
            for c, inf in CROP_INFO.items():
                s = (inf.get('season') or '').lower()
                if 'kharif' in s:
                    season_map['kharif'].append(c)
                if 'rabi' in s:
                    season_map['rabi'].append(c)
                if 'zaid' in s:
                    season_map['zaid'].append(c)
            matched_season = None
            for s in ['kharif', 'rabi', 'zaid']:
                if s in msg_lower or (lang == 'hi' and {'kharif': 'खरीफ', 'rabi': 'रबी', 'zaid': 'ज़ायद'}[s] in message):
                    matched_season = s
                    break
            if not matched_season:
                for s_k, s_v in {'kharif': 'खरीफ', 'rabi': 'रबी', 'zaid': 'ज़ायद'}.items():
                    if s_v in message:
                        matched_season = s_k
                        break
            if matched_season:
                crops_list = season_map[matched_season][:15]
                season_name = matched_season.title()
                resp = f"🌧 **{season_name} Season Crops**\n\n" + ", ".join(f"{CROP_INFO.get(c, {}).get('icon', '🌾')} {c.title()}" for c in crops_list)
                return jsonify({'success': True, 'response': resp, 'intent': 'SEASON_CROPS'})

        # 5. Crops by soil type (before concept patterns for priority)
        if re_mod.search(r'(what|which|कौन|क्या).*(grow|crop|plant|उगाएं|बोएं).*(clay|loamy|sandy|alluvial|black|red|मिट्टी)|(clay|loamy|sandy|alluvial|black).*crop|^crops (for|in|of) (clay|loamy|sandy|alluvial|black)', msg_lower):
            soil_query = None
            for soil_type in ['clay', 'loamy', 'sandy', 'alluvial', 'black']:
                if soil_type in msg_lower:
                    soil_query = soil_type
                    break
            if soil_query:
                matching = []
                for c, inf in CROP_INFO.items():
                    s = (inf.get('soil') or '').lower()
                    if soil_query in s:
                        matching.append(c)
                if matching:
                    resp = f"🪴 **Crops for {soil_query.title()} Soil**\n\n" + ", ".join(f"{CROP_INFO.get(c, {}).get('icon', '🌾')} {c.title()}" for c in matching[:15])
                    return jsonify({'success': True, 'response': resp, 'intent': 'SOIL_CROPS'})

        # 6. Check for agriculture concept queries
        for key in CONCEPT_PATTERNS:
            if re_mod.search(CONCEPT_PATTERNS[key], msg_lower):
                if key == 'npk':
                    return jsonify({'success': True, 'response': ak['npk'], 'intent': 'CONCEPT'})
                elif key == 'ph':
                    return jsonify({'success': True, 'response': ak['ph'], 'intent': 'CONCEPT'})
                elif key == 'seasons':
                    return jsonify({'success': True, 'response': ak['seasons'], 'intent': 'CONCEPT'})
                elif key == 'soil_types':
                    return jsonify({'success': True, 'response': ak['soil_types'], 'intent': 'CONCEPT'})
                elif key == 'irrigation':
                    return jsonify({'success': True, 'response': ak['irrigation'], 'intent': 'CONCEPT'})
                elif key == 'crop_rotation':
                    return jsonify({'success': True, 'response': ak['crop_rotation'], 'intent': 'CONCEPT'})

        # 7. Greeting (Hindi Unicode fix: no \b for Hindi)
        if re_mod.search(r'^(hi|hello|hey|namaste)\b', msg_lower) or \
           any(g in message for g in ['नमस्ते', 'नमस्कार', 'हाय']):
            return jsonify({'success': True, 'response': _chat_greeting(lang), 'intent': 'GREETING'})

        # 8. Help
        if re_mod.search(r'help|what can you do|सहायता|क्या कर सकते हैं', msg_lower):
            return jsonify({'success': True, 'response': _chat_help(lang), 'intent': 'HELP'})

        # 9. Thank you
        if re_mod.search(r'thanks|thank you|धन्यवाद|शुक्रिया', msg_lower):
            thank_text = "आपका स्वागत है! 😊 खेती की शुभकामनाएं! 🌾" if lang == 'hi' else "You're welcome! 😊 Happy farming! 🌾"
            return jsonify({'success': True, 'response': thank_text, 'intent': 'THANKS'})

        # 10. Weather-related
        if re_mod.search(r'weather|मौसम|temperature|तापमान|rainfall|वर्षा', msg_lower):
            resp = "🌤 I can help with crop recommendations based on your local weather conditions.\n\n💡 Go to the dashboard, enter your temperature, humidity, and rainfall data, and click **Get Recommendation** for personalized crop suggestions!"
            if lang == 'hi':
                resp = "🌤 मैं आपकी स्थानीय मौसम की स्थितियों के आधार पर फसल अनुशंसाओं में मदद कर सकता हूं।\n\n💡 डैशबोर्ड पर जाएं, अपना तापमान, आर्द्रता और वर्षा डेटा दर्ज करें, और व्यक्तिगत फसल सुझावों के लिए **अनुशंसा प्राप्त करें** पर क्लिक करें!"
            return jsonify({'success': True, 'response': resp, 'intent': 'WEATHER'})

        # 11. Disease/pest name lookup (standalone queries like "blast", "what is blight")
        from crop_knowledge import CROP_DETAILED as _CD
        disease_hits = {}
        pest_hits = {}
        for cname, cdata in _CD.items():
            for d in cdata.get('diseases', []):
                if d.lower() in msg_lower:
                    disease_hits.setdefault(d, []).append(cname)
            for p in cdata.get('pests', []):
                if p.lower() in msg_lower:
                    pest_hits.setdefault(p, []).append(cname)
        if disease_hits or pest_hits:
            lines = []
            if disease_hits:
                for d, crops in sorted(disease_hits.items()):
                    lines.append(f"🦠 **{d}** affects: {', '.join(c.title() for c in crops)}")
            if pest_hits:
                for p, crops in sorted(pest_hits.items()):
                    lines.append(f"🐛 **{p}** affects: {', '.join(c.title() for c in crops)}")
            resp = "🌾 **Disease & Pest Information**\n\n" + "\n\n".join(lines) + "\n\n💡 Ask 'rice diseases' for detailed management tips!"
            return jsonify({'success': True, 'response': resp, 'intent': 'DISEASE_PEST'})

        # 12. Default: unknown query
        resp = _chat_default(lang)
        return jsonify({'success': True, 'response': resp, 'intent': 'UNKNOWN'})

    except Exception as e:
        print(f"Chat error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


def _chat_greeting(lang):
    if lang == 'hi':
        return (
            "🌾 **नमस्ते! मैं CropSense सहायक हूं** 🌾\n\n"
            "मैं आपकी मदद कर सकता हूं:\n\n"
            "🌱 **फसलें:** \"चावल की जानकारी\", \"गेहूं के बारे में बताएं\"\n"
            "💰 **कीमतें:** \"चावल का दाम\", \"गेहूं का रेट\"\n"
            "🪴 **मिट्टी:** \"चावल के लिए मिट्टी\", \"गेहूं के लिए कौन सी मिट्टी\"\n"
            "🧪 **उर्वरक:** \"चावल के लिए NPK\", \"गेहूं के लिए खाद\"\n"
            "📅 **मौसम:** \"खरीफ में क्या उगाएं\", \"रबी फसलें\"\n"
            "[INFO] **प्रोजेक्ट:** \"CropSense क्या है\", \"इसका उपयोग कैसे करें\"\n\n"
            "💡 \"सहायता\" टाइप करें पूरी गाइड के लिए!"
        )
    return (
        "🌾 **Namaste! I'm CropSense Assistant** 🌾\n\n"
        "I can help you with:\n\n"
        "🌱 **Crops:** \"Tell me about rice\", \"Wheat information\"\n"
        "💰 **Prices:** \"Price of rice\", \"Wheat rate\"\n"
        "🪴 **Soil:** \"Soil for rice\", \"What soil for wheat\"\n"
        "🧪 **Fertilizer:** \"NPK for rice\", \"Fertilizer for wheat\"\n"
        "📅 **Seasons:** \"What to grow in Kharif\", \"Rabi crops\"\n"
        "🌍 **Agriculture:** \"What is NPK\", \"Soil types\", \"Crop rotation\"\n"
        "[INFO] **Project:** \"What is CropSense\", \"How to use\"\n\n"
        "💡 Type \"help\" for the full guide!"
    )


def _chat_help(lang):
    if lang == 'hi':
        return (
            "🌾 **CropSense सहायक - पूरी गाइड**\n\n"
            "**🌱 फसल जानकारी**\n"
            "• \"चावल की जानकारी\" - पूरी फसल जानकारी\n"
            "• \"गेहूं के बारे में बताएं\" - खेती गाइड\n\n"
            "**💰 कीमत पूछताछ**\n"
            "• \"चावल का दाम\" - बाजार मूल्य\n"
            "• \"गेहूं का रेट क्या है\" - मौजूदा दाम\n\n"
            "**🪴 मिट्टी और उर्वरक**\n"
            "• \"चावल के लिए मिट्टी\" - मिट्टी की आवश्यकता\n"
            "• \"गेहूं के लिए NPK\" - खाद की जानकारी\n\n"
            "**📅 मौसम और फसलें**\n"
            "• \"खरीफ में क्या उगाएं\" - मौसमी फसलें\n"
            "• \"रबी फसलों की सूची\" - रबी फसलें\n\n"
            "**🌍 कृषि ज्ञान**\n"
            "• \"NPK क्या है\" - पोषक तत्व\n"
            "• \"मिट्टी के प्रकार\" - मिट्टी वर्गीकरण\n"
            "• \"फसल चक्र\" - फसल चक्र के लाभ\n\n"
            "**[INFO] प्रोजेक्ट**\n"
            "• \"CropSense क्या है\" - प्रोजेक्ट जानकारी\n"
            "• \"सुविधाएं\" - सभी सुविधाएं\n"
            "• \"सटीकता\" - मॉडल सटीकता"
        )
    return (
        "🌾 **CropSense Assistant - Full Guide**\n\n"
        "**🌱 CROP INFORMATION**\n"
        "• \"Tell me about rice\" - Complete crop guide\n"
        "• \"Wheat information\" - Cultivation details\n\n"
        "**💰 PRICE QUERIES**\n"
        "• \"Price of rice\" - Market price\n"
        "• \"What is the rate of wheat\" - Current price\n\n"
        "**🪴 SOIL & FERTILIZER**\n"
        "• \"Soil for rice\" - Soil requirements\n"
        "• \"NPK for wheat\" - Fertilizer info\n\n"
        "**📅 SEASONS & CROPS**\n"
        "• \"What to grow in Kharif\" - Seasonal crops\n"
        "• \"Rabi crops list\" - Winter crops\n\n"
        "**🌍 AGRICULTURE KNOWLEDGE**\n"
        "• \"What is NPK\" - Plant nutrients\n"
        "• \"Soil types\" - Soil classification\n"
        "• \"Crop rotation\" - Rotation benefits\n"
        "• \"Irrigation methods\" - Water management\n\n"
        "**[INFO] PROJECT INFO**\n"
        "• \"What is CropSense\" - Project overview\n"
        "• \"Features\" - All features\n"
        "• \"How to use\" - Getting started\n"
        "• \"Accuracy\" - Model performance"
    )


def _chat_default(lang):
    if lang == 'hi':
        return (
            "🌾 मुझे इसके बारे में पूरी जानकारी नहीं है।\n\n"
            "💡 **कुछ इस तरह पूछें:**\n"
            "• \"चावल की जानकारी\" - फसल विवरण\n"
            "• \"NPK क्या है\" - कृषि ज्ञान\n"
            "• \"CropSense क्या है\" - प्रोजेक्ट जानकारी\n"
            "• \"खरीफ में क्या उगाएं\" - मौसमी फसलें\n\n"
            "पूरी गाइड के लिए \"सहायता\" टाइप करें! 🌾"
        )
    return (
        "🌾 I'm not sure about that.\n\n"
        "💡 **Try asking:**\n"
        "• \"Tell me about rice\" - Crop details\n"
        "• \"What is NPK\" - Agriculture knowledge\n"
        "• \"What is CropSense\" - Project info\n"
        "• \"What to grow in Kharif\" - Seasonal crops\n"
        "• \"Price of wheat\" - Market rates\n\n"
        'Type "help" for the full guide! 🌾'
    )


# ============================================
# TRANSLATION API (Microsoft Translator)
# ============================================

@app.route('/api/translate', methods=['POST'])
def translate():
    try:
        data = request.json
        texts = data.get('texts', [])
        to_lang = data.get('to', 'hi')
        from_lang = data.get('from', 'en')

        if not texts:
            return jsonify({'error': 'No texts provided'}), 400

        translated = []
        for t in texts:
            result = _azure_translate(t, to_lang, from_lang)
            if result is None:
                return jsonify({'error': 'Translation failed. Check network or try again.'}), 502
            translated.append(result)
        return jsonify({'translations': translated})

    except Exception as e:
        print(f"[ERR] Translation failed: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)