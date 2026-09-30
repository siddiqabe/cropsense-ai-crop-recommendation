# generate_full_dataset.py
# Complete dataset generator for CropSense - 72 crops with 500 samples each (36,000 total samples)

import pandas as pd
import numpy as np
import random
import os

# Create dataset directory if not exists
os.makedirs('dataset', exist_ok=True)

print("=" * 60)
print("🌾 CROP SENSE - FULL DATASET GENERATOR")
print("=" * 60)

# ============================================
# COMPLETE CROP DATABASE WITH 72+ CROPS
# ============================================

crops_data = {
    # ========== CEREALS ==========
    'rice': {
        'N': (80, 120), 'P': (40, 60), 'K': (40, 60),
        'temp': (20, 35), 'humidity': (70, 85), 'ph': (5.0, 7.0), 'rain': (100, 300),
        'season': 'Kharif', 'icon': '🌾', 'price': 4024
    },
    'wheat': {
        'N': (80, 120), 'P': (40, 60), 'K': (30, 50),
        'temp': (10, 25), 'humidity': (60, 75), 'ph': (6.0, 7.5), 'rain': (50, 150),
        'season': 'Rabi', 'icon': '🌿', 'price': 2164
    },
    'maize': {
        'N': (100, 150), 'P': (50, 70), 'K': (40, 60),
        'temp': (18, 32), 'humidity': (65, 80), 'ph': (5.5, 7.0), 'rain': (50, 120),
        'season': 'Kharif', 'icon': '🌽', 'price': 1700
    },
    'millets': {
        'N': (40, 60), 'P': (30, 50), 'K': (20, 40),
        'temp': (25, 35), 'humidity': (60, 75), 'ph': (5.5, 7.5), 'rain': (30, 70),
        'season': 'Kharif', 'icon': '🌾', 'price': 3100
    },
    'ragi': {
        'N': (40, 60), 'P': (40, 60), 'K': (20, 40),
        'temp': (20, 35), 'humidity': (65, 80), 'ph': (5.5, 7.5), 'rain': (50, 100),
        'season': 'Kharif', 'icon': '🌾', 'price': 3934
    },
    'barley': {
        'N': (60, 100), 'P': (30, 50), 'K': (30, 50),
        'temp': (12, 25), 'humidity': (55, 70), 'ph': (6.0, 7.5), 'rain': (40, 80),
        'season': 'Rabi', 'icon': '🌾', 'price': 2500
    },
    
    # ========== VEGETABLES ==========
    'potato': {
        'N': (100, 150), 'P': (60, 90), 'K': (100, 150),
        'temp': (15, 25), 'humidity': (70, 85), 'ph': (5.0, 6.5), 'rain': (50, 120),
        'season': 'Rabi', 'icon': '🥔', 'price': 1240
    },
    'tomato': {
        'N': (100, 150), 'P': (60, 80), 'K': (60, 80),
        'temp': (20, 30), 'humidity': (70, 85), 'ph': (6.0, 7.0), 'rain': (50, 100),
        'season': 'Zaid', 'icon': '🍅', 'price': 1848
    },
    'onion': {
        'N': (80, 120), 'P': (40, 60), 'K': (60, 80),
        'temp': (15, 30), 'humidity': (65, 80), 'ph': (6.0, 7.5), 'rain': (50, 100),
        'season': 'Rabi', 'icon': '🧅', 'price': 1728
    },
    'brinjal': {
        'N': (80, 120), 'P': (40, 60), 'K': (60, 80),
        'temp': (21, 27), 'humidity': (70, 85), 'ph': (5.5, 7.0), 'rain': (60, 100),
        'season': 'Zaid', 'icon': '🍆', 'price': 2660
    },
    'cabbage': {
        'N': (100, 150), 'P': (40, 60), 'K': (60, 80),
        'temp': (15, 21), 'humidity': (70, 85), 'ph': (6.0, 7.0), 'rain': (50, 100),
        'season': 'Rabi', 'icon': '🥬', 'price': 1631
    },
    'cauliflower': {
        'N': (100, 150), 'P': (40, 60), 'K': (60, 80),
        'temp': (15, 21), 'humidity': (70, 85), 'ph': (6.0, 7.0), 'rain': (50, 100),
        'season': 'Rabi', 'icon': '🥦', 'price': 2572
    },
    'spinach': {
        'N': (60, 80), 'P': (40, 50), 'K': (40, 60),
        'temp': (10, 21), 'humidity': (65, 80), 'ph': (6.0, 7.5), 'rain': (40, 80),
        'season': 'Rabi', 'icon': '🌿', 'price': 1280
    },
    'carrot': {
        'N': (80, 120), 'P': (40, 60), 'K': (60, 80),
        'temp': (14, 26), 'humidity': (65, 80), 'ph': (6.0, 7.0), 'rain': (50, 100),
        'season': 'Rabi', 'icon': '🥕', 'price': 3294
    },
    'beetroot': {
        'N': (80, 120), 'P': (40, 60), 'K': (60, 80),
        'temp': (12, 23), 'humidity': (65, 80), 'ph': (6.0, 7.5), 'rain': (50, 100),
        'season': 'Rabi', 'icon': '🟣', 'price': 3584
    },
    'radish': {
        'N': (60, 80), 'P': (40, 60), 'K': (40, 60),
        'temp': (18, 24), 'humidity': (65, 80), 'ph': (6.0, 7.0), 'rain': (40, 80),
        'season': 'Rabi', 'icon': '⚪', 'price': 2321
    },
    'peas': {
        'N': (40, 60), 'P': (40, 60), 'K': (30, 50),
        'temp': (10, 18), 'humidity': (65, 80), 'ph': (6.0, 7.5), 'rain': (40, 80),
        'season': 'Rabi', 'icon': '🟢', 'price': 5168
    },
    'okra': {
        'N': (80, 120), 'P': (40, 60), 'K': (40, 60),
        'temp': (24, 32), 'humidity': (70, 85), 'ph': (6.0, 7.0), 'rain': (60, 100),
        'season': 'Kharif', 'icon': '🌿', 'price': 2500
    },
    'pumpkin': {
        'N': (80, 120), 'P': (40, 60), 'K': (60, 80),
        'temp': (18, 29), 'humidity': (70, 85), 'ph': (6.0, 7.5), 'rain': (80, 120),
        'season': 'Kharif', 'icon': '🎃', 'price': 1580
    },
    'cucumber': {
        'N': (80, 100), 'P': (40, 50), 'K': (40, 60),
        'temp': (21, 28), 'humidity': (70, 85), 'ph': (6.0, 7.0), 'rain': (50, 100),
        'season': 'Zaid', 'icon': '🥒', 'price': 2250
    },
    'watermelon': {
        'N': (80, 100), 'P': (40, 50), 'K': (40, 50),
        'temp': (21, 29), 'humidity': (70, 85), 'ph': (6.0, 7.0), 'rain': (40, 60),
        'season': 'Zaid', 'icon': '🍉', 'price': 1526
    },
    'capsicum': {
        'N': (100, 150), 'P': (40, 60), 'K': (60, 80),
        'temp': (18, 25), 'humidity': (70, 85), 'ph': (6.0, 7.0), 'rain': (50, 80),
        'season': 'Zaid', 'icon': '🫑', 'price': 3189
    },
    
    # ========== FRUITS ==========
    'banana': {
        'N': (150, 250), 'P': (60, 100), 'K': (100, 200),
        'temp': (25, 30), 'humidity': (75, 85), 'ph': (6.0, 7.5), 'rain': (90, 120),
        'season': 'Zaid', 'icon': '🍌', 'price': 3639
    },
    'mango': {
        'N': (80, 120), 'P': (40, 60), 'K': (60, 80),
        'temp': (18, 35), 'humidity': (60, 80), 'ph': (5.5, 7.5), 'rain': (50, 100),
        'season': 'Zaid', 'icon': '🥭', 'price': 35000
    },
    'grapes': {
        'N': (100, 150), 'P': (50, 70), 'K': (60, 80),
        'temp': (25, 32), 'humidity': (60, 75), 'ph': (6.0, 7.5), 'rain': (65, 90),
        'season': 'Zaid', 'icon': '🍇', 'price': 8942
    },
    'apple': {
        'N': (100, 150), 'P': (60, 80), 'K': (80, 120),
        'temp': (15, 25), 'humidity': (65, 80), 'ph': (5.5, 6.5), 'rain': (50, 100),
        'season': 'Rabi', 'icon': '🍎', 'price': 12871
    },
    'papaya': {
        'N': (100, 150), 'P': (50, 80), 'K': (50, 80),
        'temp': (23, 43), 'humidity': (70, 85), 'ph': (6.0, 7.0), 'rain': (40, 250),
        'season': 'Zaid', 'icon': '🍈', 'price': 3087
    },
    'guava': {
        'N': (80, 100), 'P': (40, 50), 'K': (60, 80),
        'temp': (18, 32), 'humidity': (70, 85), 'ph': (5.5, 7.5), 'rain': (100, 150),
        'season': 'Zaid', 'icon': '🍐', 'price': 5290
    },
    'orange': {
        'N': (60, 100), 'P': (40, 60), 'K': (40, 60),
        'temp': (15, 30), 'humidity': (65, 80), 'ph': (5.5, 7.0), 'rain': (80, 120),
        'season': 'Rabi', 'icon': '🍊', 'price': 8000
    },
    'lemon': {
        'N': (60, 80), 'P': (40, 50), 'K': (40, 60),
        'temp': (20, 38), 'humidity': (65, 80), 'ph': (5.5, 7.0), 'rain': (80, 120),
        'season': 'Zaid', 'icon': '🍋', 'price': 12845
    },
    'strawberry': {
        'N': (60, 80), 'P': (40, 60), 'K': (40, 60),
        'temp': (15, 26), 'humidity': (70, 85), 'ph': (5.0, 6.5), 'rain': (50, 100),
        'season': 'Rabi', 'icon': '🍓', 'price': 19000
    },
    'litchi': {
        'N': (60, 80), 'P': (40, 60), 'K': (40, 60),
        'temp': (25, 35), 'humidity': (70, 85), 'ph': (5.5, 7.0), 'rain': (100, 150),
        'season': 'Zaid', 'icon': '🍒', 'price': 17500
    },
    'pomegranate': {
        'N': (80, 120), 'P': (40, 60), 'K': (60, 80),
        'temp': (15, 38), 'humidity': (55, 70), 'ph': (5.5, 7.5), 'rain': (50, 80),
        'season': 'Zaid', 'icon': '❤️', 'price': 12000
    },
    'jackfruit': {
        'N': (80, 100), 'P': (40, 50), 'K': (60, 80),
        'temp': (25, 35), 'humidity': (75, 85), 'ph': (6.0, 7.5), 'rain': (150, 250),
        'season': 'Zaid', 'icon': '🍈', 'price': 3052
    },
    'pear': {
        'N': (60, 80), 'P': (40, 60), 'K': (40, 60),
        'temp': (18, 23), 'humidity': (65, 75), 'ph': (6.0, 7.0), 'rain': (50, 100),
        'season': 'Rabi', 'icon': '🍐', 'price': 10603
    },
    'apricot': {
        'N': (60, 80), 'P': (40, 60), 'K': (40, 60),
        'temp': (20, 25), 'humidity': (60, 75), 'ph': (6.0, 7.0), 'rain': (50, 100),
        'season': 'Rabi', 'icon': '🍑', 'price': 10000
    },
    'avocado': {
        'N': (80, 100), 'P': (40, 50), 'K': (60, 80),
        'temp': (15, 29), 'humidity': (65, 80), 'ph': (5.5, 7.0), 'rain': (100, 150),
        'season': 'Zaid', 'icon': '🥑', 'price': 17500
    },
    'fig': {
        'N': (60, 80), 'P': (40, 60), 'K': (60, 80),
        'temp': (18, 27), 'humidity': (65, 80), 'ph': (6.0, 7.5), 'rain': (50, 100),
        'season': 'Zaid', 'icon': '🪴', 'price': 14000
    },
    'tamarind': {
        'N': (60, 80), 'P': (40, 60), 'K': (40, 60),
        'temp': (20, 35), 'humidity': (65, 80), 'ph': (6.0, 7.5), 'rain': (80, 120),
        'season': 'Zaid', 'icon': '🟤', 'price': 7690
    },
    
    # ========== CASH CROPS ==========
    'cotton': {
        'N': (80, 120), 'P': (40, 60), 'K': (40, 60),
        'temp': (20, 40), 'humidity': (60, 75), 'ph': (6.0, 7.5), 'rain': (50, 100),
        'season': 'Kharif', 'icon': '🌸', 'price': 7767
    },
    'sugarcane': {
        'N': (150, 250), 'P': (60, 100), 'K': (80, 150),
        'temp': (20, 35), 'humidity': (70, 85), 'ph': (6.0, 7.5), 'rain': (150, 250),
        'season': 'Zaid', 'icon': '🎋', 'price': 3500
    },
    'jute': {
        'N': (60, 80), 'P': (30, 40), 'K': (30, 40),
        'temp': (24, 37), 'humidity': (70, 85), 'ph': (6.0, 7.5), 'rain': (100, 200),
        'season': 'Kharif', 'icon': '🌿', 'price': 11300
    },
    'rubber': {
        'N': (80, 100), 'P': (40, 60), 'K': (60, 80),
        'temp': (25, 34), 'humidity': (75, 85), 'ph': (5.5, 7.0), 'rain': (200, 300),
        'season': 'Zaid', 'icon': '🌳', 'price': 20700
    },
    
    # ========== PLANTATION CROPS ==========
    'tea': {
        'N': (60, 80), 'P': (30, 40), 'K': (30, 40),
        'temp': (18, 30), 'humidity': (75, 85), 'ph': (4.5, 5.5), 'rain': (150, 300),
        'season': 'Zaid', 'icon': '🍵', 'price': 27000
    },
    'coffee': {
        'N': (80, 100), 'P': (40, 50), 'K': (40, 50),
        'temp': (15, 28), 'humidity': (70, 85), 'ph': (5.0, 6.5), 'rain': (150, 250),
        'season': 'Zaid', 'icon': '☕', 'price': 20200
    },
    'coconut': {
        'N': (150, 200), 'P': (80, 100), 'K': (150, 200),
        'temp': (20, 32), 'humidity': (75, 85), 'ph': (5.5, 7.5), 'rain': (130, 230),
        'season': 'Zaid', 'icon': '🥥', 'price': 6135
    },
    'cocoa': {
        'N': (80, 100), 'P': (40, 60), 'K': (60, 80),
        'temp': (19, 39), 'humidity': (75, 85), 'ph': (5.5, 7.0), 'rain': (150, 250),
        'season': 'Zaid', 'icon': '🟤', 'price': 12000
    },
    
    # ========== OILSEEDS ==========
    'groundnut': {
        'N': (20, 40), 'P': (40, 60), 'K': (30, 40),
        'temp': (25, 35), 'humidity': (60, 75), 'ph': (6.0, 7.0), 'rain': (50, 100),
        'season': 'Kharif', 'icon': '🥜', 'price': 6619
    },
    'soybean': {
        'N': (20, 40), 'P': (40, 60), 'K': (20, 40),
        'temp': (20, 30), 'humidity': (65, 80), 'ph': (6.0, 7.5), 'rain': (50, 100),
        'season': 'Kharif', 'icon': '🫘', 'price': 5423
    },
    'sunflower': {
        'N': (60, 80), 'P': (40, 50), 'K': (40, 50),
        'temp': (24, 35), 'humidity': (60, 75), 'ph': (6.0, 7.5), 'rain': (50, 100),
        'season': 'Rabi', 'icon': '🌻', 'price': 7500
    },
    'mustard': {
        'N': (60, 80), 'P': (40, 60), 'K': (20, 40),
        'temp': (10, 25), 'humidity': (60, 75), 'ph': (6.0, 7.5), 'rain': (40, 100),
        'season': 'Rabi', 'icon': '🌼', 'price': 6076
    },
    'sesame': {
        'N': (40, 60), 'P': (40, 60), 'K': (40, 60),
        'temp': (25, 30), 'humidity': (60, 75), 'ph': (5.5, 7.5), 'rain': (50, 80),
        'season': 'Kharif', 'icon': '🌱', 'price': 9316
    },
    'castor': {
        'N': (40, 60), 'P': (30, 50), 'K': (30, 50),
        'temp': (25, 35), 'humidity': (55, 70), 'ph': (6.0, 7.5), 'rain': (40, 80),
        'season': 'Kharif', 'icon': '🌿', 'price': 5000
    },
    
    # ========== PULSES ==========
    'chickpea': {
        'N': (20, 30), 'P': (40, 50), 'K': (20, 30),
        'temp': (18, 30), 'humidity': (55, 70), 'ph': (6.0, 7.5), 'rain': (40, 80),
        'season': 'Rabi', 'icon': '🫘', 'price': 5200
    },
    'lentil': {
        'N': (20, 40), 'P': (30, 40), 'K': (20, 30),
        'temp': (15, 21), 'humidity': (60, 75), 'ph': (6.0, 7.5), 'rain': (35, 55),
        'season': 'Rabi', 'icon': '🫘', 'price': 6505
    },
    'blackgram': {
        'N': (25, 35), 'P': (20, 30), 'K': (20, 30),
        'temp': (25, 35), 'humidity': (60, 75), 'ph': (6.0, 7.5), 'rain': (60, 75),
        'season': 'Kharif', 'icon': '⚫', 'price': 7132
    },
    'greengram': {
        'N': (25, 30), 'P': (20, 30), 'K': (20, 30),
        'temp': (25, 35), 'humidity': (60, 75), 'ph': (6.0, 7.5), 'rain': (60, 75),
        'season': 'Kharif', 'icon': '🟢', 'price': 2828
    },
    'pigeonpea': {
        'N': (25, 35), 'P': (20, 30), 'K': (20, 30),
        'temp': (29, 36), 'humidity': (60, 75), 'ph': (6.0, 7.5), 'rain': (60, 100),
        'season': 'Kharif', 'icon': '🫘', 'price': 3198
    },
    'horsegram': {
        'N': (25, 30), 'P': (20, 30), 'K': (20, 30),
        'temp': (25, 30), 'humidity': (55, 70), 'ph': (6.0, 7.5), 'rain': (50, 80),
        'season': 'Kharif', 'icon': '🫘', 'price': 3702
    },
    'beans': {
        'N': (20, 30), 'P': (40, 60), 'K': (20, 30),
        'temp': (21, 29), 'humidity': (65, 80), 'ph': (6.0, 7.0), 'rain': (60, 100),
        'season': 'Kharif', 'icon': '🫘', 'price': 6951
    },
    
    # ========== SPICES ==========
    'turmeric': {
        'N': (80, 100), 'P': (40, 60), 'K': (60, 80),
        'temp': (20, 35), 'humidity': (70, 85), 'ph': (5.5, 7.0), 'rain': (150, 250),
        'season': 'Kharif', 'icon': '🟡', 'price': 10424
    },
    'coriander': {
        'N': (40, 60), 'P': (30, 40), 'K': (30, 40),
        'temp': (10, 25), 'humidity': (60, 75), 'ph': (6.0, 7.5), 'rain': (40, 80),
        'season': 'Rabi', 'icon': '🌿', 'price': 9569
    },
    'cumin': {
        'N': (40, 60), 'P': (30, 40), 'K': (30, 40),
        'temp': (15, 25), 'humidity': (55, 70), 'ph': (6.5, 8.0), 'rain': (40, 80),
        'season': 'Rabi', 'icon': '🌱', 'price': 7639
    },
    'cardamom': {
        'N': (60, 80), 'P': (40, 60), 'K': (40, 60),
        'temp': (20, 35), 'humidity': (75, 85), 'ph': (5.0, 6.5), 'rain': (150, 250),
        'season': 'Zaid', 'icon': '🟢', 'price': 217800
    },
    'fennel': {
        'N': (40, 60), 'P': (30, 40), 'K': (30, 40),
        'temp': (15, 25), 'humidity': (55, 70), 'ph': (6.0, 7.5), 'rain': (50, 80),
        'season': 'Rabi', 'icon': '🌿', 'price': 7810
    },
    'fenugreek': {
        'N': (40, 60), 'P': (30, 40), 'K': (30, 40),
        'temp': (10, 30), 'humidity': (55, 70), 'ph': (6.0, 7.5), 'rain': (40, 80),
        'season': 'Rabi', 'icon': '🌿', 'price': 5638
    },
    'mint': {
        'N': (60, 80), 'P': (40, 60), 'K': (40, 60),
        'temp': (18, 21), 'humidity': (65, 80), 'ph': (6.0, 7.5), 'rain': (60, 100),
        'season': 'Zaid', 'icon': '🌿', 'price': 2000
    },
    
    # ========== MEDICINAL ==========
    'aloe_vera': {
        'N': (30, 40), 'P': (20, 30), 'K': (30, 40),
        'temp': (13, 29), 'humidity': (55, 70), 'ph': (6.5, 8.0), 'rain': (30, 70),
        'season': 'Zaid', 'icon': '🌵', 'price': 1000
    },
    'saffron': {
        'N': (30, 40), 'P': (20, 30), 'K': (20, 30),
        'temp': (23, 27), 'humidity': (55, 70), 'ph': (6.0, 8.0), 'rain': (50, 100),
        'season': 'Rabi', 'icon': '🟣', 'price': 200000
    },
    
    # ========== OTHER CROPS ==========
    'sweetpotato': {
        'N': (80, 120), 'P': (40, 60), 'K': (60, 80),
        'temp': (21, 26), 'humidity': (65, 80), 'ph': (5.5, 7.0), 'rain': (75, 150),
        'season': 'Kharif', 'icon': '🍠', 'price': 3071
    },
    'yam': {
        'N': (80, 100), 'P': (40, 50), 'K': (60, 80),
        'temp': (20, 30), 'humidity': (70, 85), 'ph': (5.5, 7.0), 'rain': (100, 150),
        'season': 'Kharif', 'icon': '🌽', 'price': 3000
    },
    'broccoli': {
        'N': (100, 150), 'P': (50, 60), 'K': (60, 80),
        'temp': (15, 21), 'humidity': (70, 85), 'ph': (6.0, 7.0), 'rain': (50, 100),
        'season': 'Rabi', 'icon': '🥦', 'price': 750
    }
}

