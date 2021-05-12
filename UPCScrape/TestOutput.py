import pandas as pd


df = pd.read_csv("IDUPCDict.csv")
df.T
print(df.T)