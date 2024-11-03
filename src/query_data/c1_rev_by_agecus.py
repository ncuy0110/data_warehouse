import pandas as pd
from src.db import db
import src.settings as settings
from datetime import datetime, date


customer_db = db["customers"]
transaction_db = db["transaction"]

def c1_rev_by_agecus():

    transaction = list(transaction_db.find())

    # Truy vấn transaction
    for item in transaction:
        customer = customer_db.find_one({'customerid': item['customer_id']})
        item['customer'] = customer

    # Calculate total revenue for each customer
    age_cus_revenue = {}
    for item in transaction:
        dob = datetime.strptime(item['customer']['DOB'], '%d-%m-%Y')

        # Tính toán độ tuổi
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

        # Bỏ qua nếu độ tuổi nhỏ hơn 13
        if age < 13:
            continue

        # Nhóm các giao dịch theo độ tuổi
        if age in age_cus_revenue:
            age_cus_revenue[age]["quantity"] += 1
            age_cus_revenue[age]["total_ticket"] += len(item['ticketcodes'])
            age_cus_revenue[age]["total_revenue"] += item['total']
        else:
            age_cus_revenue[age] = {"quantity": 1, "total_ticket": len(item['ticketcodes']), "total_revenue": item['total']}

    # Chuẩn bị dữ liệu cho CSV
    rows = []
    for age_group, data in age_cus_revenue.items():
        rows.append({
            "Age": age_group,
            "Quantity": data["quantity"],
            "Total_Ticket": data["total_ticket"],
            "Total_Revenue": data["total_revenue"]
        })

    # Chuyển đổi sang DataFrame và lưu thành CSV
    df = pd.DataFrame(rows)
    df = df.sort_values(by="Age")  # Sắp xếp theo cột 'age' theo thứ tự tăng dần
    df.to_csv(settings.output_path + 'age_cus_revenue.csv', index=False)


# Call the function to execute the script
c1_rev_by_agecus()