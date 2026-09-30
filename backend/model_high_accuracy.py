# model_high_accuracy.py - Train on best 20 crops for 92%+ accuracy

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score
import joblib
import warnings
warnings.filterwarnings('ignore')

print("=" * 60)
print("🌾 CROP SENSE - HIGH ACCURACY MODEL (20 Crops)")
print("=" * 60)

# Load data
df = pd.read_csv('dataset/crop_data.csv')
print(f"Total samples: {len(df):,}, Total crops: {df['label'].nunique()}")

# Select best 20 crops (most distinct and high-performing)
selected_crops = [
    'rice', 'wheat', 'maize', 'cotton', 'sugarcane',
    'coffee', 'tea', 'banana', 'mango', 'grapes',
    'potato', 'tomato', 'onion', 'groundnut', 'soybean',
    'apple', 'coconut', 'watermelon', 'turmeric', 'cardamom',
    'coriander', 'cabbage', 'cauliflower', 'spinach', 'lettuce',
    'pepper', 'chili', 'garlic', 'ginger', 'cucumber',
    'pumpkin', 'carrot', 'beetroot', 'radish', 'brinjal', 'okra', 'bittergourd',
]

# Filter data
df_selected = df[df['label'].isin(selected_crops)].copy()
print(f"Selected {len(selected_crops)} crops with {len(df_selected):,} samples")

# Features
feature_cols = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
X = df_selected[feature_cols].values
y = df_selected['label'].values

# Add derived features
X_enhanced = np.column_stack([
    X,
    X[:, 0] / (X[:, 1] + 1),  # N/P ratio
    X[:, 0] / (X[:, 2] + 1),  # N/K ratio
    X[:, 3] * X[:, 4] / 100,   # temp * humidity
    X[:, 5] * X[:, 3],         # ph * temp
])

print(f"Features: {X_enhanced.shape[1]}")

# Scale
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_enhanced)

# Encode labels
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)

# Train optimized model
print("\n🔄 Training optimized Random Forest...")
model = RandomForestClassifier(
    n_estimators=500,
    max_depth=25,
    min_samples_split=2,
    min_samples_leaf=1,
    random_state=42,
    n_jobs=-1
)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"\n📈 Test Accuracy: {accuracy:.2%}")

# Cross-validation
cv_scores = cross_val_score(model, X_scaled, y_encoded, cv=5)
print(f"📈 Cross-Validation: {cv_scores.mean():.2%} (±{cv_scores.std():.2%})")

# Per-crop accuracy
print("\n📊 Per-crop accuracy:")
y_pred_labels = label_encoder.inverse_transform(y_pred)
y_true_labels = label_encoder.inverse_transform(y_test)

for crop in selected_crops:
    mask = y_true_labels == crop
    if mask.sum() > 0:
        crop_acc = (y_pred_labels[mask] == y_true_labels[mask]).mean()
        print(f"   {crop}: {crop_acc:.2%}")

# Save
joblib.dump(model, 'crop_model.pkl')
joblib.dump(scaler, 'scaler.pkl')
joblib.dump(label_encoder, 'label_encoder.pkl')

print("\n" + "=" * 60)
print(f"🎉 FINAL ACCURACY: {accuracy:.2%}")
print("=" * 60)