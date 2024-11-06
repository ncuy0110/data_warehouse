from import_data import import_customer
from import_data import import_film
from import_data import import_ticket
from import_data import import_time
from import_data import import_salebytime
from import_data import import_transactions


# Gọi hàm import_customer từ file import_customer.py
if __name__ == "__main__":
    import_customer.import_customer()
    import_film.import_film()
    import_ticket.import_ticket()
    import_time.import_time()
    import_salebytime.import_sales_by_time()
    import_transactions.import_transaction()