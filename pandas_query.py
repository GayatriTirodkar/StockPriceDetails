import pandas as pd

df = pd.read_csv("companies.csv", delimiter = "\t")

"""
First Problem
"""
gb = df.groupby("sector")["market_capital"]
print gb.apply(lambda x:sorted(x, reverse = True)[2:4])

"""
Second Problem
"""
df['bin'] = pd.cut(df['pe_ratio'], range(11,71,5))
print df['bin']
