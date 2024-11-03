import pandas as pd
from src import settings
from src.db import db

ticket_db = db["tickets"]

def import_ticket():
    try:
        if ticket_db.count_documents({}) != 0:
            ticket_db.drop()
    except:
        pass

    df = pd.read_excel(settings.input_path, sheet_name='ticket')

    # Extract unique tickets
    # Adjust the DataFrame to select specific columns and drop duplicate rows
    tickets = df[['ticketcode', 'ticket price', 'slot', 'room', 'slot type', 'ticket type', 'popcorn']].drop_duplicates()



    # Convert to dictionary
    tickets_dict = tickets.to_dict(orient='records')

    print(tickets_dict[:5])
    print(len(tickets_dict))

    for ticket in tickets_dict:
        try:
            ticket_db.insert_one(ticket)
        except:
            pass