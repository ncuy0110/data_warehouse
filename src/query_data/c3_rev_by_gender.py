import pandas as pd
from src.db import db
import src.settings as settings


customer_db = db["customers"]
transaction_db = db["transaction"]

def c3_rev_by_gender():

    transaction = list(transaction_db.find())

    # Truy vấn transaction
    for item in transaction:
        customer = customer_db.find_one({'customerid': item['customer_id']})
        item['customer'] = customer

    gender_cus_revenue = {}
    for item in transaction:
        gender = item['customer']['gender']
        if gender in gender_cus_revenue:
            gender_cus_revenue[gender]["quantity"] += 1
            gender_cus_revenue[gender]["total_ticket"] += len(item['ticketcodes'])
            gender_cus_revenue[gender]["total_revenue"] += item['total']
        else:
            gender_cus_revenue[gender] = {"quantity": 1, "total_ticket": len(item['ticketcodes']), "total_revenue": item['total']}

    # Chuẩn bị dữ liệu cho CSV
    rows = []
    for index, data in gender_cus_revenue.items():
        rows.append({
            "Gender": index,
            "Quantity": data["quantity"],
            "Total_Ticket": data["total_ticket"],
            "Total_Revenue": data["total_revenue"]
        })

    # Chuyển đổi sang DataFrame và lưu thành CSV
    df = pd.DataFrame(rows)
    df.to_csv(settings.output_path + 'gender_cus_revenue.csv', index=False)


# Call the function to execute the script
c3_rev_by_gender()