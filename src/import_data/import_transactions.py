import pandas as pd
import math
from src import settings
from src.db import db

transaction_db = db["transaction"]
customer_db = db["customers"]
film_db = db["films"]
time_db = db["time"]

def import_transaction():
    try:
        if transaction_db.count_documents({}) != 0:
            transaction_db.drop()
    except Exception as e:
        print(f"Error dropping existing documents: {e}")
    
    transaction_db.create_index([
        ('orderid', 1), ('customerid', 1), ('show_id', 1), ('transaction_datetime', 1), ('time_id', 1)
    ], unique=True)

    # Đọc dữ liệu từ file Excel
    sheets = pd.read_excel(settings.input_path, sheet_name=['ticket'])
    df_ticket = sheets['ticket']
    

    df_ticket['transaction_datetime'] = pd.to_datetime(df_ticket['date'].astype(str) + ' ' + df_ticket['time'].astype(str))

    
    df_ticket['customer'] = df_ticket.apply(lambda x: customer_db.find_one({'customerid': x['customerid']}), axis=1)
    df_ticket = df_ticket[df_ticket['customer'].notnull()]

    df_ticket['film_data'] = df_ticket.apply(lambda x: film_db.find_one({'title': x['film']}), axis=1)
    df_ticket = df_ticket[df_ticket['film_data'].notnull()]

    # Thêm trường `show_id` từ dữ liệu `film_data`
    df_ticket['show_id'] = df_ticket['film_data'].apply(lambda x: x['show_id'] if x else None)

    df_ticket['year'] = df_ticket['transaction_datetime'].dt.year
    df_ticket['month'] = df_ticket['transaction_datetime'].dt.month
    df_ticket['day'] = df_ticket['transaction_datetime'].dt.day
    df_ticket['hour'] = df_ticket['transaction_datetime'].dt.hour
    df_ticket['minutes'] = df_ticket['transaction_datetime'].dt.minute

    df_ticket['transaction_time'] = df_ticket.apply(lambda x: time_db.find_one(
        {'year': x['year'], 'month': x['month'], 'day': x['day'], 'hour': x['hour'], 'minutes': x['minutes']}), axis=1)
    df_ticket = df_ticket[df_ticket['transaction_time'].notnull()]

    ndict = {}
    for _, data in df_ticket.iterrows():
        # Tạo khóa duy nhất cho mỗi giao dịch
        id_and_time = f"{data['orderid']}-{data['customerid']}-{data['show_id']}-{data['transaction_datetime']}"

       
        if any(pd.isna(val) or val is None or (isinstance(val, float) and math.isnan(val)) 
               for val in [data['orderid'], data['customerid'], data['show_id'], data['transaction_datetime'], data['transaction_time']]):
            continue

        if id_and_time not in ndict:
            ndict[id_and_time] = {
                'orderid': data['orderid'],
                'transaction_datetime': data['transaction_datetime'],
                'total': data['total'],
                'ticketcodes': [data['ticketcode']],
                'customer_id': data['customer']['customerid'],
                'film_id': data['show_id'],
                'time_id': data['transaction_time']['time_id'],
                'cashier': data['cashier'],
                'ticket_price': data['ticket price']
            }
        else:
            ndict[id_and_time]['ticketcodes'].append(data['ticketcode'])

    transaction_dict = list(ndict.values())

    # Chèn dữ liệu vào `transaction_db`
    inserted_transactions = []
    for transaction_record in transaction_dict:
        try:
            transaction_db.insert_one(transaction_record)
            inserted_transactions.append(transaction_record)
        except Exception as e:
            print(f"Error inserting transaction: {e}")

    print(inserted_transactions[:5])
    print(f"Total Transactions Inserted: {len(inserted_transactions)}")
