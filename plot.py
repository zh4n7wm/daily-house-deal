import pathlib
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv(pathlib.Path('~/Downloads/daily-house-deal.csv'), parse_dates=True, index_col='date')

def plot(house_type='新盘'):
    fig, ax = plt.subplots()
    for district in df.district.unique():
        number = df.loc[(df.district == district) & (df.house_type == house_type), 'number']
        # number = df.query(f'district == "{district}" & house_type == "{house_type}"')['number']
        number = number.resample('m').sum()
        number.plot(ax=ax)
    ax.legend(df.district.unique())
    ax.set_title(house_type)
    plt.show()

plot(house_type='新盘')
plot(house_type='二手房')
