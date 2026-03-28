# PhonePe
Phonepe DataAnalysis program. Code is written in Python.

Tech Stack
1. Python
2. Postgress database
2. DataVisualization using Streamlit.

It has two code files, one is related to dataload which will fetch data from repo and download json files, Python code loads json data into Postgress database.

Using SQL query data is represented in tabular and chart form for analysis using Streamlit 

Steps Involved:

1. Clone the GitHub repository containing PhonePe transaction data and load it into a SQL database using Python
2. Data loads into following tables using Dataload python notebook
   a) Aggregated Tables:
        Aggregated_user: Holds aggregated user-related data.
        aggtransaction : Contains aggregated values for map-related data.
        agginsurance: Stores aggregated insurance-related data.
   b) Map Tables:
        aggMapUsers: Contains mapping information for users.
        aggMapTransaction: Holds mapping values for total amounts at state and district levels.
        aggMapInsurance: Includes mapping information related to insurance.
   c) Top Tables:
        aggTopUsers: Lists totals for the top users.
        aggTopTransaction: Contains totals for the top states, districts, and pin codes.
        aggTopInsurance: Lists totals for the top insurance categories.
3. Data Analysis Using Python :
       a) Used plotly express, Streamlit and Pandas to analyze result from SQL
       b) Created bar chart
       c) Dashboard is created using streamlit 
