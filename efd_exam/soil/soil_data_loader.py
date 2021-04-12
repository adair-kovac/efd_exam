import pandas as pd

def load_data():
    data = pd.read_csv("soil_data.dat", sep="\t", parse_dates={"date": ["%YEAR", "Month", "Day", "Hour (UTC)", "Min"]},
                       keep_date_col=True)

    for i, row in data.iterrows():
        data.at[i, "seconds_since"] = get_time(int(row["Day"]), int(row["Hour (UTC)"]), int(row["Min"]))
    return data


def get_time(day, hour, min):
    initial_day = 17
    initial_hour = 0
    initial_min = 5
    return one_day() * (day - initial_day) + one_hour() * (hour - initial_hour) + one_min() * (min - initial_min)


def one_day():
    return 24*60*60


def one_hour():
    return 60*60


def one_min():
    return 60
