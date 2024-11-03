import pandas as pd
from src.db import db
import src.settings as settings


customer_db = db["customers"]
transaction_db = db["transaction"]

def c4_rev_by_job():

    transaction = list(transaction_db.find())

    # Truy vấn transaction
    for item in transaction:
        customer = customer_db.find_one({'customerid': item['customer_id']})
        item['customer'] = customer

    job_cus_revenue = {}
    for item in transaction:
        job = item['customer']['job']
        if job in job_cus_revenue:
            job_cus_revenue[job]["quantity"] += 1
            job_cus_revenue[job]["total_ticket"] += len(item['ticketcodes'])
            job_cus_revenue[job]["total_revenue"] += item['total']
        else:
            job_cus_revenue[job] = {"quantity": 1, "total_ticket": len(item['ticketcodes']), "total_revenue": item['total']}

    # Chuẩn bị dữ liệu cho CSV
    rows = []
    for index, data in job_cus_revenue.items():
        rows.append({
            "Job": index,
            "Quantity": data["quantity"],
            "Total_Ticket": data["total_ticket"],
            "Total_Revenue": data["total_revenue"]
        })

    # Chuyển đổi sang DataFrame và lưu thành CSV
    df = pd.DataFrame(rows)
    df.to_csv(settings.output_path + 'job_cus_revenue.csv', index=False)


# Call the function to execute the script
c4_rev_by_job()