from platform import release

import pandas as pd
from src.db import db
import src.settings as settings

film_db = db["films"]
transaction_db = db["transaction"]

def c7_rev_by_duration():

    transaction = list(transaction_db.find())

    # Truy vấn transaction
    for item in transaction:
        film = film_db.find_one({'show_id': item['film_id']})
        item['film'] = film

    duration_revenue = {}
    for item in transaction:
        duration = item['film']["duration"]
        if duration in duration_revenue:
            duration_revenue[duration]["quantity"] += 1
            duration_revenue[duration]["total"] += item['total']
        else:
            duration_revenue[duration] = {"quantity": 1, "total": item['total']}


    # Chuẩn bị dữ liệu cho CSV
    rows = []
    for index, data in duration_revenue.items():
        rows.append({
            "Duration": index,
            "Quantity": data["quantity"],
            "Total_Revenue": data["total"]
        })

    # Chuyển đổi sang DataFrame và lưu thành CSV
    df = pd.DataFrame(rows)
    df.to_csv(settings.output_path + 'duration_revenue.csv', index=False)


# Call the function to execute the script
c7_rev_by_duration()