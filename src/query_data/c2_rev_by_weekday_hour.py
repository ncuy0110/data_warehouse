import pandas as pd
from src.db import db
import src.settings as settings
from datetime import datetime

sales_by_time_db = db["sales_by_time"]
time_db = db["time"]

# Từ điển để ánh xạ ngày trong tuần thành tên ngày
WEEKDAY_MAP = {0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'}

# Từ điển để ánh xạ khung giờ
TIME_PERIODS = {
    "Morning": range(0, 12),  # Sáng từ 0 - 11 giờ
    "Afternoon": range(12, 18),  # Chiều từ 12 - 17 giờ
    "Evening": range(18, 24)  # Tối từ 18 - 23 giờ
}


def get_time_period(hour):
    """Xác định khung giờ dựa vào giá trị hour."""
    for period, hours in TIME_PERIODS.items():
        if hour in hours:
            return period
    return None


def c2_rev_by_weekday_hour():
    # Khởi tạo cấu trúc lưu doanh thu theo ngày trong tuần và khung giờ
    revenue_by_weekday_period = {day: {period: 0 for period in TIME_PERIODS.keys()} for day in WEEKDAY_MAP.keys()}

    # Tải dữ liệu một lần
    sales_by_time = list(sales_by_time_db.find())
    time_data = {time['time_id']: time for time in time_db.find()}

    # Tính toán doanh thu theo ngày trong tuần và khung giờ
    for sale in sales_by_time:
        time_dimension = time_data.get(sale['time_dim_id'])

        if time_dimension:
            year, month, day, hour = time_dimension.get('year'), time_dimension.get('month'), time_dimension.get(
                'day'), time_dimension.get('hour')
            if None not in (year, month, day, hour):
                try:
                    weekday = datetime(year, month, day).weekday()
                    time_period = get_time_period(hour)
                    if time_period:
                        revenue_by_weekday_period[weekday][time_period] += sale['total_sales']
                except ValueError:
                    print(f"Warning: Invalid date {year}-{month}-{day}")

    # Chuẩn bị dữ liệu và lưu thành CSV
    rows = []
    for weekday, periods in revenue_by_weekday_period.items():
        for period, revenue in periods.items():
            rows.append({
                "Weekday": WEEKDAY_MAP[weekday],
                "Time_Period": period,
                "Revenue": revenue
            })

    df = pd.DataFrame(rows)
    df.to_csv(settings.output_path + 'c2_rev_by_weekday_hour.csv', index=False)
