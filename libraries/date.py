from datetime import date

def get_date():
    today = date.today()
    # Textual month, day and year	
    date_written = today.strftime("%B %d, %Y")
    return date_written