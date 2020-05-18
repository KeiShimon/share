# %%
import pandas as pd

# %%
# 出力したい列名の入ったリストを定義
columns_to_export = [
    'trialnum',
    'trialcode',
    'values.CurrentScore',
    'values.QuestionM',
    'values.QuestionM2',
    'values.QuestionS',
    'response',
]

# %%
last_id = 43
data_source_dir = 'data'
data_export_dir = 'split_files'

for id in range(1, last_id+1):
    id_string = str(id).zfill(2)
    # 数値から文字列に変換した上で，文字列メソッド zfill を用いて0埋め

    df = pd.read_csv(f'{data_source_dir}/{str(id).zfill(2)}.dat')
    # f 文字列を用いることで，文字列の中に変数などの値を埋め込むことができる

    # pre_experiment.csv を出力する
    df.loc[1:40, columns_to_export]\
        .to_csv(f'{data_export_dir}/{id_string}_pre_experiment.csv', index=None)

    # forward.csv と backward.csv を出力する
    # df[df['trialcode'] != 'Rest'] とすることで，'tiralcode'の中身が'Rest'でないものだけを抽出できる
    # DataFrameを参照するかどうかを，True/Falseで決める方法を用いている
    if df.loc[0, 'group'][0] == 'F':
        df.loc[47:238, columns_to_export][df['trialcode'] != 'Rest']\
            .to_csv(f'{data_export_dir}/{id_string}_forward.csv', index=None)
        df.loc[240:431, columns_to_export][df['trialcode'] != 'Rest']\
            .to_csv(f'{data_export_dir}/{id_string}_backward.csv', index=None)
    else:
        df.loc[240:431, columns_to_export][df['trialcode'] != 'Rest']\
            .to_csv(f'{data_export_dir}/{id_string}_forward.csv', index=None)
        df.loc[47:238, columns_to_export][df['trialcode'] != 'Rest']\
            .to_csv(f'{data_export_dir}/{id_string}_backward.csv', index=None)

    # cushion.csv を出力する
    cushion = 'soft' if df.at[0, 'group'][2] == 'S' else 'hard'
    df.loc[433:624, columns_to_export][df['trialcode'] != 'Rest']\
        .to_csv(f'{data_export_dir}/{id_string}_cushion_{cushion}.csv', index=None)

# %%
