# %%
import numpy as np
import os
import pandas as pd

from collections import OrderedDict

nan = np.nan

# %%
# 参加者情報
ID = 'id'
ID_FIRST, ID_LAST = 1, 20

# 列名
TRIALNUM, TRIALCODE = 'trialnum', 'trialcode'
CURRENT_SCORE_VALUE = 'values.CurrentScore'
QUESTION_M_VALUE, QUESTION_M2_VALUE = 'values.QuestionM', 'values.QuestionM2'
QUESTION_S_VALUE = 'values.QuestionS'
RESPONSE = 'response'
COLUMNS = [
    TRIALNUM,
    TRIALCODE,
    CURRENT_SCORE_VALUE,
    QUESTION_M_VALUE,
    QUESTION_M2_VALUE,
    QUESTION_S_VALUE,
    RESPONSE,
]

# 条件
CONDITION = 'condition'
PRE = 'pre'
FORWARD, BACKWARD = 'forward', 'backward'
CUSHION, SOFT, HARD = 'cushion', 'soft', 'hard'
CONTROL = 'control'
COLUMN_NAME_TAILS = {
    PRE: '_pre',
    FORWARD: '_forward',
    BACKWARD: '_backward',
    CONTROL: '_control',
    CUSHION: '_cushion'
}
FILE_NAME_TAILS = {
    PRE: '_pre_experiment.csv',
    FORWARD: '_forward.csv',
    BACKWARD: '_backward.csv',
    SOFT: '_cushion_soft.csv',
    HARD: '_cushion_hard.csv'
}
CONDITION_TO_INT = {PRE: 0, CONTROL: 1, SOFT: 2, HARD: 3}

# 多面的感情尺度
DEPRESSION, HOSTILITY = 'depression', 'hostility'
BOREDOM, LIVELINESS = 'boredom', 'liveliness'
WELL_BEING, FRIENDLINESS = 'well_being', 'friendliness'
CONCENTRATION, STARTLE = 'concentration', 'startle'
MOOD_MEASURES = [
    DEPRESSION, HOSTILITY,
    BOREDOM, LIVELINESS,
    WELL_BEING, FRIENDLINESS,
    CONCENTRATION, STARTLE,
]

# 結果への感じ方
FEEL_L10, FEEL_G10 = 'feel_L10', 'feel_G10'
FEEL_L50, FEEL_G50 = 'feel_L50', 'feel_G50'
FEEL_MEASURES = [FEEL_L10, FEEL_G10, FEEL_L50, FEEL_G50]

# 行動データ
RISKY_OVERALL = '50_ratio_overall'
RISKY_NOFIRST = '50_ratio_nofirst'
RISKY_LOSE, RISKY_GAIN = '50_ratio_after_lose', '50_ratio_after_gain'
RISKY_L10, RISKY_G10 = '50_ratio_after_L10', '50_ratio_after_G10'
RISKY_L50, RISKY_G50 = '50_ratio_after_L50', '50_ratio_after_G50'
CASES_LOSE, CASES_GAIN = 'cases_lose', 'cases_gain'
CASES_L10, CASES_G10 = 'cases_L10', 'cases_G10'
CASES_L50, CASES_G50 = 'cases_L50', 'cases_G50'
BEHAVIOR_MEASURES = [
    RISKY_OVERALL, RISKY_NOFIRST,
    RISKY_LOSE, CASES_LOSE,
    RISKY_GAIN, CASES_GAIN,
    RISKY_L10, CASES_L10,
    RISKY_G10, CASES_G10,
    RISKY_L50, CASES_L50,
    RISKY_G50, CASES_G50,
]


# %%
# 多面的感情尺度の結果を返す関数
def calculate_mood_state_result(df):
    score = [0] * 8
    for i, row in df[df[TRIALCODE] == 'QuestionM'].iterrows():
        score[int(row[QUESTION_M2_VALUE][0]) - 1] += int(row[RESPONSE][1])
    return score


# %%
# ディクショナリにキーを追加し，その要素を空のリストとする関数
def add_key(dict, key):
    dict[key] = []


# %%
# for debug only
# 作成中のデータの登録数が正しい数かチェックする
def assert_data_length(data):
    for k, v in data.items():
        # if len(v) == 0:
        #     print(f'empty for {k} !')
        if len(v) and len(v) != 2 * (ID_LAST-ID_FIRST+1):
            print(f'{k} has {len(v)} items !')


# %%
# softかhardか
dirs = set(os.listdir('split_files'))
conditions = [1] * (ID_LAST-ID_FIRST+1)
cushion_conditions = []
for id in range(ID_FIRST, 1+ID_LAST):
    soft_file_name = f'{str(id).zfill(2)}{FILE_NAME_TAILS[SOFT]}'
    if soft_file_name in dirs:
        cushion_conditions.append(2)
    else:
        cushion_conditions.append(3)
conditions += cushion_conditions

