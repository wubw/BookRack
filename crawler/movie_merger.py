import pandas as pd

df = pd.read_csv('../data/' + 'will_watch.csv', encoding='utf_8_sig')
print(df)

df1 = pd.read_csv('../data/' + 'have_watched.csv', encoding='utf_8_sig')
df = df.append(df1)

df.to_csv('../data/' + 'movie_merged.csv', encoding='utf_8_sig')
print(df)