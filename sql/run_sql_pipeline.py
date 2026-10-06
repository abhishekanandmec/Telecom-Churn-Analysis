#!/usr/bin/env python3
"""
SQL ETL Pipeline Runner (SQLite / Python)
Replicates the Microsoft SQL Server ETL process locally without needing SSMS.
Loads raw CSV data, profiles data, handles NULLs, creates production tables,
and exports the views and Power BI tables.
"""

import os
import sqlite3
import pandas as pd

def run_etl():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    raw_csv_path = os.path.join(repo_root, "data", "raw", "Customer_Data.csv")
    processed_dir = os.path.join(repo_root, "data", "processed")
    os.makedirs(processed_dir, exist_ok=True)

    print(f"Loading raw data from: {raw_csv_path}")
    raw_df = pd.read_csv(raw_csv_path)
    print(f"Raw records loaded: {len(raw_df)}")

    # Connect to local SQLite database
    db_path = os.path.join(processed_dir, "db_Churn.sqlite")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Step 1: Load into staging table
    raw_df.to_sql("stg_Churn", conn, if_exists="replace", index=False)
    print("Loaded data into staging table: stg_Churn")

    # Step 2: Data Exploration (Null checks & distributions)
    cursor.execute("""
        SELECT Gender, COUNT(Gender) AS TotalCount,
               ROUND(COUNT(Gender) * 1.0 / (SELECT COUNT(*) FROM stg_Churn), 4) AS Percentage
        FROM stg_Churn GROUP BY Gender
    """)
    print("\n[Data Exploration - Gender Distribution]:")
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]} ({row[2]*100:.2f}%)")

    cursor.execute("""
        SELECT Customer_Status, COUNT(Customer_Status) AS TotalCount,
               ROUND(SUM(Total_Revenue), 2) AS TotalRev,
               ROUND(SUM(Total_Revenue) / (SELECT SUM(Total_Revenue) FROM stg_Churn) * 100, 2) AS RevPercentage
        FROM stg_Churn GROUP BY Customer_Status
    """)
    print("\n[Data Exploration - Customer Status Distribution]:")
    for row in cursor.fetchall():
        print(f"  {row[0]}: Count={row[1]}, Total Revenue=${row[2]:,.2f} ({row[3]:.2f}%)")

    # Step 3: ETL - Clean NULLs into prod_Churn
    cursor.execute("DROP TABLE IF EXISTS prod_Churn")
    cursor.execute("""
        CREATE TABLE prod_Churn AS
        SELECT 
            Customer_ID,
            Gender,
            Age,
            Married,
            State,
            Number_of_Referrals,
            Tenure_in_Months,
            COALESCE(Value_Deal, 'None') AS Value_Deal,
            Phone_Service,
            COALESCE(Multiple_Lines, 'No') AS Multiple_Lines,
            Internet_Service,
            COALESCE(Internet_Type, 'None') AS Internet_Type,
            COALESCE(Online_Security, 'No') AS Online_Security,
            COALESCE(Online_Backup, 'No') AS Online_Backup,
            COALESCE(Device_Protection_Plan, 'No') AS Device_Protection_Plan,
            COALESCE(Premium_Support, 'No') AS Premium_Support,
            COALESCE(Streaming_TV, 'No') AS Streaming_TV,
            COALESCE(Streaming_Movies, 'No') AS Streaming_Movies,
            COALESCE(Streaming_Music, 'No') AS Streaming_Music,
            COALESCE(Unlimited_Data, 'No') AS Unlimited_Data,
            Contract,
            Paperless_Billing,
            Payment_Method,
            Monthly_Charge,
            Total_Charges,
            Total_Refunds,
            Total_Extra_Data_Charges,
            Total_Long_Distance_Charges,
            Total_Revenue,
            Customer_Status,
            COALESCE(Churn_Category, 'Others') AS Churn_Category,
            COALESCE(Churn_Reason, 'Others') AS Churn_Reason
        FROM stg_Churn
    """)
    conn.commit()
    print("\nSuccessfully populated production table: prod_Churn")

    # Step 4: Create Views
    cursor.execute("DROP VIEW IF EXISTS vw_ChurnData")
    cursor.execute("""
        CREATE VIEW vw_ChurnData AS
        SELECT * FROM prod_Churn WHERE Customer_Status IN ('Churned', 'Stayed')
    """)

    cursor.execute("DROP VIEW IF EXISTS vw_JoinData")
    cursor.execute("""
        CREATE VIEW vw_JoinData AS
        SELECT * FROM prod_Churn WHERE Customer_Status = 'Joined'
    """)
    conn.commit()

    # Step 5: Export processed CSV files
    prod_churn_df = pd.read_sql("SELECT * FROM prod_Churn", conn)
    vw_churn_df = pd.read_sql("SELECT * FROM vw_ChurnData", conn)
    vw_join_df = pd.read_sql("SELECT * FROM vw_JoinData", conn)

    prod_churn_df.to_csv(os.path.join(processed_dir, "prod_Churn.csv"), index=False)
    vw_churn_df.to_csv(os.path.join(processed_dir, "vw_ChurnData.csv"), index=False)
    vw_join_df.to_csv(os.path.join(processed_dir, "vw_JoinData.csv"), index=False)
    print(f"Exported prod_Churn.csv ({len(prod_churn_df)} rows)")
    print(f"Exported vw_ChurnData.csv ({len(vw_churn_df)} rows)")
    print(f"Exported vw_JoinData.csv ({len(vw_join_df)} rows)")

    # Step 6: Generate Power BI Transform Reference Tables
    # 6.1 mapping_AgeGrp
    age_unique = prod_churn_df[['Age']].drop_duplicates().sort_values('Age').reset_index(drop=True)
    def map_age_group(age):
        if age < 20: return "< 20", 1
        elif age < 36: return "20 - 35", 2
        elif age < 51: return "36 - 50", 3
        else: return "> 50", 4
    
    age_groups = [map_age_group(a) for a in age_unique['Age']]
    mapping_AgeGrp = pd.DataFrame({
        'Age': age_unique['Age'],
        'Age Group': [g[0] for g in age_groups],
        'AgeGrpSorting': [g[1] for g in age_groups]
    })
    mapping_AgeGrp.to_csv(os.path.join(processed_dir, "mapping_AgeGrp.csv"), index=False)
    print(f"Exported mapping_AgeGrp.csv ({len(mapping_AgeGrp)} rows)")

    # 6.2 mapping_TenureGrp
    tenure_unique = prod_churn_df[['Tenure_in_Months']].drop_duplicates().sort_values('Tenure_in_Months').reset_index(drop=True)
    def map_tenure_group(tenure):
        if tenure < 6: return "< 6 Months", 1
        elif tenure < 12: return "6-12 Months", 2
        elif tenure < 18: return "12-18 Months", 3
        elif tenure < 24: return "18-24 Months", 4
        else: return ">= 24 Months", 5
    
    tenure_groups = [map_tenure_group(t) for t in tenure_unique['Tenure_in_Months']]
    mapping_TenureGrp = pd.DataFrame({
        'Tenure_in_Months': tenure_unique['Tenure_in_Months'],
        'Tenure Group': [g[0] for g in tenure_groups],
        'TenureGrpSorting': [g[1] for g in tenure_groups]
    })
    mapping_TenureGrp.to_csv(os.path.join(processed_dir, "mapping_TenureGrp.csv"), index=False)
    print(f"Exported mapping_TenureGrp.csv ({len(mapping_TenureGrp)} rows)")

    # 6.3 prod_Services (Unpivoted services)
    service_cols = [
        'Phone_Service', 'Multiple_Lines', 'Internet_Service', 'Online_Security',
        'Online_Backup', 'Device_Protection_Plan', 'Premium_Support',
        'Streaming_TV', 'Streaming_Movies', 'Streaming_Music', 'Unlimited_Data'
    ]
    # Keep Customer_ID, Churn Status, etc. for slicing
    prod_churn_df['Churn Status'] = prod_churn_df['Customer_Status'].apply(lambda x: 1 if x == 'Churned' else 0)
    prod_services = pd.melt(
        prod_churn_df,
        id_vars=['Customer_ID', 'Customer_Status', 'Churn Status'],
        value_vars=service_cols,
        var_name='Services',
        value_name='Status'
    )
    prod_services.to_csv(os.path.join(processed_dir, "prod_Services.csv"), index=False)
    print(f"Exported prod_Services.csv ({len(prod_services)} rows)")

    conn.close()
    print("\nETL Pipeline execution completed successfully.")

if __name__ == "__main__":
    run_etl()
