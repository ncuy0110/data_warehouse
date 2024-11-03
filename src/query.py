from src.query_data.c1_rev_by_agecus import c1_rev_by_agecus
from src.query_data.c2_rev_by_typefilm import c2_rev_by_typefilm
from src.query_data.c3_rev_by_gender import c3_rev_by_gender
from src.query_data.c4_rev_by_job import c4_rev_by_job
from src.query_data.c5_rev_by_film import c5_rev_by_film
from src.query_data.c6_rev_by_release_year import c6_rev_by_release_year
from src.query_data.c7_rev_by_duration import c7_rev_by_duration
from src.query_data.c1_rev_by_hour import c1_rev_by_hour
from src.query_data.c2_rev_by_weekday_hour import c2_rev_by_weekday_hour
from src.query_data.c3_rev_by_ticket_type_weekday import c3_rev_by_ticket_type_weekday
from src.query_data.c4_total_popcorn_sales_by_weekday_hour import c4_total_popcorn_sales_by_weekday_hour
from src.query_data.c5_ticket_sales_by_day import c5_ticket_sales_by_day

if __name__ == "__main__":
    c1_rev_by_agecus()
    c2_rev_by_typefilm()
    c3_rev_by_gender()
    c4_rev_by_job()
    c5_rev_by_film()
    c6_rev_by_release_year()
    c7_rev_by_duration()
    # print("Running c1_rev_by_hour...")
    # c1_rev_by_hour()
    # print("Completed c1_rev_by_hour\n")

    # print("Running c2_rev_by_weekday_hour...")
    # c2_rev_by_weekday_hour()
    # print("Completed c2_rev_by_weekday_hour\n")

    # print("Running c3_rev_by_ticket_type_weekday...")
    # c3_rev_by_ticket_type_weekday()
    # print("Completed c3_rev_by_ticket_type_weekday\n")

    print("Running c4_total_popcorn_sales_by_weekday_hour...")
    c4_total_popcorn_sales_by_weekday_hour()
    print("Completed c4_total_popcorn_sales_by_weekday_hour\n")

    # print("Running c5_ticket_sales_by_day...")
    # c5_ticket_sales_by_day()
    # print("Completed c5_ticket_sales_by_day\n")

    print("All queries have been run successfully.")
