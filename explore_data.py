import pandas as pd

df = pd.read_csv("data/miami_mls_listings.csv")

print("=" * 50)
print("SHAPE")
print(df.shape)

print("\n" + "=" * 50)
print("COLUMNS")
print(df.columns.tolist())

print("\n" + "=" * 50)
print("FIRST 3 ROWS")
print(df.head(3))

print("\n" + "=" * 50)
print("MISSING VALUES")
print(df.isnull().sum())

print("\nNEIGHBORHOODS")
print(df["neighborhood"].value_counts())

print("\nPROPERTY TYPES")
print(df["property_type"].value_counts())

print("\nPRICE STATS")
print(df["price"].describe())

print("\nBEDROOMS")
print(df["bedrooms"].value_counts())

print("\nSAMPLE FEATURES")
print(df["features"].head(10))