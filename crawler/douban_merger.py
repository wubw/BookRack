import pandas as pd

df = pd.read_csv('../data/' + 'reading.csv', encoding='utf_8_sig')
print(df)

df1 = pd.read_csv('../data/' + 'have_read.csv', encoding='utf_8_sig')
df = df.append(df1)

df2 = pd.read_csv('../data/' + 'will_read.csv', encoding='utf_8_sig')
df = df.append(df2)

df.to_csv('../data/' + 'merged.csv', encoding='utf_8_sig')
print(df)