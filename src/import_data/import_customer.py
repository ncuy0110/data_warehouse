import pandas as pd
from src import settings
from src.db import db
from datetime import datetime, timedelta
customer_db = db["customers"]

def import_customer():
    try:
        if customer_db.count_documents({}) != 0:
            customer_db.drop()
    except:
        pass

    df = pd.read_excel(settings.input_path, sheet_name='customer')

    # Extract unique customers
    customers = df[['customerid', 'DOB', 'gender', 'address', 'Website', 'job', 'industry']].drop_duplicates()

  
    if pd.api.types.is_numeric_dtype(customers['DOB']):
       
        customers['DOB'] = pd.to_datetime('1899-12-30') + pd.to_timedelta(customers['DOB'], 'D')
    else:
       
        customers['DOB'] = pd.to_datetime(customers['DOB'], errors='coerce')

    customers['DOB'] = customers['DOB'].dt.strftime('%d-%m-%Y')

    customers_dict = customers.to_dict(orient='records')

    print(customers_dict[:5])  
    print(len(customers_dict))  

    for customer in customers_dict:
        try:
            customer_db.insert_one(customer)
        except Exception as e:
            print(f"Lỗi khi chèn dữ liệu: {e}")  # In ra lỗi nếu có
