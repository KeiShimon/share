# %%
import os

# %%
# data ディレクトリ内に移動
os.chdir('data')

# %%
# 消す： Feedback, _raw, _2020..., 緑, 赤
for f in os.listdir():
    if len(f) > 30:
        new_filename = f.replace(f[-28:-4], '')
    else:
        new_filename = f
    new_filename = new_filename.replace('緑', '').replace('赤', '')\
        .replace('Feedback', '').replace('raw', '').replace('_', '')

    os.rename(f, new_filename)

os.listdir()

# %%
