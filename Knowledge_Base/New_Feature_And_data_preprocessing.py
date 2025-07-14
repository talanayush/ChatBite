import pandas as pd
import re

# Load the CSV file
df = pd.read_csv('Nugget_final_dataset.csv')

df['category'] = df['category'].replace('YuMum', 'Main Course')

df['description'].fillna("The Restaurant didn't have enough knowledge about this item", inplace=True)


# creating a new feature with the column name dish type
def extract_price(price_str):
    if pd.isnull(price_str):
        return None
    match = re.search(r'\d+', str(price_str).replace(',', ''))
    return int(match.group()) if match else None

df['numeric_price'] = df['price'].apply(extract_price)

def classify_dish_type(price):
    if price is None:
        return 'unknown'
    if price < 220:
        return 'cheap'
    elif 220 <= price <= 270:
        return 'moderate'
    else:
        return 'expensive'

df['dish type'] = df['numeric_price'].apply(classify_dish_type)


def row_to_tag(row):
    return ' | '.join([str(x) for x in row])

df['tag'] = df.apply(row_to_tag, axis=1)

df = df.drop(columns=['numeric_price'])

df.to_csv('Nugget_New_feature_dataset.csv', index=False)