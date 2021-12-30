from datetime import datetime


def convert_from_DDMMYYYY_date_string_to_DDMMYYYYhhmm_datetime(date_string):
    return datetime.strptime(date_string, "%d/%m/%Y").strftime("%d/%m/%Y %H:%M:%S")


if __name__ == "__main__":
    print(convert_from_DDMMYYYY_date_string_to_DDMMYYYYhhmm_datetime("01/01/2019"))