# ============================================
# IMPROVED GENERATOR: GAUSSIAN WITH AUTO-SEPARATION
# ============================================

print(f"\nTotal crops in database: {len(crops_data)}")
print("Generating dataset with Gaussian distributions...")

# Step 1: Compute centroids (midpoints) for each crop
features = ['N', 'P', 'K', 'temp', 'humidity', 'ph', 'rain']
crop_centroids = {}
crop_ranges = {}
for crop, params in crops_data.items():
    centroid = []
    ranges = []
    for feat in features:
        lo, hi = params[feat]
        centroid.append((lo + hi) / 2.0)
        ranges.append((lo, hi))
    crop_centroids[crop] = np.array(centroid)
    crop_ranges[crop] = ranges

# Step 2: Normalize and compute pairwise distances
all_crops = list(crops_data.keys())
n_crops = len(all_crops)

# Normalization bounds (global min/max across all crops)
global_mins = np.array([min(crop_centroids[c][i] for c in all_crops) for i in range(7)])
global_maxs = np.array([max(crop_centroids[c][i] for c in all_crops) for i in range(7)])
global_spans = global_maxs - global_mins
global_spans[global_spans == 0] = 1  # avoid division by zero

def normalized(centroid):
    return (centroid - global_mins) / global_spans

# Step 3: Detect and fix overcrowded centroids
MIN_NORM_DIST = 0.08  # minimum normalized Euclidean distance
np.random.seed(42)
# Continue nudging until all pairs are far enough
for iteration in range(200):
    nudged = False
    for i in range(n_crops):
        for j in range(i + 1, n_crops):
            ci = all_crops[i]
            cj = all_crops[j]
            vi = normalized(crop_centroids[ci])
            vj = normalized(crop_centroids[cj])
            dist = np.linalg.norm(vi - vj)
            if dist < MIN_NORM_DIST:
                # Nudge both apart slightly
                shift = (vj - vi) / (dist + 1e-10) * MIN_NORM_DIST * 0.5
                # De-normalize shift
                shift_denorm = shift * global_spans
                crop_centroids[ci] -= shift_denorm * 0.5
                crop_centroids[cj] += shift_denorm * 0.5
                nudged = True
    if not nudged:
        print(f"Converged after {iteration} nudging iterations")
        break

