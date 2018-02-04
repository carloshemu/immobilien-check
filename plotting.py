import seaborn as sns
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from mpl_toolkits.basemap import Basemap


import sys

reload(sys)
sys.setdefaultencoding('utf8')


# df = pd.read_csv("munich.csv", delimiter=",",
#                  header=None,
#                  names=["rent", "area", "rooms", "address"])
#
# f = open("munich", 'wb')
# pickle.dump(df, f)
# f.close()

# f = open("munich", "rb")
# df = pickle.load(f)
# f.close()

# print df.head(5)

def plot_scatter():
    plt.scatter(list(df.area), list(df.rent))
    plt.xlabel("Area [m2]")
    plt.ylabel("Rent [Euro]")
    plt.savefig("areavsrent.png")


def plot_hist():
    plt.hist(list(df.rent), bins=20)
    plt.xlabel("Rent [Euro]")
    plt.ylabel("Ratio")
    plt.savefig("histrent.png")


def plot_region_box(df):

    df['rent/m2'] = df['rent'] / df['area']
    g = sns.factorplot(x='region', y='rent/m2', data=df, kind="box", size=6, aspect=1.5)
    g.set_xticklabels(rotation=90)
    # plt.show()
    plt.tight_layout()
    plt.savefig("region.png")


def plot_region_map(df):

    fig = plt.figure(figsize=(18, 12))

    m = Basemap(llcrnrlat=47.95,
                llcrnrlon=11.40,
                urcrnrlat=48.3,
                urcrnrlon=11.8)
    # m = Basemap(llcrnrlat=48.15,
    #             llcrnrlon=11.70,
    #             urcrnrlat=48.3,
    #             urcrnrlon=11.8)
    m.arcgisimage(dpi=300, xpixels=3000)

    df["rent/m2"] = df["rent"] / df["area"]

    gp = df.groupby(by="region")
    region = list(gp.mean().index)
    lat = list(gp.min()['lat'])
    lon = list(gp.min()['lon'])
    rentm2 = list(gp.mean()['rent/m2'])

    new_df = pd.DataFrame({"region" : region,
                           "lat": lat,
                           "lon": lon,
                           "rent/m2": rentm2})

    for index, row in new_df.iterrows():
        circle = patches.Circle((row['lon'], row['lat']), row['rent/m2']/3000, facecolor='red', linewidth=1)
        plt.gca().add_patch(circle)
        plt.gca().text(row['lon'], row['lat'], "%.2f" % row['rent/m2'], fontsize=15, color='white')

    plt.tight_layout()
    plt.savefig("region_map.png")


    print df["lat"].min(), df["lat"].max()
    print df["lon"].min(), df["lon"].max()


if __name__ == "__main__":
    df = pd.read_csv("munich_extended.csv", delimiter=",",
                     header=None,
                     names=["rent", "area", "rooms", "address",
                            "region", "lat", "lon", "rent/m2"])

    plot_region_map(df)