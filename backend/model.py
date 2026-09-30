import warnings
warnings.filterwarnings('ignore')
import pandas as pd, numpy as np, joblib, os, json
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

base_dir = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(base_dir, 'dataset', 'crop_data.csv')

if not os.path.exists(dataset_path):
    raise FileNotFoundError(f"Dataset missing: {dataset_path}")

df = pd.read_csv(dataset_path)
print(f"Dataset: {len(df)} samples, {df['label'].nunique()} crops")

X = df[["N","P","K","temperature","humidity","ph","rainfall"]]
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Train: {len(X_train)}, Test: {len(X_test)}")

model = RandomForestClassifier(
    n_estimators=200, max_depth=18, min_samples_leaf=2,
    random_state=42, n_jobs=-1
)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
prec = precision_score(y_test, y_pred, average='weighted', zero_division=0)
rec = recall_score(y_test, y_pred, average='weighted', zero_division=0)
f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)

print(f"Accuracy:  {acc:.2%}")
print(f"Precision: {prec:.4f}")
print(f"Recall:    {rec:.4f}")
print(f"F1 Score:  {f1:.4f}")

model_path = os.path.join(base_dir, 'crop_model.pkl')
joblib.dump(model, model_path)
print(f"Model saved: {model_path}")

metrics = {
    "accuracy": round(acc * 100, 1),
    "precision": round(prec, 4),
    "recall": round(rec, 4),
    "f1_score": round(f1, 4),
    "training_samples": len(X_train),
    "testing_samples": len(X_test),
    "total_crops": len(model.classes_),
    "features_used": list(X.columns),
    "algorithm": "Random Forest Classifier"
}
# Remove stale .joblib so get_model() regenerates from fresh .pkl
stale_joblib = os.path.join(base_dir, 'crop_model.joblib')
if os.path.exists(stale_joblib):
    os.remove(stale_joblib)
    print(f"Removed stale: {stale_joblib}")

metrics_path = os.path.join(base_dir, "model_metrics.json")
with open(metrics_path, "w") as f:
    json.dump(metrics, f, indent=2)
print(f"Metrics saved: {metrics_path}")
print("Done!")
