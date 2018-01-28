import seaborn as sns
import pandas as pd
import pickle
import matplotlib.pyplot as plt


# df = pd.read_csv("munich.csv", delimiter=",",
#                  header=None,
#                  names=["rent", "area", "rooms", "address"])
#
# f = open("munich", 'wb')
# pickle.dump(df, f)
# f.close()

f = open("munich", "rb")
df = pickle.load(f)
f.close()

print df.head(5)

# plt.scatter(list(df.area), list(df.rent))
# plt.xlabel("Area [m2]")
# plt.ylabel("Rent [Euro]")
# plt.savefig("areavsrent.png")


plt.hist(list(df.rent), bins=20)
plt.xlabel("Rent [Euro]")
plt.ylabel("Ratio")
plt.savefig("histrent.png")