# %%
# データ格納庫の初期化
data = OrderedDict()
data[ID] = [i for _ in range(2) for i in range(ID_FIRST, 1+ID_LAST)]
data[CONDITION] = conditions
for b in BEHAVIOR_MEASURES:
    add_key(data, b)
for f in FEEL_MEASURES:
    add_key(data, f)
for m in MOOD_MEASURES:
    add_key(data, m)

# %%
# forward と backward の平均
for id in range(ID_FIRST, 1+ID_LAST):
    id_string = str(id).zfill(2)

    mood_scores = np.zeros(8)
    feel_scores = {FEEL_G10: 0, FEEL_L10: 0, FEEL_G50: 0, FEEL_L50: 0}
    risky_choices = {
        RISKY_OVERALL: 0, RISKY_NOFIRST: 0,
        RISKY_LOSE: 0, CASES_LOSE: 0,
        RISKY_GAIN: 0, CASES_GAIN: 0,
        RISKY_L10: 0, CASES_L10: 0,
        RISKY_G10: 0, CASES_G10: 0,
        RISKY_L50: 0, CASES_L50: 0,
        RISKY_G50: 0, CASES_G50: 0,
    }

    for condition in [FORWARD, BACKWARD]:
        df = pd.read_csv(f'split_files/{id_string}{FILE_NAME_TAILS[condition]}')

        # mood
        mood_scores += np.array(calculate_mood_state_result(df))

        # feel
        for i, row in df[df[TRIALCODE] == 'QuestionS'].iterrows():
            if row[QUESTION_S_VALUE].startswith('５０点が外れたとき'):
                column_name = FEEL_L50
            elif row[QUESTION_S_VALUE].startswith('５０点が当たったとき'):
                column_name = FEEL_G50
            elif row[QUESTION_S_VALUE].startswith('１０点が外れたとき'):
                column_name = FEEL_L10
            else:  # row[QUESTION_S_VALUE].startswith('１０点が当たったとき')
                column_name = FEEL_G10
            response_value = int(row[RESPONSE][-1])
            feel_scores[column_name] += response_value

        # behavior
        last_outcome = ''  # 前回の課題の結果を格納する
        lost_last_time = True  # 前回がGainだったかLoseだったか

        for i, row in df[df[RESPONSE] == '0'].iterrows():
            outcome = row[TRIALCODE][-3:]
            chose_risky = outcome.endswith('50')
            lost_this_time = outcome[0] == 'L'

            risky_choices[RISKY_OVERALL] += chose_risky

            if row[TRIALNUM] != 2:  # not first trial
                risky_choices[RISKY_NOFIRST] += chose_risky
                if lost_last_time:
                    risky_choices[RISKY_LOSE] += chose_risky
                else:
                    risky_choices[RISKY_GAIN] += chose_risky

                if last_outcome == 'L10':
                    risky_choices[RISKY_L10] += chose_risky
                elif last_outcome == 'G10':
                    risky_choices[RISKY_G10] += chose_risky
                elif last_outcome == 'L50':
                    risky_choices[RISKY_L50] += chose_risky
                else:  # last_outcome == 'G50'
                    risky_choices[RISKY_G50] += chose_risky

            if row[TRIALNUM] != 72:  # not last trial
                if lost_this_time:
                    risky_choices[CASES_LOSE] += 1
                else:
                    risky_choices[CASES_GAIN] += 1

                if outcome == 'L10':
                    risky_choices[CASES_L10] += 1
                elif outcome == 'G10':
                    risky_choices[CASES_G10] += 1
                elif outcome == 'L50':
                    risky_choices[CASES_L50] += 1
                else:  # outcome == 'G50'
                    risky_choices[CASES_G50] += 1

            last_outcome = outcome
            lost_last_time = lost_this_time

    # debug
    assert 280 == risky_choices[CASES_G10] + risky_choices[CASES_G50]\
        + risky_choices[CASES_L10] + risky_choices[CASES_L50]
    assert 280 == risky_choices[CASES_LOSE] + risky_choices[CASES_GAIN]

    # mood
    mood_scores /= 2
    for score, mood in zip(mood_scores, MOOD_MEASURES):
        data[mood].append(score)

    # feel
    for key in feel_scores:
        feel_scores[key] /= 2
        data[key].append(feel_scores[key])

    # behavior
    risky_choices[RISKY_OVERALL] /= 288
    risky_choices[RISKY_NOFIRST] /= 280
    risky_choices[RISKY_G10] /= risky_choices[CASES_G10]
    risky_choices[RISKY_L10] /= risky_choices[CASES_L10]
    risky_choices[RISKY_G50] /= risky_choices[CASES_G50]
    risky_choices[RISKY_L50] /= risky_choices[CASES_L50]
    risky_choices[RISKY_LOSE] /= risky_choices[CASES_LOSE]
    risky_choices[RISKY_GAIN] /= risky_choices[CASES_GAIN]

    # register behavior
    for key, value in risky_choices.items():
        data[key].append(value)

# %%
# soft or hard を追加

