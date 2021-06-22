import yfinance as yf
import pandas as pd

test = yf.download('AAPL', start="2021-05-22", end="2021-06-20", interval='1m')
print(test)
test.to_csv("test.csv")

# d = pd.read_csv("data.csv")
# print(d)