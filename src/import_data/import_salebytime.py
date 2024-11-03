import pandas as pd
from src import settings
from src.db import db

sales_by_time_db = db["sales_by_time"]
time_db = db["time"]

def import_sales_by_time():
    try:
        if sales_by_time_db.count_documents({}) != 0:
            sales_by_time_db.drop()
    except:
        pass
    
    # Đọc dữ liệu từ bảng `ticket` trong file Excel
    df = pd.read_excel(settings.input_path, sheet_name='ticket')

    # Parse the date and time columns
    df['date'] = pd.to_datetime(df['date'])
    df['time'] = pd.to_datetime(df['time'], format='%H:%M:%S').dt.time
    
    # Extract year, month, day, hour, and minute
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['hour'] = df['time'].apply(lambda x: x.hour)
    df['minutes'] = df['time'].apply(lambda x: x.minute)
    
    # Tạo trường `date_key` với định dạng `YYYY-MM-DD HH:MM`
    df['date_key'] = df.apply(lambda x: f"{x['year']}-{x['month']:02}-{x['day']:02} {x['hour']:02}:{x['minutes']:02}", axis=1)
    
    # Convert to dictionary and initialize aggregation dictionary
    data_dict = df.to_dict(orient='records')
    ndict = {}

    for data in data_dict:
        # Bỏ qua bản ghi nếu có trường nào bị null
        if any(pd.isnull(value) for value in data.values()):
            continue
        
        # Sử dụng `date_key` để nhóm dữ liệu
        id_and_time = data['date_key']
        
        # Aggregate data by `date_key`
        if id_and_time in ndict:
            ndict[id_and_time]['total_ticket'] += 1
            if data.get('popcorn') == "Có":
                ndict[id_and_time]['total_popcorn'] += 1
            ndict[id_and_time]['total_sales'] += data.get('total', 0)
            ndict[id_and_time]['ticketcodes'].append(data['ticketcode'])
        else:
            # Tìm `time_id` trong `time_db` dựa trên `date_key`
            time_dimension = time_db.find_one({'year': data['year'], 
                                               'month': data['month'], 
                                               'day': data['day'], 
                                               'hour': data['hour'], 
                                               'minutes': data['minutes']})
            time_dim_id = time_dimension['time_id'] if time_dimension else None
            
            # Khởi tạo dữ liệu mới trong `ndict`
            ndict[id_and_time] = {
                'time_dim_id': time_dim_id,  # Lưu `time_id` từ `time_db`
                'total_ticket': 1,
                'total_popcorn': 1 if data.get('popcorn') == "có" else 0,
                'total_sales': data.get('total', 0),
                'ticketcodes': [data['ticketcode']]
            }

    # Insert aggregated data into MongoDB
    data_id = 1
    inserted = []

    for record in ndict.values():
        # Set unique ID
        record['id'] = data_id
        data_id += 1
        
        # Insert each record into MongoDB
        try:
            sales_by_time_db.insert_one(record)
            inserted.append(record)
        except Exception as e:
            print(f"Error inserting record {record['id']}: {e}")

    # Print the result
    print(inserted[:5])  # Print the first 5 inserted records for verification
    print("Total records inserted:", len(inserted))
