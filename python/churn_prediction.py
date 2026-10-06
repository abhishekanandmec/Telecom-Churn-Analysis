#!/usr/bin/env python3
"""
Step 5 - Predict Customer Churn using Random Forest
Project: Telecom Customer Churn Analysis
Source: Pivotalstats Portfolio Project

This script trains a Random Forest Classifier on historical churn data (vw_ChurnData),
evaluates model performance, plots feature importances, and predicts churn risk
for new joiners (vw_JoinData), outputting 'Predictions.csv'.
"""

import os
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

def run_churn_modeling():
    # Resolve directory paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    processed_dir = os.path.join(repo_root, "data", "processed")
    outputs_dir = os.path.join(script_dir, "outputs")
    os.makedirs(outputs_dir, exist_ok=True)

    # 1. Importing Libraries & Data Load
    churn_data_path = os.path.join(processed_dir, "vw_ChurnData.csv")
    print(f"Loading historical churn data from: {churn_data_path}")
    data = pd.read_csv(churn_data_path)
    print("Initial Data Head:\n", data.head())

    # 2. Data Preprocessing
    # Drop columns that won't be used for prediction
    data = data.drop(['Customer_ID', 'Churn_Category', 'Churn_Reason'], axis=1)

    # List of columns to be label encoded
    columns_to_encode = [
        'Gender', 'Married', 'State', 'Value_Deal', 'Phone_Service', 'Multiple_Lines',
        'Internet_Service', 'Internet_Type', 'Online_Security', 'Online_Backup',
        'Device_Protection_Plan', 'Premium_Support', 'Streaming_TV', 'Streaming_Movies',
        'Streaming_Music', 'Unlimited_Data', 'Contract', 'Paperless_Billing',
        'Payment_Method'
    ]

    # Encode categorical variables except the target variable
    label_encoders = {}
    for column in columns_to_encode:
        label_encoders[column] = LabelEncoder()
        data[column] = label_encoders[column].fit_transform(data[column])

    # Manually encode the target variable 'Customer_Status'
    data['Customer_Status'] = data['Customer_Status'].map({'Stayed': 0, 'Churned': 1})

    # Split data into features and target
    X = data.drop('Customer_Status', axis=1)
    y = data['Customer_Status']

    # Split data into training and testing sets (80/20)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"Train samples: {len(X_train)}, Test samples: {len(X_test)}")

    # 3. Train Random Forest Model
    print("\nTraining RandomForestClassifier(n_estimators=100, random_state=42)...")
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)

    # 4. Evaluate Model
    y_pred = rf_model.predict(X_test)

    cm = confusion_matrix(y_test, y_pred)
    cr = classification_report(y_test, y_pred)

    print("\nConfusion Matrix:")
    print(cm)
    print("\nClassification Report:")
    print(cr)

    # Save metrics to text file
    metrics_path = os.path.join(outputs_dir, "evaluation_metrics.txt")
    with open(metrics_path, "w") as f:
        f.write("Random Forest Model Evaluation Metrics\n")
        f.write("=" * 45 + "\n\n")
        f.write("Confusion Matrix:\n")
        f.write(np.array2string(cm) + "\n\n")
        f.write("Classification Report:\n")
        f.write(cr + "\n")
    print(f"Saved evaluation metrics to: {metrics_path}")

    # Feature Selection using Feature Importance
    importances = rf_model.feature_importances_
    indices = np.argsort(importances)[::-1]

    # Plot the feature importances
    plt.figure(figsize=(15, 6))
    sns.barplot(x=importances[indices], y=X.columns[indices], hue=X.columns[indices], legend=False, palette="viridis")
    plt.title('Feature Importances', fontsize=14, fontweight='bold')
    plt.xlabel('Relative Importance', fontsize=12)
    plt.ylabel('Feature Names', fontsize=12)
    plt.tight_layout()

    fig_path = os.path.join(outputs_dir, "feature_importances.png")
    plt.savefig(fig_path, dpi=300)
    plt.close()
    print(f"Saved feature importances plot to: {fig_path}")

    # Save model and encoders
    model_path = os.path.join(outputs_dir, "churn_rf_model.joblib")
    joblib.dump({"model": rf_model, "encoders": label_encoders}, model_path)
    print(f"Saved trained model and encoders to: {model_path}")

    # 5. Use Model for Prediction on New Data (vw_JoinData)
    join_data_path = os.path.join(processed_dir, "vw_JoinData.csv")
    print(f"\nLoading new joiner data from: {join_data_path}")
    new_data = pd.read_csv(join_data_path)
    print("New Joiner Data Head:\n", new_data.head())

    # Retain the original DataFrame to preserve unencoded columns
    original_data = new_data.copy()

    # Retain the Customer_ID column
    customer_ids = new_data['Customer_ID']

    # Drop columns that won't be used for prediction in the encoded DataFrame
    inference_features = new_data.drop(['Customer_ID', 'Customer_Status', 'Churn_Category', 'Churn_Reason'], axis=1)

    # Encode categorical variables using the saved label encoders
    for column in inference_features.select_dtypes(include=['object']).columns:
        inference_features[column] = label_encoders[column].transform(inference_features[column])

    # Make predictions
    new_predictions = rf_model.predict(inference_features)

    # Add predictions to the original DataFrame
    original_data['Customer_Status_Predicted'] = new_predictions

    # Filter the DataFrame to include only records predicted as "Churned"
    predicted_churners = original_data[original_data['Customer_Status_Predicted'] == 1]
    print(f"Total Joiners: {len(original_data)}")
    print(f"Count of Predicted Churners: {len(predicted_churners)}")

    # Save the results (both inside python/outputs and data/processed for Power BI import)
    pred_path_outputs = os.path.join(outputs_dir, "Predictions.csv")
    pred_path_data = os.path.join(processed_dir, "Predictions.csv")
    predicted_churners.to_csv(pred_path_outputs, index=False)
    predicted_churners.to_csv(pred_path_data, index=False)
    print(f"Saved predicted churners to:\n - {pred_path_outputs}\n - {pred_path_data}")

if __name__ == "__main__":
    run_churn_modeling()
