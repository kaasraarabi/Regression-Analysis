import pandas as pd



chunk_size = 100000
chunks = pd.read_csv('Data\\DID-ALL.csv', chunksize=chunk_size)
df2 = pd.read_csv('Data\\cleaned_file.csv')


all_merged = []

for chunk in chunks:
    chunk['Code-mehvar'] = chunk['DID'].astype(str).str[:6].astype(int)
    chunk['Date'] = chunk['DID'].astype(str).str[6:].astype(int)


    chunk = chunk[chunk['Date'] >= 13980101]
    if chunk.empty:
        continue

    chunk['Date'] = chunk['Date'].astype(str)


    df_merged = chunk.merge(df2[['Code-mehvar', 'origin', 'destination']],
                           on='Code-mehvar', how='left')
    df_merged['origin'] = df_merged['origin'].fillna('Unknown_city')
    df_merged['destination'] = df_merged['destination'].fillna('Unknown_city')

    all_merged.append(df_merged)


if all_merged:
    merged_data = pd.concat(all_merged, ignore_index=True)




    entries = merged_data.groupby(['Date', 'destination'])['ALL'].sum().reset_index()
    exits = merged_data.groupby(['Date', 'origin'])['ALL'].sum().reset_index()

    entries = entries.rename(columns={'destination': 'City', 'ALL': 'Total_Entries'})
    exits = exits.rename(columns={'origin': 'City', 'ALL': 'Total_Exits'})


    final_result = pd.merge(entries, exits, on=['Date', 'City'], how='outer').fillna(0)




    print(f"تعداد کل رکوردها در final_result: {len(final_result)}")


    final_result.to_csv('daily_entries_exits.csv', index=False, encoding='utf-8-sig')
else:
    print("error")