import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import ceil

def is_leap_year(year):
    """
    Check if the given year is a leap year.
    """
    if year % 4 == 0:
        if year % 100 == 0:
            if year % 400 == 0:
                return True
            else:
                return False
        else:
            return True
    else:
        return False

# Define the dictionary with the number of days before each month
days_in_month = {
    "gennaio": 31,       # 31 days
    "febbraio": None,    # 28 or 29 days (depending on leap year)
    "marzo": 31,         # 31 days
    "aprile": 30,        # 30 days
    "maggio": 31,        # 31 days
    "giugno": 30,        # 30 days
    "luglio": 31,        # 31 days
    "agosto": 31,        # 31 days
    "settembre": 30,     # 30 days
    "ottobre": 31,       # 31 days
    "novembre": 30,      # 30 days
    "dicembre": 31       # 31 days
}

weekdays = {
    "lunedì": 0,
    "martedì": 1,
    "mercoledì": 2,
    "giovedì": 3,
    "venerdì": 4,
    "sabato": 5,
    "domenica": 6
}

def init_calendar(data):
    #inizializzo calendario
    weekday, day, month, year = data.split(" ")

    if is_leap_year(int(year)):
        days_in_month["febbraio"] = 29
    else:
        days_in_month["febbraio"] = 28

    #hyp.   Lu  Ma  Me  Gi  Ve  Sa  Do
    #   a   x   x   x   x   1   2   3   
    #   b   4   5   6   7   ...
    #   c
    #   d
    #   e
    
    first_monday = (int(day) - int(weekdays[weekday]))%7    

    num_weeks = ceil(days_in_month[month]/7)
    if first_monday != 1:
        num_weeks = num_weeks + 1

    calendar = np.ones((num_weeks, 7))

    if first_monday == 1:
        init_row = 0
    else:
        init_row = 1
    
    day_number = 0

    for week_idx in range(init_row, calendar.shape[0]):   #rows
        for day_idx in range(calendar.shape[1]):    #columns
            day_number = first_monday + day_idx + (week_idx-1)*7

            calendar[week_idx][day_idx] = day_number

            if day_number > days_in_month[month]:
                calendar[week_idx][day_idx] = 0

    if first_monday != 1:
        day_number = first_monday
        for day_idx in range(calendar.shape[1]-1, -1, -1):    #columns
            day_number = day_number - 1

            calendar[0][day_idx] = day_number
            if day_number < 1:
                calendar[0][day_idx] = 0

    print(calendar)
    calendar = np.vstack([np.zeros(7),calendar])

    return calendar

    #a questo punto ho creato il calendario del mese selezionato


def plot_calendars(calendar, idx, date, exams):
    weekday, day, month, year = date[idx].split(" ")

    # Plot the calendar with text
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.axis('tight')
    ax.axis('off')

    # Create table data with text
    table_data = []
    for week_idx in range(calendar.shape[0]):
        row_data = []
        for day_idx in range(calendar.shape[1]):
            day_number = calendar[week_idx, day_idx]
            
            text = ""

            if idx == 0:
                for j in range(0, idx - 1):
                    exam_day = date[j].split(" ")[1]
                    if day_number == int(exam_day):
                        text = text + str(exams.iloc[j]) + "\n"
            else:
                for j in range(idx, len(date)):
                    exam_day = date[j].split(" ")[1]
                    if day_number == int(exam_day):
                        text = text + str(exams.iloc[j]) + "\n"

            # Concatenate day number and text
            cell_text = f"{int(day_number)}\n{text}"

            row_data.append(cell_text)  # Add text directly
        table_data.append(row_data)

    # Plot the table with text
    table = ax.table(cellText=table_data, loc='center', cellLoc='center')

    # Add column names
    column_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    for j, name in enumerate(column_names):
        table[(0, j)].visible_edges = 'open'  # Ensure top edges are visible
        table[(0, j)].set_text_props(fontweight='bold', color='blue')  # Bold and color the text
        table[(0, j)].get_text().set_text(name)  # Set the text

    # Adjust cell dimensions
    table.auto_set_font_size(False)
    table.set_fontsize(11)  # Set font size
    table.scale(1, 3)  # Adjust cell height

    plt.title(f'Exam Calendar - {month} {year}')
    plt.show()



def create_exam_calendar(exam_data):
    df = pd.read_csv(csv_path, sep='\t', index_col=0)

    date = df[df.columns[4]]
    exams = df[df.columns[1]]

    calendars = []
    new_calendar_exam_idx = 0

    calendars.append(init_calendar(date[0]))
    weekday0, day0, month0, year0 = date[0].split(" ")


    for i in range(len(date)):
        weekday, day, month, year = date[i].split(" ")
        if month != month0:
            #devo creare un nuovo calendario
            new_calendar_exam_idx = i   #hyp. max 2 calendars per session of exams
            month0 = month
            calendars.append(init_calendar(date[i]))

    if new_calendar_exam_idx != 0:
        #significa che ho almeno 2 calendari
        plot_calendars(calendars[0], 0, date, exams)
        plot_calendars(calendars[1], new_calendar_exam_idx, date, exams)
        
        


if __name__ == "__main__":
    csv_path = "/home/edo/Desktop/Appello2_Inverno2024_STUDENTI3_filtered.csv"
    create_exam_calendar(csv_path)