from query_data.c1_rev_by_agecus import c1_rev_by_agecus
from query_data.c2_rev_by_typefilm import c2_rev_by_typefilm
from query_data.c3_rev_by_gender import c3_rev_by_gender
from query_data.c4_rev_by_job import c4_rev_by_job
from query_data.c5_rev_by_film import c5_rev_by_film
from query_data.c7_rev_by_duration import c7_rev_by_duration
from query_data.c4_total_popcorn_sales_by_weekday_hour import c4_total_popcorn_sales_by_weekday_hour

if __name__ == "__main__":
    c1_rev_by_agecus()
    c2_rev_by_typefilm()
    c3_rev_by_gender()
    c4_rev_by_job()
    c5_rev_by_film()
    c7_rev_by_duration()

    print("Running c4_total_popcorn_sales_by_weekday_hour...")
    c4_total_popcorn_sales_by_weekday_hour()
    print("Completed c4_total_popcorn_sales_by_weekday_hour\n")

    print("All queries have been run successfully.")
