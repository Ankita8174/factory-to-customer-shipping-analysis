import os
import pandas as pd

# orders.csv ka path
base_path = os.path.dirname(os.path.dirname(__file__))
file_path = os.path.join(base_path, "orders.csv")

df = pd.read_csv(file_path)

print(df.head())
print("Total Records:", len(df))
# Delivery Time calculate karo
df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"] = pd.to_datetime(df["Ship Date"])

df["Delivery Days"] = (df["Ship Date"] - df["Order Date"]).dt.days

print("\nAverage Delivery Days:", df["Delivery Days"].mean())