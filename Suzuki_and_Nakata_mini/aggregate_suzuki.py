# %%
import pandas as pd

from collections import OrderedDict

# %%
# 参加者情報
ID = 'id'
ID_FIRST, ID_LAST = 1, 43

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
    for _, row in df[df[TRIALCODE] == 'QuestionM'].iterrows():
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
        if len(v) == 0:
            print(f'empty for {k} !')
        if len(v) and len(v) != 1 + ID_LAST - ID_FIRST:
            print(f'{k} has {len(v)} items !')


# %%
# 鈴木さんのデータは，1人1行のデータで出力する
# 出力する列について，ブロックの順序は，左から pre -> forward -> backward
#   pre の中身は，多面的状態尺度のみ
#   forward, backward の中身は，行動データ -> 結果への感じ方 -> 多面的状態尺度

# ディクショナリをデータ保管庫として使う
# キーが列名になるので，キーの登録順序が維持されない普通のディクショナリだと困る
# 順番を記憶できるディクショナリを使う
data = OrderedDict()
data[ID] = [i for i in range(ID_FIRST, 1+ID_LAST)]
for condition in [PRE, FORWARD, BACKWARD]:
    if condition != PRE:
        for b in BEHAVIOR_MEASURES:
            add_key(data, b + COLUMN_NAME_TAILS[condition])
        for f in FEEL_MEASURES:
            add_key(data, f + COLUMN_NAME_TAILS[condition])
    for m in MOOD_MEASURES:
        add_key(data, m + COLUMN_NAME_TAILS[condition])

# pre-experiment
for id in range(ID_FIRST, 1+ID_LAST):
    id_string = str(id).zfill(2)
    df = pd.read_csv('split_files/' + id_string + FILE_NAME_TAILS[PRE])

    mood_scores = calculate_mood_state_result(df)  # type: list
    for mood_measure, score in zip(MOOD_MEASURES, mood_scores):
        data[mood_measure+COLUMN_NAME_TAILS[PRE]].append(score)

# forward, backward
for id in range(ID_FIRST, 1+ID_LAST):
    id_string = str(id).zfill(2)
    for condition in [FORWARD, BACKWARD]:
        df = pd.read_csv(f'split_files/{id_string}{FILE_NAME_TAILS[condition]}')

        # register mood
        mood_scores = calculate_mood_state_result(df)  # type: list
        for mood_measure, score in zip(MOOD_MEASURES, mood_scores):
            data[mood_measure+COLUMN_NAME_TAILS[condition]].append(score)

        # register feel
        for i, row in df[df[TRIALCODE] == 'QuestionS'].iterrows():
            if row[QUESTION_S_VALUE].startswith('５０点が外れたとき'):
                column_name = FEEL_L50
            elif row[QUESTION_S_VALUE].startswith('５０点が当たったとき'):
                column_name = FEEL_G50
            elif row[QUESTION_S_VALUE].startswith('１０点が外れたとき'):
                column_name = FEEL_L10
            else:  # row[QUESTION_S_VALUE].startswith('１０点が当たったとき')
                column_name = FEEL_G10
            column_name += COLUMN_NAME_TAILS[condition]
            response_value = int(row[RESPONSE][-1])
            data[column_name].append(response_value)

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

        for i, row in df[df[RESPONSE] == '0'].iterrows():
            outcome = row[TRIALCODE][-3:]
            chose_risky = outcome.endswith('50')
            lost_this_time = outcome[0] == 'L'

            risky_choices[RISKY_OVERALL] += chose_risky

            if row[TRIALNUM] != 2:  # not first trial
                risky_choices[RISKY_NOFIRST] += chose_risky

                if lost_last_time:
                    risky_choices[CASES_LOSE] += 1
                    risky_choices[RISKY_LOSE] += chose_risky
                else:
                    risky_choices[CASES_GAIN] += 1
                    risky_choices[RISKY_GAIN] += chose_risky

                if last_outcome == 'L10':
                    risky_choices[CASES_L10] += 1
                    risky_choices[RISKY_L10] += chose_risky
                elif last_outcome == 'G10':
                    risky_choices[CASES_G10] += 1
                    risky_choices[RISKY_G10] += chose_risky
                elif last_outcome == 'L50':
                    risky_choices[CASES_L50] += 1
                    risky_choices[RISKY_L50] += chose_risky
                else:  # last_outcome == 'G50'
                    risky_choices[CASES_G50] += 1
                    risky_choices[RISKY_G50] += chose_risky

            last_outcome = outcome
            lost_last_time = lost_this_time

        # debug, check the number of cases
        assert 140 == risky_choices[CASES_G10] + risky_choices[CASES_G50]\
            + risky_choices[CASES_L10] + risky_choices[CASES_L50]
        assert 140 == risky_choices[CASES_LOSE] + risky_choices[CASES_GAIN]
        # calculate ratio
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
            data[key + COLUMN_NAME_TAILS[condition]].append(value)

assert_data_length(data)

# %%
df_aggregated = pd.DataFrame(data).round(4)
df_aggregated.to_csv('data/aggregate_suzuki.csv', index=None)

# %%
data

# %%
len(data)

# %%
data[ID]

# %%
