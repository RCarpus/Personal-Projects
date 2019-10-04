import pandas as pd
df = pd.read_json('scryfall-oracle-cards.json')
print(df.head(5))
