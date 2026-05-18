# 🌾 CropSense - Smart Crop Recommendation System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3-green.svg)](https://flask.palletsprojects.com/)
[![Scikit-learn](https://img.shields.io/badge/scikit--learn-1.3-yellow.svg)](https://scikit-learn.org/)

AI-powered web app for Indian farmers. Enter NPK soil values, climate data → get top crop recommendations with fertilizer plans, market prices, seasons.

## ✨ Features
- **ML Predictions**: RandomForest trained on real crop dataset (22+ samples)
- **50+ Crops**: Comprehensive database (Rice → exotic fruits/spices)
- **Real-time**: NPK analysis, climate matching, ₹/quintal prices
- **Chatbot**: Ask about soil/crops/seasons (voice-enabled)
- **History**: Track recommendations per user
- **Contact Form**: Farmer support (Gmail-powered)

## 🚀 Quick Start (One Command)

```bash
# From project root
cd backend
python run.py
```

**Opens**: http://localhost:5000

**What happens**:
1. Creates `venv/`
2. `pip install -r requirements.txt`
3. Trains `crop_model.pkl` (if missing)
4. Starts Flask dev server

## 📋 Manual Setup

1. **Python 3.8+** (Windows/macOS/Linux)
2. ```bash
   cd backend
   python -m venv venv
   # Windows:
   venv\\Scripts\\activate
   # macOS/Linux: 
   source venv/bin/activate
   pip install -r requirements.txt
   python model.py  # Train ML model
   python app.py
   ```

3. **Visit**: http://localhost:5000

## 🔧 Configuration

Copy `.env.example` → `.env`:
```
MAIL_USERNAME=your-gmail@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_RECIPIENTS=support@cropsense.in
```
- [Gmail App Password](https://support.google.com/mail/answer/185833)

## 🏗️ Project Structure
```
CropSense/
├── backend/           # Flask API + ML
│   ├── app.py         # Main server
│   ├── model.py       # Train RandomForest
│   ├── run.py         # 🚀 One-command runner
│   ├── crop_model.pkl # Trained model
│   └── dataset/       # crop_data.csv
├── frontend/          # HTML/JS/CSS SPA
└── TODO.md            # Fix progress
```

## 🧪 Testing APIs
```bash
curl http://localhost:5000/health
curl -X POST http://localhost:5000/predict \\
  -H "Content-Type: application/json" \\
  -d '{"N":90,"P":42,"K":43,"temperature":20.87,"humidity":82,"ph":6.5,"rainfall":202.93}'
```

## 📈 ML Model
- **Dataset**: `backend/dataset/crop_data.csv` (NPK + climate → crop)
- **Algorithm**: RandomForestClassifier (n_estimators=100)
- **Accuracy**: ~95% on test set
- **Classes**: 15+ Indian crops (Rice, Wheat, Maize...)

## 🤖 Frontend
- **data.js**: ML fetch, chatbot (voice), crop DB
- **No build step**: Pure HTML/JS/CSS → instant

## 🔒 Users
- LocalStorage (username/password)
- History persists across sessions

## 🛠️ Development
```bash
# Edit + hot reload (debug=True)
python backend/app.py

# Run tests
python backend/test_api.py
```

## 📱 Responsive
- Desktop/Tablet/Mobile
- Print-friendly results
- CSV export

## Future Ideas ✨
- [ ] Real weather API
- [ ] Image soil analysis
- [ ] MSP prices (live)
- [ ] Multi-language
- [ ] Mobile PWA

**Made with ❤️ for Indian farmers. Kisan ki majboori nahi, unki majburi ko samajhna zaroori hai.**

---
*License: MIT | Questions? Edit TODO.md*

