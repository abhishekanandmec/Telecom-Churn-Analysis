# Power BI Dashboard Specification

This document provides a precise, visual-by-visual design guide to build the Telecom Churn Analysis dashboard in Power BI Desktop, matching the tutorial and video.

---

## 1. Global Setup & Canvas Formatting

- **Canvas Size**: 16:9 (`1280 x 720` px)
- **Theme Color Palette**:
  - Primary Indigo: `#4A44F2`
  - Secondary Lavender: `#9B9FF2`
  - Light Accent Blue: `#A0D1FF`
  - Background Neutral: `#F2F2F2`
  - Dark Neutral: `#1E1E2C` / `#0A083B`
- **Default Font**: Segoe UI / Poppins
- **Page Canvas Backgrounds**:
  - **Summary Page**: Insert `powerbi/assets/backgrounds/Summary.PNG` (Image Fit: Fit / Normal, Transparency: 0%).
  - **Churn Prediction Page**: Insert `powerbi/assets/backgrounds/Prediction.PNG` (Image Fit: Fit / Normal, Transparency: 0%).

---

## 2. Page 1: Summary Page (`Summary.PNG`)

### Top KPI Cards (Top Banner)
1. **Total Customers**:
   - Visual: Card
   - Field: `[Total Customers]`
   - Callout Value: Large Bold, Font Color: Dark Slate / White depending on box contrast
2. **New Joiners**:
   - Visual: Card
   - Field: `[New Joiners]`
3. **Total Churn**:
   - Visual: Card
   - Field: `[Total Churn]`
4. **Churn Rate %**:
   - Visual: Card
   - Field: `[Churn Rate]` (Format: `0.0%`)

---

### Section A: Demographic Analysis
1. **Gender – Churn Rate**:
   - Visual: Donut Chart / Clustered Column
   - Legend/Axis: `prod_Churn[Gender]`
   - Values: `[Churn Rate]`
   - Decorative: Insert gender icons `powerbi/assets/icons/Ico_Gender.png` and `Ico_Gender2.png`.
2. **Age Group – Total Customers & Churn Rate**:
   - Visual: Line and Clustered Column Chart
   - Shared Axis: `mapping_AgeGrp[Age Group]` (Sorted by `AgeGrpSorting`)
   - Column Values: `[Total Customers]`
   - Line Values: `[Churn Rate]`

---

### Section B: Account & Payment Info
1. **Payment Method – Churn Rate**:
   - Visual: Clustered Bar Chart (Horizontal)
   - Y-Axis: `prod_Churn[Payment_Method]`
   - X-Axis: `[Churn Rate]`
2. **Contract – Churn Rate**:
   - Visual: Clustered Column Chart
   - X-Axis: `prod_Churn[Contract]` (Month-to-month, One year, Two year)
   - Y-Axis: `[Churn Rate]`
3. **Tenure Group – Total Customers & Churn Rate**:
   - Visual: Line and Clustered Column Chart
   - Shared Axis: `mapping_TenureGrp[Tenure Group]` (Sorted by `TenureGrpSorting`)
   - Column Values: `[Total Customers]`
   - Line Values: `[Churn Rate]`

---

### Section C: Geographic Analysis
1. **Top 5 State – Churn Rate**:
   - Visual: Clustered Bar Chart
   - Y-Axis: `prod_Churn[State]`
   - X-Axis: `[Churn Rate]`
   - Filters on Visual: Top N -> Top 5 by `[Churn Rate]`

---

### Section D: Churn Distribution & Tooltip Drilldown
1. **Churn Category – Total Churn**:
   - Visual: Clustered Bar / Column Chart
   - Axis: `prod_Churn[Churn_Category]` (Competitor, Dissatisfaction, Price, Attitude, Others)
   - Values: `[Total Churn]`
   - Tooltip Page Setting: Link to **Churn Reason (Tooltip Page)**.

---

### Section E: Services Used
1. **Internet Type – Churn Rate**:
   - Visual: Clustered Bar Chart
   - Axis: `prod_Churn[Internet_Type]` (Fiber Optic, DSL, Cable, None)
   - Values: `[Churn Rate]`
2. **prod_Service >> Services – Status Breakdown**:
   - Visual: 100% Stacked Bar Chart or Matrix
   - Axis: `prod_Services[Services]`
   - Legend: `prod_Services[Status]`
   - Values: `% RT Sum of Churn Status` / Churn distribution by service adoption.

---

## 3. Tooltip Page: Churn Reason Page

- **Page Type**: Tooltip (`320 x 240` px or small canvas)
- **Visual**:
  - Clustered Bar Chart:
    - Y-Axis: `prod_Churn[Churn_Reason]`
    - X-Axis: `[Total Churn]`
    - Data Labels: On

---

## 4. Page 2: Churn Prediction Page (`Prediction.PNG`)

Uses the new predicted data table (`Predictions` imported from `Predictions.csv`).

### KPI Card (Header Banner)
- **Visual**: Card Visual
- **Field**: `[Count Predicted Churner]` or `[Title Predicted Churners]`
- **Value**: Shows `381` predicted churners out of 411 new joiners.

### Customer Detail Grid (Right Side)
- **Visual**: Table / Grid
- **Columns**:
  1. `Predictions[Customer_ID]`
  2. `Predictions[Monthly_Charge]` (Currency format)
  3. `Predictions[Total_Revenue]` (Currency format)
  4. `Predictions[Total_Refunds]`
  5. `Predictions[Number_of_Referrals]`

### Demographic Breakdown (Left / Center)
1. **Gender – Churn Count**:
   - Visual: Bar / Donut Chart
   - Category: `Predictions[Gender]`
   - Values: `COUNT(Predictions[Customer_ID])`
2. **Age Group – Churn Count**:
   - Visual: Column Chart
   - Category: Age Group derived / `Predictions[Age]`
   - Values: `COUNT(Predictions[Customer_ID])`
3. **Marital Status – Churn Count**:
   - Visual: Bar Chart / Card
   - Category: `Predictions[Married]`
   - Values: `COUNT(Predictions[Customer_ID])`

### Account Info Breakdown
1. **Payment Method – Churn Count**:
   - Visual: Bar Chart
   - Category: `Predictions[Payment_Method]`
   - Values: `COUNT(Predictions[Customer_ID])`
2. **Contract – Churn Count**:
   - Visual: Column Chart
   - Category: `Predictions[Contract]`
   - Values: `COUNT(Predictions[Customer_ID])`
3. **Tenure Group – Churn Count**:
   - Visual: Column Chart
   - Category: `Predictions[Tenure_in_Months]`
   - Values: `COUNT(Predictions[Customer_ID])`

### Geographic Breakdown
1. **State – Churn Count**:
   - Visual: Horizontal Bar Chart
   - Category: `Predictions[State]`
   - Values: `COUNT(Predictions[Customer_ID])`
