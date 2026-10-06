-- ============================================================================
-- Step 4: Create Views for Power BI & Machine Learning
-- Project: Telecom Customer Churn Analysis
-- Source: Pivotalstats Portfolio Project
-- ============================================================================

USE db_Churn;
GO

-- View 1: Historical customer data (Stayed and Churned)
-- Used for Power BI analysis and ML Model training/testing
CREATE VIEW vw_ChurnData AS
SELECT * 
FROM prod_Churn 
WHERE Customer_Status IN ('Churned', 'Stayed');
GO

-- View 2: New joiner customer data (Joined)
-- Used for running ML churn predictions on newly joined customers
CREATE VIEW vw_JoinData AS
SELECT * 
FROM prod_Churn 
WHERE Customer_Status = 'Joined';
GO
