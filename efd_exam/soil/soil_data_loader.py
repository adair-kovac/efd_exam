import pandas as pd
from matplotlib import pyplot as plt

def load_data():
    data = pd.read_csv("soil_data.dat", sep="\t", parse_dates=[["%YEAR", "Month", "Day", "Hour (UTC)", "Min"]],
                       keep_date_col=True)
    return data