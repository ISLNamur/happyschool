from django.utils import timezone


def get_scolar_year():
    current_date = timezone.now()
    year = current_date.year
    month = current_date.month
    day = current_date.day

    if month < 8:
        return year - 1
    elif month == 8 and day < 20:
        return year - 1
    else:
        return year


def in_scolar_year(date):
    current_year = get_scolar_year()
    if date.year < current_year:
        return False

    if date.month >= 9 and date.year == current_year:
        return True

    if date.month < 9 and date.year == current_year + 1:
        return True

    return False