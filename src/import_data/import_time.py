import pandas as pd
from src import settings
from src.db import db

time_db = db["time"]

def import_time():
    try:
        if time_db.count_documents({}) != 0:
            time_db.drop()
    except:
        pass
    
    # Create a unique index on year, month, day, hour, and minutes
    time_db.create_index(
        [('year', 1), ('month', 1), ('day', 1), ('hour', 1), ('minutes', 1)],
        unique=True
    )

    # Read the data from the Excel sheet
    df = pd.read_excel(settings.input_path, sheet_name='ticket')

    # Parse the date and time columns
    df['date'] = pd.to_datetime(df['date'])
    df['time'] = pd.to_datetime(df['time'], format='%H:%M:%S').dt.time

    # Extract year, month, day, hour, and minutes from date and time
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['hour'] = df['time'].apply(lambda x: x.hour)
    df['minutes'] = df['time'].apply(lambda x: x.minute)

    # Keep only the required columns
    df = df[['year', 'month', 'day', 'hour', 'minutes']]

    # Convert to dictionary
    data_dict = df.to_dict(orient='records')

    print(data_dict[:5])  # Display the first 5 records for verification
    print("Time: ", len(data_dict))  # Display the total count of records

    # Insert records into the MongoDB collection with a unique time_id
    data_id = 1
    for data in data_dict:
        data["time_id"] = data_id
        try:
            time_db.insert_one(data)
            data_id += 1
        except:
            pass
