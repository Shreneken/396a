import json
import matplotlib.pyplot as plt
import numpy as np

with open(f"./MergedData/stats/genres.json", 'r', encoding="utf-8") as wr:
    data = wr.read()

data = json.loads(data)

lower_genres = []
genres = {"Others": 0}
for k, v in data.items():
    if v <= 30:
        genres["Others"] += v
        lower_genres.append(k)
    else:
        genres[k] = v

data = list(genres.values())
labels = list(genres.keys())
colors = ["purple", "#652CB3", "#f2c4e2", "#b03f76", "#f2c079", "#8179f2", "#f2798d", "#E6E6E6", "#f7d763", "#bbafed", "orchid", "peachpuff"]
length, width = 6, 5
# plt.axis([-50, 100, -50, 100])
fig, ax = plt.subplots(figsize=(8, 6), subplot_kw=dict(aspect="equal"))

wedges, texts = ax.pie(data, colors=colors, wedgeprops=dict(width=0.5))

bbox_props = dict(boxstyle="square,pad=0.1", fc="w", ec="k", lw=0)
kw = dict(arrowprops=dict(arrowstyle="->"),
          bbox=bbox_props, zorder=0, va="center")

for i, p in enumerate(wedges):
    ang = (p.theta2 - p.theta1)/3 + p.theta1
    y = np.sin(np.deg2rad(ang))
    x = np.cos(np.deg2rad(ang))
    horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
    connectionstyle = f"angle,angleA=0,angleB={ang}"
    kw["arrowprops"].update({"connectionstyle": connectionstyle})
    ax.annotate(labels[i], xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
                horizontalalignment=horizontalalignment, **kw)

ax.set_title("Genre Distribution", pad=30)
plt.gcf()
plt.tight_layout()
# plt.show()
fig.savefig(f"./MergedData/stats/figures/genre_distribution__image.png", dpi=500)