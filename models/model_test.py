import pandas as pd

# Load training dataset
df = pd.read_csv("data/Website Phishing.csv")
df.columns = df.columns.str.lower()

# Convert -1 to 0 as done in training
df['result'] = df['result'].replace(-1, 0)

# Show feature distribution for legitimate URLs (result == 1)
legit = df[df['result'] == 1]
print(legit.describe())

# Show class balance
print("\nClass Balance:")
print(df['result'].value_counts())
