// ============================================================================
// Power Query (M) Transformations & Table References
// Project: Telecom Customer Churn Analysis
// Source: Pivotalstats Portfolio Project
// ============================================================================

/*
-------------------------------------------------------------------------------
1. Table: prod_Churn (Add Calculated Columns)
-------------------------------------------------------------------------------
In Power Query or DAX calculated columns:

a) Churn Status:
   Churn Status = if [Customer_Status] = "Churned" then 1 else 0
   (Change data type to Whole Number / Int64.Type)

b) Monthly Charge Range:
   Monthly Charge Range = 
       if [Monthly_Charge] < 20 then "< 20" 
       else if [Monthly_Charge] < 50 then "20-50" 
       else if [Monthly_Charge] < 100 then "50-100" 
       else "> 100"
*/

// M Code for prod_Churn enhancements:
let
    Source = Sql.Database("YOUR_SERVER_NAME", "db_Churn"),
    dbo_prod_Churn = Source{[Schema="dbo",Item="prod_Churn"]}[Data],
    
    // Add Churn Status (1 for Churned, 0 otherwise)
    AddChurnStatus = Table.AddColumn(dbo_prod_Churn, "Churn Status", each if [Customer_Status] = "Churned" then 1 else 0, Int64.Type),
    
    // Add Monthly Charge Range
    AddChargeRange = Table.AddColumn(AddChurnStatus, "Monthly Charge Range", each 
        if [Monthly_Charge] < 20 then "< 20" 
        else if [Monthly_Charge] < 50 then "20-50" 
        else if [Monthly_Charge] < 100 then "50-100" 
        else "> 100", 
        type text
    )
in
    AddChargeRange


/*
-------------------------------------------------------------------------------
2. Table: mapping_AgeGrp (Reference Table)
-------------------------------------------------------------------------------
Steps:
1. Reference prod_Churn.
2. Select only the "Age" column and Remove Duplicates.
3. Add custom column "Age Group":
   if [Age] < 20 then "< 20" else if [Age] < 36 then "20 - 35" else if [Age] < 51 then "36 - 50" else "> 50"
4. Add custom column "AgeGrpSorting":
   if [Age Group] = "< 20" then 1 else if [Age Group] = "20 - 35" then 2 else if [Age Group] = "36 - 50" then 3 else 4
5. Change data type of AgeGrpSorting to Int64.Type.
6. In Power BI Data View, select 'Age Group' and click 'Sort by column' -> 'AgeGrpSorting'.
*/

// M Code for mapping_AgeGrp:
let
    Source = prod_Churn,
    SelectAge = Table.SelectColumns(Source, {"Age"}),
    RemoveDuplicates = Table.Distinct(SelectAge),
    AddAgeGroup = Table.AddColumn(RemoveDuplicates, "Age Group", each 
        if [Age] < 20 then "< 20" 
        else if [Age] < 36 then "20 - 35" 
        else if [Age] < 51 then "36 - 50" 
        else "> 50", 
        type text
    ),
    AddSorting = Table.AddColumn(AddAgeGroup, "AgeGrpSorting", each 
        if [Age Group] = "< 20" then 1 
        else if [Age Group] = "20 - 35" then 2 
        else if [Age Group] = "36 - 50" then 3 
        else 4, 
        Int64.Type
    )
in
    AddSorting


/*
-------------------------------------------------------------------------------
3. Table: mapping_TenureGrp (Reference Table)
-------------------------------------------------------------------------------
Steps:
1. Reference prod_Churn.
2. Select only the "Tenure_in_Months" column and Remove Duplicates.
3. Add custom column "Tenure Group":
   if [Tenure_in_Months] < 6 then "< 6 Months" 
   else if [Tenure_in_Months] < 12 then "6-12 Months" 
   else if [Tenure_in_Months] < 18 then "12-18 Months" 
   else if [Tenure_in_Months] < 24 then "18-24 Months" 
   else ">= 24 Months"
4. Add custom column "TenureGrpSorting":
   if [Tenure_in_Months] = "< 6 Months" then 1 
   else if [Tenure_in_Months] = "6-12 Months" then 2 
   else if [Tenure_in_Months] = "12-18 Months" then 3 
   else if [Tenure_in_Months] = "18-24 Months " then 4 
   else 5
5. Change data type of TenureGrpSorting to Int64.Type.
6. In Power BI Data View, select 'Tenure Group' and click 'Sort by column' -> 'TenureGrpSorting'.
*/

// M Code for mapping_TenureGrp:
let
    Source = prod_Churn,
    SelectTenure = Table.SelectColumns(Source, {"Tenure_in_Months"}),
    RemoveDuplicates = Table.Distinct(SelectTenure),
    AddTenureGroup = Table.AddColumn(RemoveDuplicates, "Tenure Group", each 
        if [Tenure_in_Months] < 6 then "< 6 Months" 
        else if [Tenure_in_Months] < 12 then "6-12 Months" 
        else if [Tenure_in_Months] < 18 then "12-18 Months" 
        else if [Tenure_in_Months] < 24 then "18-24 Months" 
        else ">= 24 Months", 
        type text
    ),
    AddSorting = Table.AddColumn(AddTenureGroup, "TenureGrpSorting", each 
        if [Tenure Group] = "< 6 Months" then 1 
        else if [Tenure Group] = "6-12 Months" then 2 
        else if [Tenure Group] = "12-18 Months" then 3 
        else if [Tenure Group] = "18-24 Months" then 4 
        else 5, 
        Int64.Type
    )
in
    AddSorting


/*
-------------------------------------------------------------------------------
4. Table: prod_Services (Unpivoted Service Attributes)
-------------------------------------------------------------------------------
Steps:
1. Reference prod_Churn.
2. Select Customer_ID, Churn Status, Customer_Status, plus service columns:
   Phone_Service, Multiple_Lines, Internet_Service, Online_Security,
   Online_Backup, Device_Protection_Plan, Premium_Support,
   Streaming_TV, Streaming_Movies, Streaming_Music, Unlimited_Data.
3. Unpivot the service columns.
4. Rename:
   "Attribute" -> "Services"
   "Value"     -> "Status"
*/

// M Code for prod_Services:
let
    Source = prod_Churn,
    SelectColumns = Table.SelectColumns(Source, {
        "Customer_ID", "Churn Status", "Customer_Status",
        "Phone_Service", "Multiple_Lines", "Internet_Service",
        "Online_Security", "Online_Backup", "Device_Protection_Plan",
        "Premium_Support", "Streaming_TV", "Streaming_Movies",
        "Streaming_Music", "Unlimited_Data"
    }),
    UnpivotServices = Table.UnpivotOtherColumns(
        SelectColumns, 
        {"Customer_ID", "Churn Status", "Customer_Status"}, 
        "Services", 
        "Status"
    )
in
    UnpivotServices
