import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

xy = 0.3, 0.3,
width, height = 0.5, 0.2

p = mpatches.Rectangle(xy, width, height, facecolor="orange", edgecolor="red")
plt.gca().add_patch(p)

plt.draw()
plt.show()
