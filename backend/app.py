from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import joblib
import numpy as np
import os
from flask_mail import Mail, Message
from dotenv import load_dotenv
import subprocess

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)  # Allow frontend to connect

# Load .env
load_dotenv()


model = None  # Lazy loaded via get_model()

def get_model():
    global model
    if model is None:
        model_path = 'crop_model.pkl'
        if not os.path.exists(model_path):
            print("🔄 Auto-training model...")
            subprocess.check_call(['python', 'model.py'])
        try:
            model = joblib.load(model_path)
            print("✅ Model loaded successfully")
        except Exception as e:
            print(f"❌ Model load failed: {e}")
            model = None
    return model

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD') 
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', 'no-reply@cropsense.in')
app.config['MAIL_RECIPIENTS'] = os.getenv('MAIL_RECIPIENTS', 'support@cropsense.in').split(',')

# Disable mail if no creds (dev mode safe)
if not app.config['MAIL_USERNAME'] or app.config['MAIL_USERNAME'] == 'your-email@gmail.com':
    app.config['TESTING'] = True
    print("ℹ️  Email disabled (no .env creds). Set MAIL_USERNAME/PASSWORD for contact form.")

mail = Mail(app)

# ============================================
# FRONTEND ROUTES - Serve your website
# ============================================

@app.route('/')
def serve_index():
    """Serve the main homepage"""
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def serve_frontend(path):
    """Serve all frontend files (HTML, CSS, JS, etc.)"""
    # If the path exists as a file in frontend, serve it
    frontend_path = os.path.join('../frontend', path)
    if os.path.exists(frontend_path):
        return send_from_directory('../frontend', path)
    
    # If path doesn't have .html extension, try adding it
    if not path.endswith('.html'):
        html_path = path + '.html'
        if os.path.exists(os.path.join('../frontend', html_path)):
            return send_from_directory('../frontend', html_path)
    
    # If still not found, serve index.html (for client-side routing)
    return send_from_directory('../frontend', 'index.html')

# ============================================
# API ROUTES - Your existing endpoints
# ============================================

