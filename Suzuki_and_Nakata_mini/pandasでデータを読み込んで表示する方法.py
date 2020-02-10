# %%
import pandas as pd

# %%
# 読み込み
df = pd.read_csv('data/05.dat')

# %%
# 全データ表示
df

# %%
# 先頭5行のみ表示
df.head()

# %%
# どんな列名があるか
df.columns

# %%
# 列1本をみたい
df['trialcode']

# %%
# 行一本を見たい
df.loc[4]

# %%
# ある特定のセルを見たい
df.loc[4, 'trialcode']

# %%
# at の方が実行速度が速いので，1つのセルだけ参照したいときは at を使う方が良い
df.at[4, 'trialcode']

# at のデメリットは，1個のセルしか参照できないこと
# 以降のセルで，loc を用いて複数行・複数列の参照を行っているが，これらは at では出来ない

# %%
# 複数の行の，ある列をみたい
df.loc[2:4, 'trialcode']

# %%
# at でやるとエラー
df.at[2:4, 'trialcode']

# %%
# 複数の行の，複数の列をみたい
df.loc[2:4, 'trialcode':'response']

# %%
# 全ての行の，複数の列をみたい
df.loc[:, ['trialcode', 'response']]

# %%