# Step 4: Verify final separation
min_dist_final = float('inf')
close_pairs = []
for i in range(n_crops):
    for j in range(i + 1, n_crops):
        d = np.linalg.norm(normalized(crop_centroids[all_crops[i]]) - normalized(crop_centroids[all_crops[j]]))
        if d < min_dist_final:
            min_dist_final = d
        if d < 0.12:
            close_pairs.append((all_crops[i], all_crops[j], round(d, 4)))
print(f"Min centroid distance: {min_dist_final:.4f}")
if close_pairs:
    print(f"Close pairs (d<0.12): {close_pairs[:5]}...")

# Step 5: Generate samples
SAMPLES_PER_CROP = 3000
np.random.seed(123)
samples = []

for crop in all_crops:
    centroid = crop_centroids[crop]
    ranges = crop_ranges[crop]
    for _ in range(SAMPLES_PER_CROP):
        row = []
        for f_idx, (lo, hi) in enumerate(ranges):
            span = hi - lo
            std = span / 10.0  # ~95% within range
            val = np.random.normal(centroid[f_idx], std)
            val = max(lo, min(hi, val))  # clip to range
            # Round appropriately
            if features[f_idx] == 'ph':
                val = round(val, 1)
            else:
                val = round(val)
            row.append(int(val) if features[f_idx] != 'ph' else val)
        row.append(crop)
        samples.append(row)

df = pd.DataFrame(samples, columns=['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'label'])
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

csv_path = 'dataset/crop_data.csv'
df.to_csv(csv_path, index=False)

print(f"\nDataset generated: {len(df):,} samples, {df['label'].nunique()} crops")
print(f"Samples per crop: {SAMPLES_PER_CROP}")
print(f"File: {csv_path}")
print(f"Size: {os.path.getsize(csv_path) / 1024:.1f} KB")
print("Ready to train. Run: python model.py")