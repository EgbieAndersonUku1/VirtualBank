from datetime import datetime


def current_year_choices(number_of_years_to_create=20):
    current_year = datetime().year
    return  [(year, str(year)) for year in range(current_year, current_year + number_of_years_to_create)]