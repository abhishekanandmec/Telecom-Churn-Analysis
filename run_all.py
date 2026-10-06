#!/usr/bin/env python3
"""
Master Execution Script
Telecom Customer Churn Analysis Portfolio Project

Executes the entire end-to-end data pipeline:
1. SQL ETL: Data loading, profiling, NULL handling, and views creation.
2. Power Query mapping tables generation (mapping_AgeGrp, mapping_TenureGrp, prod_Services).
3. Machine Learning: Random Forest Classifier training, evaluation, feature importances,
   and batch inference on new joiners to output Predictions.csv.
"""

import sys
import os
import subprocess

def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    print("=" * 70)
    print("🚀 STARTING TELECOM CUSTOMER CHURN ANALYSIS PIPELINE")
    print("=" * 70)

    # 1. Run SQL ETL Pipeline
    print("\n[Step 1/2] Running SQL ETL Pipeline...")
    etl_script = os.path.join(root_dir, "sql", "run_sql_pipeline.py")
    res_etl = subprocess.run([sys.executable, etl_script], capture_output=False)
    if res_etl.returncode != 0:
        print("❌ Error in SQL ETL step.")
        sys.exit(res_etl.returncode)

    # 2. Run Machine Learning Pipeline
    print("\n[Step 2/2] Running Machine Learning Churn Modeling & Prediction...")
    ml_script = os.path.join(root_dir, "python", "churn_prediction.py")
    res_ml = subprocess.run([sys.executable, ml_script], capture_output=False)
    if res_ml.returncode != 0:
        print("❌ Error in Machine Learning step.")
        sys.exit(res_ml.returncode)

    print("\n" + "=" * 70)
    print("✅ END-TO-END PIPELINE COMPLETED SUCCESSFULLY!")
    print("=" * 70)
    print("Outputs generated:")
    print("  • data/processed/prod_Churn.csv")
    print("  • data/processed/vw_ChurnData.csv")
    print("  • data/processed/vw_JoinData.csv")
    print("  • data/processed/Predictions.csv (381 predicted churners)")
    print("  • python/outputs/feature_importances.png")
    print("  • python/outputs/evaluation_metrics.txt")
    print("  • notebooks/churn_prediction_model.ipynb")
    print("=" * 70)

if __name__ == "__main__":
    main()