for id in range(ID_FIRST, 1+ID_LAST):
    # soft? hard?
    if cushion_conditions[id-1] == 2:
        condition = SOFT
    else:
        condition = HARD

    # read
    id_string = str(id).zfill(2)
    df = pd.read_csv(f'split_files/{id_string}{FILE_NAME_TAILS[condition]}')

    # mood
    mood_scores = calculate_mood_state_result(df)
    # register mood
    for score, mood in zip(mood_scores, MOOD_MEASURES):
        data[mood].append(score)

    # feel
    feel_scores = {FEEL_G10: 0, FEEL_L10: 0, FEEL_G50: 0, FEEL_L50: 0}
    for i, row in df[df[TRIALCODE] == 'QuestionS'].iterrows():
        if row[QUESTION_S_VALUE].startswith('５０点が外れたとき'):
            column_name = FEEL_L50
        elif row[QUESTION_S_VALUE].startswith('５０点が当たったとき'):
            column_name = FEEL_G50
        elif row[QUESTION_S_VALUE].startswith('１０点が外れたとき'):
            column_name = FEEL_L10
        else:  # row[QUESTION_S_VALUE].startswith('１０点が当たったとき')
            column_name = FEEL_G10
        response_value = int(row[RESPONSE][-1])
        feel_scores[column_name] += response_value
    # register feel
    for key in feel_scores:
        data[key].append(feel_scores[key])

    # behavior
    risky_choices = {
        RISKY_OVERALL: 0, RISKY_NOFIRST: 0,
        RISKY_LOSE: 0, CASES_LOSE: 0,
        RISKY_GAIN: 0, CASES_GAIN: 0,
        RISKY_L10: 0, CASES_L10: 0,
        RISKY_G10: 0, CASES_G10: 0,
        RISKY_L50: 0, CASES_L50: 0,
        RISKY_G50: 0, CASES_G50: 0,
    }
    last_outcome = ''  # 前回の課題の結果を格納する
    lost_last_time = True  # 前回がGainだったかLoseだったか
    # calculate behavior
    for i, row in df[df[RESPONSE] == '0'].iterrows():
        outcome = row[TRIALCODE][-3:]
        chose_risky = outcome.endswith('50')
        lost_this_time = outcome[0] == 'L'

        risky_choices[RISKY_OVERALL] += chose_risky

        if row[TRIALNUM] != 2:  # not first trial
            risky_choices[RISKY_NOFIRST] += chose_risky
            if lost_last_time:
                risky_choices[RISKY_LOSE] += chose_risky
            else:
                risky_choices[RISKY_GAIN] += chose_risky

            if last_outcome == 'L10':
                risky_choices[RISKY_L10] += chose_risky
            elif last_outcome == 'G10':
                risky_choices[RISKY_G10] += chose_risky
            elif last_outcome == 'L50':
                risky_choices[RISKY_L50] += chose_risky
            else:  # last_outcome == 'G50'
                risky_choices[RISKY_G50] += chose_risky

        if row[TRIALNUM] != 72:  # not last trial
            if lost_this_time:
                risky_choices[CASES_LOSE] += 1
            else:
                risky_choices[CASES_GAIN] += 1

            if outcome == 'L10':
                risky_choices[CASES_L10] += 1
            elif outcome == 'G10':
                risky_choices[CASES_G10] += 1
            elif outcome == 'L50':
                risky_choices[CASES_L50] += 1
            else:  # outcome == 'G50'
                risky_choices[CASES_G50] += 1

        last_outcome = outcome
        lost_last_time = lost_this_time
    # debug
    assert 140 == risky_choices[CASES_G10] + risky_choices[CASES_G50]\
        + risky_choices[CASES_L10] + risky_choices[CASES_L50]
    assert 140 == risky_choices[CASES_LOSE] + risky_choices[CASES_GAIN]
    # calculate into ratio based on cases
    risky_choices[RISKY_OVERALL] /= 144
    risky_choices[RISKY_NOFIRST] /= 140
    risky_choices[RISKY_G10] /= risky_choices[CASES_G10]
    risky_choices[RISKY_L10] /= risky_choices[CASES_L10]
    risky_choices[RISKY_G50] /= risky_choices[CASES_G50]
    risky_choices[RISKY_L50] /= risky_choices[CASES_L50]
    risky_choices[RISKY_LOSE] /= risky_choices[CASES_LOSE]
    risky_choices[RISKY_GAIN] /= risky_choices[CASES_GAIN]
    # register behavior
    for key, value in risky_choices.items():
        data[key].append(value)

assert_data_length(data)

# %%
df_aggregate_nakata = pd.DataFrame(data)\
    .round(4).sort_values(by=[ID, CONDITION])

# %%
df_aggregate_nakata.to_csv('aggregate_nakata.csv', index=None)

# %%
df_aggregate_nakata.columns

# %%
df_aggregate_nakata

# %%
df_aggregate_nakata.sort_values(CONDITION)

# %%
