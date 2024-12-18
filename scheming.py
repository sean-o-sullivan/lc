import pandas as pd

data = pd.read_csv("graphingRegions.csv")
print("Dataset\n")
heads = list(data.head(1))
print(heads)

print(heads[1])
first = data[heads[1]]
print(first)
print("\nSingle Column selected from Dataset")
display(first.head(5))
