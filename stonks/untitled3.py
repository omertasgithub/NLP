import yfinance as yf
import pandas as pd

test = yf.download('AAPL', start="2020-05-21", end="2020-05-25", interval='1m')
print(test)
test.to_csv("test.csv")

# d = pd.read_csv("data.csv")
# print(d)