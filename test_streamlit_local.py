import pandas as pd

url = "https://drive.google.com/uc?id=1Oi5kWc173-Z4ecnySTkbz6hffuYigXri"
df = pd.read_csv(url)
print(df.head())
