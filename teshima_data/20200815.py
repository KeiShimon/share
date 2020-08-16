# %% [markdown]

## 個人ファイル

- RT を列挙する
- RTの平均を求める

## 全員ファイル

- RTの平均を列挙する
- count correctness

# %%
import pandas as pd
from collections import defaultdict

# %%
REACTION_TIME_THRESHOLD = 2000

MATCH = 'Match'
MISMATCH = 'Mismatch'
DESCRIPTION = 'Description'
POSITION = 'Position'

# %%
REACTION_TIME_MATCH = 'reaction_time_match'
REACTION_TIME_MISMATCH = 'reaction_time_mismatch'

# %%

SAMPLE_FILE_NAME = 'pre01_Markers_RT.csv'

# %%
df_counter_balance = None

# %%
CORRECT_RESPONSE_COUNT_MATCH = 'correct_response_count_match'
CORRECT_RESPONSE_COUNT_MISMATCH = 'correct_response_count_mismatch'

# data storage for counting correct responses
correct_responses_counter = {
    CORRECT_RESPONSE_COUNT_MATCH: [],
    CORRECT_RESPONSE_COUNT_MISMATCH: [],
}

for _, subject in df_counter_balance.iterrows():
    # unpack counterbalance data
    id = subject['Id']
    correct_response_match = subject[MATCH]
    correct_response_mismatch = subject[MISMATCH]

    # file name
    input_file = ''
    output_file = ''

    # read file
    try:
        df = pd.read_csv(input_file)
    except:
        break

    # data storage
    individual_data = {
        REACTION_TIME_MATCH: [],
        REACTION_TIME_MISMATCH: [],
    }
    for key, value in correct_responses_counter.items():
        value.append(0)

    # itereate over rows
    for i, row in df.iterrows():

        # is the row 'comment' ?
        if row['Type'] != 'Comment':
            continue

        # is it a response first place?
        try:
            if df.at[i + 1, 'Type'] != 'Threshold':
                continue
        except:
            break  # outcome will be same as using continue

        # is it a correct response?
        if row[DESCRIPTION] == MATCH and df.at[i + 1, DESCRIPTION] != \
                correct_response_match:
            continue
        if row[DESCRIPTION] == MISMATCH and df.at[i + 1, DESCRIPTION] != \
                correct_response_mismatch:
            continue

        # was the response made within the time-limit ?
        reaction_time = 2 * df.at[i + 1, POSITION] - row[POSITION]
        if reaction_time >= REACTION_TIME_THRESHOLD:
            continue

        if row[DESCRIPTION] == MATCH:
            individual_data[REACTION_TIME_MATCH].append(reaction_time)
            correct_responses_counter[CORRECT_RESPONSE_COUNT_MATCH] += 1
        else:
            individual_data[REACTION_TIME_MISMATCH].append(reaction_time)
            correct_responses_counter[CORRECT_RESPONSE_COUNT_MISMATCH] += 1

    # output individual data
    pd.DataFrame(individual_data).to_csv(output_file, index=None)

# output aggregated data
pd.DataFrame(correct_responses_counter).to_csv('hogehoge.csv')


# %%
# 既存のDataFrame に、新しい列を足す

# df['新しい列名'] = [リスト様のデータ]

# ただし、この方法だと、一番右列に列が追記される
# それが嫌なら、df.insert() を使う方法がある
# しかし、insert はメモリ移動のコストが非常に大きいため、
# insert をそもそも使わなくて済むようにプログラムを組むのが望ましい
