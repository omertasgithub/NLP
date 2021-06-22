import yfinance as yf
import pandas as pd

data = yf.download('AAPL', start="2021-05-22", end="2021-06-20", interval='2m')
print(data)
data.to_csv("data.csv")

# d = pd.read_csv("data.csv")
# print(d)