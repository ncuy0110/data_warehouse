from src.import_data import import_customer
from src.import_data import import_film
from src.import_data import import_ticket
from src.import_data import import_time
from src.import_data import import_salebytime
from src.import_data import import_transactions


# Gọi hàm import_customer từ file import_customer.py
if __name__ == "__main__":
    import_customer.import_customer()
    import_film.import_film()
    import_ticket.import_ticket()
    import_time.import_time()
    import_salebytime.import_sales_by_time()
    import_transactions.import_transaction()