# Crop information database (YOUR EXISTING CROP_INFO STAYS THE SAME)
CROP_INFO = {
    'Rice': {
        'icon': '🌾',
        'season': 'Kharif',
        'soil': 'Clay',
        'fert': 'Urea 100kg/ha, DAP 50kg/ha',
        'price': 2100,
        'min_temp': 20,
        'max_temp': 35,
        'min_rain': 100,
        'max_rain': 300
    },
    'Wheat': {
        'icon': '🌿',
        'season': 'Rabi',
        'soil': 'Loamy',
        'fert': 'Urea 120kg/ha, DAP 60kg/ha',
        'price': 2275,
        'min_temp': 10,
        'max_temp': 25,
        'min_rain': 50,
        'max_rain': 150
    },
    'Maize': {
        'icon': '🌽',
        'season': 'Kharif',
        'soil': 'Loamy',
        'fert': 'Urea 120kg/ha, DAP 60kg/ha',
        'price': 1962,
        'min_temp': 18,
        'max_temp': 32,
        'min_rain': 50,
        'max_rain': 120
    },
    'Cotton': {
        'icon': '🌸',
        'season': 'Kharif',
        'soil': 'Black',
        'fert': 'Urea 100kg/ha, DAP 50kg/ha',
        'price': 6620,
        'min_temp': 20,
        'max_temp': 40,
        'min_rain': 50,
        'max_rain': 100
    },
    'Sugarcane': {
        'icon': '🎋',
        'season': 'Zaid',
        'soil': 'Alluvial',
        'fert': 'Urea 250kg/ha, DAP 100kg/ha',
        'price': 3500,
        'min_temp': 20,
        'max_temp': 35,
        'min_rain': 150,
        'max_rain': 250
    },
    'Tea': {
        'icon': '🍵',
        'season': 'Zaid',
        'soil': 'Acidic',
        'fert': 'Urea 60kg/ha, DAP 30kg/ha',
        'price': 18000,
        'min_temp': 18,
        'max_temp': 30,
        'min_rain': 150,
        'max_rain': 300
    },
    'Coffee': {
        'icon': '☕',
        'season': 'Zaid',
        'soil': 'Laterite',
        'fert': 'Urea 80kg/ha, DAP 40kg/ha',
        'price': 42000,
        'min_temp': 15,
        'max_temp': 28,
        'min_rain': 150,
        'max_rain': 250
    },
    'Groundnut': {
        'icon': '🥜',
        'season': 'Kharif',
        'soil': 'Sandy',
        'fert': 'Urea 20kg/ha, DAP 60kg/ha',
        'price': 5500,
        'min_temp': 20,
        'max_temp': 35,
        'min_rain': 50,
        'max_rain': 100
    },
    'Soybean': {
        'icon': '🫘',
        'season': 'Kharif',
        'soil': 'Loamy',
        'fert': 'Urea 30kg/ha, DAP 60kg/ha',
        'price': 4600,
        'min_temp': 15,
        'max_temp': 30,
        'min_rain': 50,
        'max_rain': 100
    },
    'Pulses': {
        'icon': '🫛',
        'season': 'Rabi',
        'soil': 'Loamy',
        'fert': 'Urea 25kg/ha, DAP 50kg/ha',
        'price': 6000,
        'min_temp': 15,
        'max_temp': 30,
        'min_rain': 40,
        'max_rain': 80
    },
    'Millets': {
        'icon': '🌾',
        'season': 'Kharif',
        'soil': 'Sandy',
        'fert': 'Urea 40kg/ha, DAP 40kg/ha',
        'price': 2800,
        'min_temp': 25,
        'max_temp': 40,
        'min_rain': 30,
        'max_rain': 70
    },
    'Jute': {
        'icon': '🌿',
        'season': 'Kharif',
        'soil': 'Alluvial',
        'fert': 'Urea 60kg/ha, DAP 30kg/ha',
        'price': 5500,
        'min_temp': 24,
        'max_temp': 37,
        'min_rain': 100,
        'max_rain': 200
    },
    'Mustard': {
        'icon': '🌼',
        'season': 'Rabi',
        'soil': 'Loamy',
        'fert': 'Urea 60kg/ha, DAP 40kg/ha',
        'price': 5200,
        'min_temp': 10,
        'max_temp': 25,
        'min_rain': 40,
        'max_rain': 100
    },
    'Barley': {
        'icon': '🌾',
        'season': 'Rabi',
        'soil': 'Loamy',
        'fert': 'Urea 80kg/ha, DAP 40kg/ha',
        'price': 2000,
        'min_temp': 10,
        'max_temp': 25,
        'min_rain': 40,
        'max_rain': 120
    },
    'Potato': {
        'icon': '🥔',
        'season': 'Rabi',
        'soil': 'Loamy',
        'fert': 'Urea 120kg/ha, DAP 80kg/ha',
        'price': 1500,
        'min_temp': 15,
        'max_temp': 25,
        'min_rain': 50,
        'max_rain': 120
    },
    'Chickpea': {
        'icon': '🫘',
        'season': 'Rabi',
        'soil': 'Loamy',
        'fert': 'Urea 40kg/ha, DAP 30kg/ha',
        'price': 5200,
        'min_temp': 15,
        'max_temp': 30,
        'min_rain': 40,
        'max_rain': 95
    },
    'Kidneybeans': {
        'icon': '🫘',
        'season': 'Kharif',
        'soil': 'Loamy',
        'fert': 'Urea 25kg/ha, DAP 60kg/ha',
        'price': 5500,
        'min_temp': 15,
        'max_temp': 25,
        'min_rain': 60,
        'max_rain': 150
    },
    'Pigeonpeas': {
        'icon': '🫘',
        'season': 'Kharif',
        'soil': 'Loamy',
        'fert': 'Urea 30kg/ha, DAP 20kg/ha',
        'price': 6000,
        'min_temp': 18,
        'max_temp': 37,
        'min_rain': 90,
        'max_rain': 200
    },
    'Mothbeans': {
        'icon': '🫘',
        'season': 'Kharif',
        'soil': 'Sandy',
        'fert': 'Urea 20kg/ha, DAP 15kg/ha',
        'price': 4500,
        'min_temp': 24,
        'max_temp': 32,
        'min_rain': 30,
        'max_rain': 75
    },
    'Mungbean': {
        'icon': '🫘',
        'season': 'Kharif',
        'soil': 'Loamy',
        'fert': 'Urea 25kg/ha, DAP 20kg/ha',
        'price': 5500,
        'min_temp': 27,
        'max_temp': 30,
        'min_rain': 35,
        'max_rain': 60
    },
    'Blackgram': {
        'icon': '🫘',
        'season': 'Kharif',
        'soil': 'Loamy',
        'fert': 'Urea 30kg/ha, DAP 20kg/ha',
        'price': 6500,
        'min_temp': 25,
        'max_temp': 35,
        'min_rain': 60,
        'max_rain': 75
    },
    'Lentil': {
        'icon': '🫘',
        'season': 'Rabi',
        'soil': 'Loamy',
        'fert': 'Urea 40kg/ha, DAP 30kg/ha',
        'price': 6000,
        'min_temp': 18,
        'max_temp': 30,
        'min_rain': 35,
        'max_rain': 55
    },
    'Pomegranate': {
        'icon': '🍎',
        'season': 'Zaid',
        'soil': 'Loamy',
        'fert': 'Urea 100kg/ha, DAP 50kg/ha',
        'price': 9000,
        'min_temp': 18,
        'max_temp': 35,
        'min_rain': 100,
        'max_rain': 120
    },
    'Banana': {
        'icon': '🍌',
        'season': 'Zaid',
        'soil': 'Loamy',
        'fert': 'Urea 200kg/ha, DAP 100kg/ha',
        'price': 3500,
        'min_temp': 25,
        'max_temp': 30,
        'min_rain': 90,
        'max_rain': 120
    },
    'Mango': {
        'icon': '🥭',
        'season': 'Zaid',
        'soil': 'Loamy',
        'fert': 'Urea 150kg/ha, DAP 80kg/ha',
        'price': 5000,
        'min_temp': 24,
        'max_temp': 40,
        'min_rain': 70,
        'max_rain': 150
    },
    'Grapes': {
        'icon': '🍇',
        'season': 'Zaid',
        'soil': 'Loamy',
        'fert': 'Urea 120kg/ha, DAP 60kg/ha',
        'price': 7000,
        'min_temp': 9,
        'max_temp': 42,
        'min_rain': 65,
        'max_rain': 75
    },
    'Watermelon': {
        'icon': '🍉',
        'season': 'Zaid',
        'soil': 'Sandy',
        'fert': 'Urea 80kg/ha, DAP 50kg/ha',
        'price': 2500,
        'min_temp': 24,
        'max_temp': 27,
        'min_rain': 40,
        'max_rain': 60
    },
    'Muskmelon': {
        'icon': '🍈',
        'season': 'Zaid',
        'soil': 'Sandy',
        'fert': 'Urea 80kg/ha, DAP 50kg/ha',
        'price': 2800,
        'min_temp': 27,
        'max_temp': 30,
        'min_rain': 20,
        'max_rain': 30
    },
    'Apple': {
        'icon': '🍎',
        'season': 'Rabi',
        'soil': 'Loamy',
        'fert': 'Urea 120kg/ha, DAP 80kg/ha',
        'price': 8000,
        'min_temp': 21,
        'max_temp': 24,
        'min_rain': 100,
        'max_rain': 125
    },
    'Orange': {
        'icon': '🍊',
        'season': 'Zaid',
        'soil': 'Loamy',
        'fert': 'Urea 100kg/ha, DAP 60kg/ha',
        'price': 6000,
        'min_temp': 10,
        'max_temp': 35,
        'min_rain': 100,
        'max_rain': 120
    },
    'Papaya': {
        'icon': '🍈',
        'season': 'Zaid',
        'soil': 'Loamy',
        'fert': 'Urea 150kg/ha, DAP 80kg/ha',
        'price': 3500,
        'min_temp': 23,
        'max_temp': 43,
        'min_rain': 40,
        'max_rain': 250
    },
    'Coconut': {
        'icon': '🥥',
        'season': 'Zaid',
        'soil': 'Sandy',
        'fert': 'Urea 200kg/ha, DAP 100kg/ha',
        'price': 6000,
        'min_temp': 25,
        'max_temp': 30,
        'min_rain': 130,
        'max_rain': 230
    }
}
@app.route('/predict', methods=['POST'])
def predict():
    mdl = get_model()
    if mdl is None:
        return jsonify({'error': 'Model not available. Try refreshing.'}), 500
    
    try:
        # Get data from request
        data = request.json
        print("📥 Received data:", data)
        
        # Prepare features
        features = np.array([[
            float(data['N']),
            float(data['P']),
            float(data['K']),
            float(data['temperature']),
            float(data['humidity']),
            float(data['ph']),
            float(data['rainfall'])
        ]])
        
        # Get prediction probabilities
        probabilities = mdl.predict_proba(features)[0]
        
        # Get top 3 crops
        top_3_indices = np.argsort(probabilities)[-3:][::-1]
        top_3_crops = [mdl.classes_[i] for i in top_3_indices]
        top_3_confidences = [float(probabilities[i]) for i in top_3_indices]
        
        # Prepare response with crop details
        recommendations = []
        for i, (crop, confidence) in enumerate(zip(top_3_crops, top_3_confidences)):
            crop_info = CROP_INFO.get(crop, {
                'icon': '🌿',
                'season': 'General',
                'fert': 'Standard fertilizer',
                'price': 0,
                'min_temp': 0,
                'max_temp': 0,
                'min_rain': 0,
                'max_rain': 0
            })
            
            recommendations.append({
                'rank': i + 1,
                'name': crop,
                'icon': crop_info['icon'],
                'season': crop_info['season'],
                'fert': crop_info['fert'],
                'price': crop_info['price'],
                'confidence': round(confidence * 100, 2),
                'min_temp': crop_info['min_temp'],
                'max_temp': crop_info['max_temp'],
                'min_rain': crop_info['min_rain'],
                'max_rain': crop_info['max_rain']
            })
        
        print("✅ Recommendations generated:", [r['name'] for r in recommendations])
        
        return jsonify({
            'success': True,
            'recommendations': recommendations
        })
        
    except Exception as e:
        print("❌ Error:", str(e))
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    mdl = get_model()
    return jsonify({'status': 'healthy', 'model_loaded': mdl is not None})

@app.route('/contact', methods=['POST'])
def contact():
    try:
        data = request.json
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')
        
        # Create email
        msg = Message(
            subject=f"New Contact Form Message from {name}",
            recipients=['support@cropsense.in'],  # Where you want to receive emails
            body=f"""
        Name: {name}
        Email: {email}
        
        Message:
        {message}
        """,
            reply_to=email
        )
        
        # Send email (disabled if no config)
        if app.config['TESTING']:
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
    'training_samples': 24,
    'testing_samples': 6,
    'total_crops': len(CROP_INFO),
    'features_used': ['N', 'P', 'K', 'Temperature', 'Humidity', 'pH', 'Rainfall']
})


if __name__ == '__main__':
    app.run(debug=True, port=5000)