import pandas as pd
import matplotlib.pyplot as plt

# Load CSV
df = pd.read_csv("lane_counts.csv")

# Plot lane-wise counts
plt.figure(figsize=(10, 6))
plt.plot(df["Frame"], df["Lane 1"], label="Lane 1", marker='o')
plt.plot(df["Frame"], df["Lane 2"], label="Lane 2", marker='s')
plt.plot(df["Frame"], df["Lane 3"], label="Lane 3", marker='^')

plt.title("Traffic Flow per Lane")
plt.xlabel("Frame Number")
plt.ylabel("Vehicle Count")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("lane_counts_plot.png")
plt.show()