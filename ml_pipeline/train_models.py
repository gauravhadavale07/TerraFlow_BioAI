"""
TerraFlow BioAI - Model Training Pipeline
Trains all 4 ML models for the smart irrigation & agro-advisory system.

Models:
  1. Crop Recommendation      → Random Forest Classifier
  2. Fertilizer Recommendation → XGBoost Classifier
  3. Soil Type Classification  → Random Forest Classifier
  4. Irrigation Prediction     → XGBoost Classifier (primary model for TerraFlow)

Each model is trained with features that EXACTLY match what the sensors produce,
so that at deployment time, raw sensor readings → model prediction with no mismatch.
"""

import os
import sys
import json
import warnings
import numpy as np
import pandas as pd
import joblib
from pathlib import Path
from datetime import datetime

from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import (
    accuracy_score, classification_report, confusion_matrix,
    f1_score, precision_score, recall_score
)

warnings.filterwarnings('ignore')

# Try importing xgboost; fall back to sklearn GradientBoosting if not available
try:
    from xgboost import XGBClassifier
    HAS_XGBOOST = True
except ImportError:
    HAS_XGBOOST = False
    print("[WARN] XGBoost not available, using sklearn GradientBoostingClassifier")

BASE_DIR = Path(__file__).parent.parent
DATASET_DIR = BASE_DIR / "datasets"
MODEL_DIR = BASE_DIR / "models"
MODEL_DIR.mkdir(exist_ok=True)


def save_model_artifacts(model, scaler, label_encoders, metadata, model_name):
    """Save model, scaler, encoders, and metadata to the models directory."""
    model_subdir = MODEL_DIR / model_name
    model_subdir.mkdir(exist_ok=True)

    # Save model
    joblib.dump(model, model_subdir / "model.joblib")

    # Save scaler
    if scaler is not None:
        joblib.dump(scaler, model_subdir / "scaler.joblib")

    # Save label encoders
    if label_encoders:
        joblib.dump(label_encoders, model_subdir / "label_encoders.joblib")

    # Save metadata (feature names, class names, metrics, etc.)
    with open(model_subdir / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2, default=str)

    print(f"  ✓ Model artifacts saved to: {model_subdir}")


