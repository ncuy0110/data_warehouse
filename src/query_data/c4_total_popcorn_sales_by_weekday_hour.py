import pandas as pd
from src.db import db
import src.settings as settings
from datetime import datetime

# Database collections
sales_by_time_db = db["sales_by_time"]
time_db = db["time"]

# Weekday mapping
WEEKDAY_MAP = {0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'}

def c4_total_popcorn_sales_by_weekday_hour():
    # Initialize structures for revenue and popcorn sales by weekday and hour
    sales_data = {
        (weekday, hour): {"Total_Popcorn_Sales": 0, "Revenue": 0}
        for weekday in WEEKDAY_MAP.keys() for hour in range(24)
    }

    # Load data from MongoDB
    sales_by_time = list(sales_by_time_db.find())
    time_data = {time['time_id']: time for time in time_db.find()}

    # Calculate revenue and popcorn sales per weekday and hour
    for sale in sales_by_time:
        time_dimension = time_data.get(sale['time_dim_id'])
        if time_dimension:
            year, month, day, hour = (
                time_dimension.get('year'),
                time_dimension.get('month'),
                time_dimension.get('day'),
                time_dimension.get('hour')
            )

            # Determine weekday and validate hour
            try:
                weekday = datetime(year, month, day).weekday()
                if 0 <= hour <= 23:
                    sales_data[(weekday, hour)]["Total_Popcorn_Sales"] += sale.get('total_popcorn', 0)
                    sales_data[(weekday, hour)]["Revenue"] += sale.get('total_sales', 0)
            except ValueError:
                print(f"Warning: Invalid date {year}-{month}-{day}")

    # Prepare data to save as CSV
    rows = []
    for (weekday, hour), data in sales_data.items():
        rows.append({
            "Weekday": WEEKDAY_MAP[weekday],
            "Hour": hour,
            "Total_Popcorn_Sales": data["Total_Popcorn_Sales"],
            "Revenue": data["Revenue"]
        })

    df = pd.DataFrame(rows)
    df.to_csv(settings.output_path + 'c4_total_popcorn_sales_by_weekday_hour.csv', index=False)

# Run the function
c4_total_popcorn_sales_by_weekday_hour()
