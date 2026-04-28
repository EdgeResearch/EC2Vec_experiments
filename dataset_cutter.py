import pandas as pd
import os

# === INPUT ===
CSV_FILE = 'consp2vec_dataset/non_conspiracy.csv'
MAX_WORDS = 500000

df = pd.read_csv(CSV_FILE, usecols=['title', 'body', 'subreddit_name'])
df['title'] = df['title'].fillna('')
df['body'] = df['body'].fillna('')

# Rimuovi title duplicati sostituendoli con " "
df['title'] = df['title'].where(~df['title'].duplicated(), ' ')

df['word_count'] = (df['title'].apply(lambda x: len(x.split())) +
                    df['body'].apply(lambda x: len(x.split())))

output_folder = os.path.splitext(os.path.basename(CSV_FILE))[0]
os.makedirs(output_folder, exist_ok=True)

for subreddit, group in df.groupby('subreddit_name'):
    safe_name = str(subreddit).replace('/', '_').replace(' ', '_')
    group = group.reset_index(drop=True)

    current_rows = []
    current_words = 0

    for _, row in group.iterrows():
        if current_words + row['word_count'] > MAX_WORDS:
            break
        current_rows.append(row)
        current_words += row['word_count']

    if current_rows:
        out_path = os.path.join(output_folder, f'{safe_name}.csv')
        pd.DataFrame(current_rows)[['title', 'body']].to_csv(out_path, index=False)
        print(f'Saved: {out_path} ({len(current_rows)} rows, {current_words} words)')

print(f'\nDone.')