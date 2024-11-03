import pandas as pd
from src.db import db
import src.settings as settings

film_db = db["films"]
transaction_db = db["transaction"]

def c5_rev_by_film():

    transaction = list(transaction_db.find())

    # Truy vấn transaction
    for item in transaction:
        film = film_db.find_one({'show_id': item['film_id']})
        item['film'] = film

    film_revenue = {}
    for item in transaction:
        name = item['film']["title"]
        if name in film_revenue:
            film_revenue[name]["quantity"] += 1
            film_revenue[name]["total"] += item['total']
        else:
            film_revenue[name] = {"quantity": 1, "total": item['total']}


    # Chuẩn bị dữ liệu cho CSV
    rows = []
    for index, data in film_revenue.items():
        rows.append({
            "Title": index,
            "Quantity": data["quantity"],
            "Total_Revenue": data["total"]
        })

    # Chuyển đổi sang DataFrame và lưu thành CSV
    df = pd.DataFrame(rows)
    df = df.sort_values(by="Title")
    df.to_csv(settings.output_path + 'film_revenue.csv', index=False)


# Call the function to execute the script
c5_rev_by_film()