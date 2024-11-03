import pandas as pd
from src.db import db
import src.settings as settings


film_db = db["films"]
transaction_db = db["transaction"]

def c2_rev_by_typefilm():

    transaction = list(transaction_db.find())

    # Truy vấn transaction
    for item in transaction:
        film = film_db.find_one({'show_id': item['film_id']})
        item['film'] = film

    type_film_revenue = {}
    for item in transaction:
        genres = item["film"]["listed_in"].split(", ")
        for genre in genres:
            if genre in type_film_revenue:
                type_film_revenue[genre]["quantity"] += 1
                type_film_revenue[genre]["total_revenue"] += item['total']
            else:
                type_film_revenue[genre] = {"quantity": 1, "total_revenue": item['total']}

    # Chuẩn bị dữ liệu cho CSV
    rows = []
    for index, data in type_film_revenue.items():
        rows.append({
            "Type_Film": index,
            "Quantity": data["quantity"],
            "Total_Revenue": data["total_revenue"]
        })

    # Chuyển đổi sang DataFrame và lưu thành CSV
    df = pd.DataFrame(rows)
    df = df.sort_values(by="Type_Film")  # Sắp xếp theo cột 'age' theo thứ tự tăng dần
    df.to_csv(settings.output_path + 'type_film_revenue.csv', index=False)


# Call the function to execute the script
c2_rev_by_typefilm()