def train_crop_recommendation():
    """
    Model 1: Crop Recommendation
    Algorithm: Random Forest (as specified in TerraFlow report Section 10)
    Features: N, P, K, temperature, humidity, pH, rainfall
    Target: crop label (22 classes)

    At inference: BME280 gives temperature + humidity,
                  soil test gives N/P/K/pH, weather API gives rainfall
    """
    print("=" * 60)
    print("MODEL 1: CROP RECOMMENDATION")
    print("=" * 60)

    df = pd.read_csv(DATASET_DIR / "crop_recommendation_clean.csv")

    feature_cols = ['nitrogen', 'phosphorus', 'potassium',
                    'temperature', 'humidity', 'ph', 'rainfall']
    X = df[feature_cols].values
    y = df['label'].values

    # Encode target labels
    le_target = LabelEncoder()
    y_encoded = le_target.fit_transform(y)

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Train/test split (stratified)
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )

    # Random Forest — aligned with TerraFlow report
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=20,
        min_samples_split=5,
        min_samples_leaf=2,
        max_features='sqrt',
        random_state=42,
        n_jobs=-1,
        class_weight='balanced'
    )
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='weighted')

    # Cross-validation
    cv_scores = cross_val_score(model, X_scaled, y_encoded, cv=5, scoring='accuracy')

    print(f"\n  Accuracy:     {accuracy:.4f}")
    print(f"  F1 (weighted): {f1:.4f}")
    print(f"  CV Accuracy:   {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

    # Feature importance
    importances = dict(zip(feature_cols, model.feature_importances_))
    print(f"  Feature importances: {json.dumps({k: round(float(v), 3) for k, v in sorted(importances.items(), key=lambda x: -x[1])}, indent=4)}")

    # Classification report
    report = classification_report(y_test, y_pred,
                                   target_names=le_target.classes_,
                                   output_dict=True)

    # Save
    metadata = {
        "model_name": "crop_recommendation",
        "algorithm": "RandomForestClassifier",
        "features": feature_cols,
        "feature_count": len(feature_cols),
        "target": "crop_label",
        "classes": list(le_target.classes_),
        "num_classes": len(le_target.classes_),
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "accuracy": round(accuracy, 4),
        "f1_weighted": round(f1, 4),
        "cv_accuracy_mean": round(cv_scores.mean(), 4),
        "cv_accuracy_std": round(cv_scores.std(), 4),
        "feature_importances": {k: round(v, 4) for k, v in importances.items()},
        "sensor_mapping": {
            "temperature": "BME280 ambient temperature (°C)",
            "humidity": "BME280 relative humidity (%RH)",
            "nitrogen": "Soil test N (kg/ha)",
            "phosphorus": "Soil test P (kg/ha)",
            "potassium": "Soil test K (kg/ha)",
            "ph": "Soil test / pH sensor",
            "rainfall": "Weather API (mm)",
        },
        "trained_at": datetime.now().isoformat(),
        "dataset_source": "Kaggle: atharvaingle/crop-recommendation-dataset",
    }

    save_model_artifacts(
        model=model,
        scaler=scaler,
        label_encoders={"target": le_target},
        metadata=metadata,
        model_name="crop_recommendation"
    )

    return model, accuracy


def train_fertilizer_recommendation():
    """
    Model 2: Fertilizer Recommendation
    Algorithm: XGBoost (or GradientBoosting fallback)
    Features: temperature, humidity, moisture, soil_type, crop_type, N, P, K
    Target: fertilizer name (7 classes)

    At inference: BME280 gives temp + humidity,
                  soil moisture sensor gives moisture,
                  user selects soil type + crop,
                  soil test gives N/P/K
    """
    print("\n" + "=" * 60)
    print("MODEL 2: FERTILIZER RECOMMENDATION")
    print("=" * 60)

    df = pd.read_csv(DATASET_DIR / "fertilizer_recommendation_clean.csv")

    # Encode categorical features
    le_soil = LabelEncoder()
    le_crop = LabelEncoder()
    le_target = LabelEncoder()

    df['soil_type_encoded'] = le_soil.fit_transform(df['soil_type'])
    df['crop_type_encoded'] = le_crop.fit_transform(df['crop_type'])
    y_encoded = le_target.fit_transform(df['fertilizer_name'])

    feature_cols = ['temperature', 'humidity', 'soil_moisture',
                    'soil_type_encoded', 'crop_type_encoded',
                    'nitrogen', 'phosphorus', 'potassium']

    X = df[feature_cols].values

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )

    # XGBoost or GradientBoosting
    if HAS_XGBOOST:
        model = XGBClassifier(
            n_estimators=300,
            max_depth=8,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            eval_metric='mlogloss',
            verbosity=0,
        )
    else:
        model = GradientBoostingClassifier(
            n_estimators=300,
            max_depth=8,
            learning_rate=0.1,
            subsample=0.8,
            random_state=42,
        )

    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='weighted')
    cv_scores = cross_val_score(model, X_scaled, y_encoded, cv=5, scoring='accuracy')

    print(f"\n  Accuracy:     {accuracy:.4f}")
    print(f"  F1 (weighted): {f1:.4f}")
    print(f"  CV Accuracy:   {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

    # Feature importance
    if HAS_XGBOOST:
        importances = dict(zip(feature_cols, model.feature_importances_))
    else:
        importances = dict(zip(feature_cols, model.feature_importances_))
    print(f"  Feature importances: {json.dumps({k: round(float(v), 3) for k, v in sorted(importances.items(), key=lambda x: -x[1])}, indent=4)}")

    metadata = {
        "model_name": "fertilizer_recommendation",
        "algorithm": "XGBClassifier" if HAS_XGBOOST else "GradientBoostingClassifier",
        "features": feature_cols,
        "features_raw": ['temperature', 'humidity', 'soil_moisture',
                         'soil_type', 'crop_type',
                         'nitrogen', 'phosphorus', 'potassium'],
        "target": "fertilizer_name",
        "classes": list(le_target.classes_),
        "num_classes": len(le_target.classes_),
        "soil_type_mapping": dict(zip(le_soil.classes_.tolist(),
                                       range(len(le_soil.classes_)))),
        "crop_type_mapping": dict(zip(le_crop.classes_.tolist(),
                                       range(len(le_crop.classes_)))),
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "accuracy": round(accuracy, 4),
        "f1_weighted": round(f1, 4),
        "cv_accuracy_mean": round(cv_scores.mean(), 4),
        "cv_accuracy_std": round(cv_scores.std(), 4),
        "feature_importances": {k: round(float(v), 4) for k, v in importances.items()},
        "sensor_mapping": {
            "temperature": "BME280 ambient temperature (°C)",
            "humidity": "BME280 relative humidity (%RH)",
            "soil_moisture": "FC-28/YL-69 soil moisture sensor (%)",
            "soil_type": "User configuration / soil classifier output",
            "crop_type": "User selection",
            "nitrogen": "Soil test N (kg/ha)",
            "phosphorus": "Soil test P (kg/ha)",
            "potassium": "Soil test K (kg/ha)",
        },
        "trained_at": datetime.now().isoformat(),
        "dataset_source": "Kaggle: gdabhishek/fertilizer-prediction (augmented 20x)",
    }

    save_model_artifacts(
        model=model,
        scaler=scaler,
        label_encoders={"target": le_target, "soil_type": le_soil, "crop_type": le_crop},
        metadata=metadata,
        model_name="fertilizer_recommendation"
    )

    return model, accuracy


def train_soil_type_classification():
    """
    Model 3: Soil Type Classification
    Algorithm: Random Forest
    Features: temperature, humidity, soil_moisture, N, P, K, pH
    Target: soil_type (6 classes: Black, Red, Alluvial, Sandy, Clayey, Loamy)

    At inference: BME280 gives temp + humidity,
                  soil moisture sensor gives moisture,
                  soil test gives N/P/K/pH
    """
    print("\n" + "=" * 60)
    print("MODEL 3: SOIL TYPE CLASSIFICATION")
    print("=" * 60)

    df = pd.read_csv(DATASET_DIR / "soil_type_classification.csv")

    feature_cols = ['temperature', 'humidity', 'soil_moisture',
                    'nitrogen', 'phosphorus', 'potassium', 'ph']
    X = df[feature_cols].values
    y = df['soil_type'].values

    le_target = LabelEncoder()
    y_encoded = le_target.fit_transform(y)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=15,
        min_samples_split=5,
        min_samples_leaf=2,
        max_features='sqrt',
        random_state=42,
        n_jobs=-1,
        class_weight='balanced'
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='weighted')
    cv_scores = cross_val_score(model, X_scaled, y_encoded, cv=5, scoring='accuracy')

    print(f"\n  Accuracy:     {accuracy:.4f}")
    print(f"  F1 (weighted): {f1:.4f}")
    print(f"  CV Accuracy:   {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

    importances = dict(zip(feature_cols, model.feature_importances_))
    print(f"  Feature importances: {json.dumps({k: round(float(v), 3) for k, v in sorted(importances.items(), key=lambda x: -x[1])}, indent=4)}")

    report = classification_report(y_test, y_pred,
                                   target_names=le_target.classes_,
                                   output_dict=True)
    print(f"\n  Per-class accuracy:")
    for cls in le_target.classes_:
        prec = report[cls]['precision']
        rec = report[cls]['recall']
        print(f"    {cls:12s}: precision={prec:.3f}  recall={rec:.3f}")

    metadata = {
        "model_name": "soil_type_classification",
        "algorithm": "RandomForestClassifier",
        "features": feature_cols,
        "target": "soil_type",
        "classes": list(le_target.classes_),
        "num_classes": len(le_target.classes_),
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "accuracy": round(accuracy, 4),
        "f1_weighted": round(f1, 4),
        "cv_accuracy_mean": round(cv_scores.mean(), 4),
        "cv_accuracy_std": round(cv_scores.std(), 4),
        "feature_importances": {k: round(v, 4) for k, v in importances.items()},
        "sensor_mapping": {
            "temperature": "BME280 ambient temperature (°C)",
            "humidity": "BME280 relative humidity (%RH)",
            "soil_moisture": "FC-28/YL-69 soil moisture sensor (%)",
            "nitrogen": "Soil test N (kg/ha)",
            "phosphorus": "Soil test P (kg/ha)",
            "potassium": "Soil test K (kg/ha)",
            "ph": "Soil test / pH sensor",
        },
        "trained_at": datetime.now().isoformat(),
        "dataset_source": "Synthetic (ICAR/FAO soil profiles, agronomic references)",
    }

    save_model_artifacts(
        model=model,
        scaler=scaler,
        label_encoders={"target": le_target},
        metadata=metadata,
        model_name="soil_type_classification"
    )

    return model, accuracy


def train_irrigation_prediction():
    """
    Model 4: Irrigation Prediction (PRIMARY MODEL for TerraFlow)
    Algorithm: XGBoost (or GradientBoosting fallback)
    Features: temperature, humidity, soil_moisture, soil_type, crop_type,
              N, P, K, pH, rainfall
    Target: irrigation_needed (0 or 1)

    This is the most important model — it directly drives TerraFlow's
    irrigation decision support alongside the rule-based engine.

    At inference: BME280 → temp + humidity,
                  soil moisture sensor → moisture,
                  soil test → N/P/K/pH,
                  weather API → rainfall,
                  user config → soil type + crop type
    """
    print("\n" + "=" * 60)
    print("MODEL 4: IRRIGATION PREDICTION (PRIMARY)")
    print("=" * 60)

    df = pd.read_csv(DATASET_DIR / "irrigation_prediction.csv")

    # Encode categorical
    le_soil = LabelEncoder()
    le_crop = LabelEncoder()

    df['soil_type_encoded'] = le_soil.fit_transform(df['soil_type'])
    df['crop_type_encoded'] = le_crop.fit_transform(df['crop_type'])

    feature_cols = ['temperature', 'humidity', 'soil_moisture',
                    'soil_type_encoded', 'crop_type_encoded',
                    'nitrogen', 'phosphorus', 'potassium',
                    'ph', 'rainfall']

    X = df[feature_cols].values
    y = df['irrigation_needed'].values

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42, stratify=y
    )

    if HAS_XGBOOST:
        model = XGBClassifier(
            n_estimators=300,
            max_depth=8,
            learning_rate=0.05,
            subsample=0.8,
            colsample_bytree=0.8,
            scale_pos_weight=len(y_train[y_train == 0]) / max(len(y_train[y_train == 1]), 1),
            random_state=42,
            eval_metric='logloss',
            verbosity=0,
        )
    else:
        model = GradientBoostingClassifier(
            n_estimators=300,
            max_depth=8,
            learning_rate=0.05,
            subsample=0.8,
            random_state=42,
        )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='binary')
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    cv_scores = cross_val_score(model, X_scaled, y, cv=5, scoring='accuracy')

    print(f"\n  Accuracy:   {accuracy:.4f}")
    print(f"  F1 Score:   {f1:.4f}")
    print(f"  Precision:  {precision:.4f}")
    print(f"  Recall:     {recall:.4f}")
    print(f"  CV Accuracy: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    print(f"\n  Confusion Matrix:")
    print(f"    TN={cm[0][0]:4d}  FP={cm[0][1]:4d}")
    print(f"    FN={cm[1][0]:4d}  TP={cm[1][1]:4d}")

    # Feature importance
    if HAS_XGBOOST:
        importances = dict(zip(feature_cols, model.feature_importances_))
    else:
        importances = dict(zip(feature_cols, model.feature_importances_))
    print(f"\n  Feature importances:")
    for k, v in sorted(importances.items(), key=lambda x: -x[1]):
        bar = '█' * int(v * 50)
        print(f"    {k:25s}: {v:.4f} {bar}")

    metadata = {
        "model_name": "irrigation_prediction",
        "algorithm": "XGBClassifier" if HAS_XGBOOST else "GradientBoostingClassifier",
        "features": feature_cols,
        "features_raw": ['temperature', 'humidity', 'soil_moisture',
                         'soil_type', 'crop_type',
                         'nitrogen', 'phosphorus', 'potassium',
                         'ph', 'rainfall'],
        "target": "irrigation_needed",
        "classes": ["NO_IRRIGATION", "IRRIGATE"],
        "num_classes": 2,
        "soil_type_mapping": dict(zip(le_soil.classes_.tolist(),
                                       range(len(le_soil.classes_)))),
        "crop_type_mapping": dict(zip(le_crop.classes_.tolist(),
                                       range(len(le_crop.classes_)))),
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "accuracy": round(accuracy, 4),
        "f1_binary": round(f1, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "cv_accuracy_mean": round(cv_scores.mean(), 4),
        "cv_accuracy_std": round(cv_scores.std(), 4),
        "confusion_matrix": cm.tolist(),
        "feature_importances": {k: round(float(v), 4) for k, v in importances.items()},
        "sensor_mapping": {
            "temperature": "BME280 ambient temperature (°C)",
            "humidity": "BME280 relative humidity (%RH)",
            "soil_moisture": "FC-28/YL-69 soil moisture sensor (%)",
            "soil_type": "User configuration / soil classifier",
            "crop_type": "User selection",
            "nitrogen": "Soil test N (kg/ha)",
            "phosphorus": "Soil test P (kg/ha)",
            "potassium": "Soil test K (kg/ha)",
            "ph": "Soil test / pH sensor",
            "rainfall": "Weather API (mm)",
        },
        "decision_logic": (
            "Ground truth generated from FAO-56 inspired rules: "
            "soil moisture depletion vs crop-specific thresholds, "
            "VPD-based ET demand, rainfall offset, soil drainage factors."
        ),
        "trained_at": datetime.now().isoformat(),
        "dataset_source": "Synthetic (FAO-56 crop water requirement logic)",
    }

    save_model_artifacts(
        model=model,
        scaler=scaler,
        label_encoders={"soil_type": le_soil, "crop_type": le_crop},
        metadata=metadata,
        model_name="irrigation_prediction"
    )

    return model, accuracy


# ═══════════════════════════════════════════════════════════════════════════
# MAIN EXECUTION
# ═══════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("╔" + "═" * 58 + "╗")
    print("║   TerraFlow BioAI — ML Model Training Pipeline            ║")
    print("║   4 Models × Sensor-Aligned Features                      ║")
    print("╚" + "═" * 58 + "╝")
    print()

    results = {}

    m1, a1 = train_crop_recommendation()
    results["crop_recommendation"] = a1

    m2, a2 = train_fertilizer_recommendation()
    results["fertilizer_recommendation"] = a2

    m3, a3 = train_soil_type_classification()
    results["soil_type_classification"] = a3

    m4, a4 = train_irrigation_prediction()
    results["irrigation_prediction"] = a4

    print("\n" + "═" * 60)
    print("TRAINING SUMMARY")
    print("═" * 60)
    for name, acc in results.items():
        status = "✓" if acc > 0.85 else "△" if acc > 0.7 else "✗"
        print(f"  {status} {name:35s} Accuracy: {acc:.4f}")

    print("\n  All models saved to:", MODEL_DIR)
    print("  Each model directory contains:")
    print("    - model.joblib          (trained model)")
    print("    - scaler.joblib         (feature scaler)")
    print("    - label_encoders.joblib (category encoders)")
    print("    - metadata.json         (features, metrics, sensor mapping)")
    print()

