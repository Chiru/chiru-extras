import csv
import pandas as pd
import numpy as np

locations = pd.read_csv('btid.csv', parse_dates=True)
dataset = pd.read_csv('dataorder.csv', parse_dates=True)

