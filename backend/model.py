import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

print("🚀 Starting model training...")

# Resolve dataset path relative to this file so it works regardless of current working directory
base_dir = os.path.abspath(os.path.dirname(__file__))
dataset_path = os.path.join(base_dir, 'dataset', 'crop_data.csv')
if not os.path.exists(dataset_path):
    raise FileNotFoundError(f"❌ Dataset missing: {dataset_path}")

try:
    df = pd.read_csv(dataset_path)
    print(f"✅ Dataset loaded: {len(df)} samples, {df['label'].nunique()} crops")
    print(f"📊 Crops: {sorted(df['label'].unique())}")
except Exception as e:
    raise Exception(f"❌ CSV error: {e}")

# Prepare features and target
feature_columns = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
X = df[feature_columns]
y = df['label']  # ← CHANGED FROM 'crop' TO 'label'

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"✅ Data split: {len(X_train)} training, {len(X_test)} testing")

# Train Random Forest model
print("🔄 Training Random Forest model...")
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42
)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"✅ Model accuracy: {accuracy:.2%}")

# Save model
model_path = 'crop_model.pkl'
joblib.dump(model, model_path)
print(f"✅ Model saved as '{model_path}'")

print("\n📊 Training complete! Model ready for use.")