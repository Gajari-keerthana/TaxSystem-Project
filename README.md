                                                                                       **Tax and Payment Tracking System**
_Overview_
  This project aims to develop a Tax and Payment Tracking System for small businesses, such as LLC, C, Corporations, or S Corporations.The system is designed to help tack, calculate, and save tax payment records 
  for these companies, making it easier to manage and meet annual tax obligations.

 _ Tech Stack_
. Backend Framework: Python Flask (Microservice Architecture)
. Database: SQLite (SQL syntax similar to MySQL or PostgreSQL for simplicity)
. UI: Frontend with CRUD operations(Create, Read, Update, Delete) for interacting with tax records.

_Key Features_
1. HTTP Endpoints:
   . POST: Add new tax payment records to the database.
   . GET: View all tax payment records for the year.
2. UI Feautures:
   . Perform CRUD operations(Inser, Save, Update, Delete) on the tax payment records.
3. Database:
   . Store and retrieve tax payment records using SQLite.
   . Tables are structured to track yearly payments and estimate future payments.

_Project Description_
  This system will assit LLCs and similar small companies in tracking their tax payments to the NJ State tax office. Every year, these companies are required to make estimated tax payments four times a year, 
  on the following dates:
  . April 15
  . June 15
  . September 15
  . January 15 (of the following year)

  The system provides:
  1. Tax Calculation and Tracking:
     . Help LLCs track the tax payments they have made.
     .Save these payments to the database for future reference and calulations.
  2. Web Interface:
     . An easy-to-use web UI for entering tax payment values and managing them through CRUD operations.
  3. Payment Management:
     . Users can view all tax payments made within the year and add new payments via the web UI.

_Future Improvements_
. Integration with external payment gateways.
. Support for additional tax calculations and forms
. Export tax record to CSV or PDF for easy reporting


    
