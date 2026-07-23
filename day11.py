# Day 11 - Pandas

import pandas as pd

# PART 1 - Creating DataFrames
# A DataFrame is a table with rows and columns
# exactly like an Excel sheet but inside Python
# every AI dataset you work with will be a DataFrame

print("PART 1 - Creating DataFrames")
data = {
    "name": ["Faiq", "Ali", "Sara", "Ahmed", "Zara"],
    "age": [21, 23, 22, 24, 21],
    "score": [95, 78, 88, 65, 92],
    "city": ["Lahore", "Karachi", "Lahore", "Islamabad", "Karachi"]
}

df = pd.DataFrame(data)

print(df)
print(f"\nShape (rows x columns): {df.shape}")
print(f"Column names: {df.columns.tolist()}")
print(f"\nFirst 3 rows:\n{df.head(3)}")
print(f"\nData types:\n{df.dtypes}")
print(f"\nBasic statistics:\n{df.describe()}")

# PART 2 - Selecting Data
# how to access specific rows and columns
# you will use this every single day
print("\nPART 2 - Selecting Data")

# single column
print(f"All names:\n{df['name']}")

# multiple columns
print(f"\nName and score only:\n{df[['name', 'score']]}")

# by row number
print(f"\nRow 0 (first row):\n{df.iloc[0]}")
print(f"\nRows 1 to 3:\n{df.iloc[1:3]}")

# by condition - filter rows
high_scorers = df[df['score'] >= 88]
print(f"\nStudents who scored 88 or above:\n{high_scorers}")

# multiple conditions
lahore_high = df[(df['city'] == 'Lahore') & (df['score'] >= 88)]
print(f"\nLahore students who scored 88 or above:\n{lahore_high}")

# PART 3 - Cleaning Messy Data
# real world data is always messy
# missing values, wrong formats, inconsistent text
# cleaning data is 80% of real AI engineering work

print("\nPART 3 - Cleaning Messy Data")

messy_data = {
    "name": ["Faiq", "Ali", None, "Ahmed", "Zara"],
    "age": [21, None, 22, 24, 21],
    "score": [95, 78, 88, None, 92],
    "city": ["Lahore", "karachi", "Lahore", "islamabad", "Karachi"]
}

messy_df = pd.DataFrame(messy_data)
print(f"Original messy data:\n{messy_df}")
print(f"\nMissing values per column:\n{messy_df.isnull().sum()}")

# fill missing numbers with column average
messy_df['age'] = messy_df['age'].fillna(messy_df['age'].mean())
messy_df['score'] = messy_df['score'].fillna(messy_df['score'].mean())

# fill missing text with placeholder
messy_df['name'] = messy_df['name'].fillna("Unknown")

# fix inconsistent capitalization in city names
messy_df['city'] = messy_df['city'].str.title()

print(f"\nCleaned data:\n{messy_df}")

# PART 4 - Adding Columns and Sorting
# transform and enrich your data

print("\nPART 4 - Adding Columns and Sorting")

# add a grade column based on score
df['grade'] = df['score'].apply(
    lambda x: 'A' if x >= 90 else 'B' if x >= 80 else 'C' if x >= 70 else 'D'
)
print(f"With grades:\n{df}")

# sort by score highest to lowest
sorted_df = df.sort_values('score', ascending=False)
print(f"\nSorted by score (high to low):\n{sorted_df}")

# PART 5 - Grouping Data
# summarize data by category
# used constantly when analyzing AI datasets

print("\nPART 5 - Grouping Data")

city_stats = df.groupby('city')['score'].agg(['mean', 'max', 'min', 'count'])
print(f"Score stats by city:\n{city_stats}")

grade_count = df.groupby('grade')['name'].count()
print(f"\nHow many students per grade:\n{grade_count}")

# PART 6 - CSV Files
# real AI datasets come as CSV files
# you load them, clean them, feed them to models
print("\nPART 6 - CSV Files")

# save your DataFrame to CSV
df.to_csv("students.csv", index=False)
print("Saved to students.csv")

# load it back
loaded_df = pd.read_csv("students.csv")
print(f"\nLoaded back from CSV:\n{loaded_df}")

# quick summary of loaded data
print(f"\nDataset info:")
print(f"  Rows: {len(loaded_df)}")
print(f"  Columns: {loaded_df.columns.tolist()}")
print(f"  Average score: {loaded_df['score'].mean():.1f}")
print(f"  Top student: {loaded_df.loc[loaded_df['score'].idxmax(), 'name']}")