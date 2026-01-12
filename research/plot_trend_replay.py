import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# =========================
# Konfiguration
# =========================
CSV_PATH = "data/XAUUSD_PERIOD_05.csv"
WINDOW = 100  # Anzahl Kerzen
START_INDEX = 200  # Startpunkt im Chart

# =========================
# Daten laden
# =========================
df = pd.read_csv(
    CSV_PATH,
    sep="\t",
    names=["time", "high", "low", "open", "close"],
    header=0
)

df["close"] = df["close"].astype(float)

index = START_INDEX

# =========================
# Regression
# =========================
def regression_line(y):
    x = np.arange(len(y))
    m, b = np.polyfit(x, y, 1)
    return m, b, m * x + b

# =========================
# High / Low relativ zur Regression
# =========================
def find_extrema_against_regression(closes, reg):
    extrema = []

    def side(i):
        return np.sign(closes[i] - reg[i])

    n = len(closes)
    current_side = side(0)

    max_dist = abs(closes[0] - reg[0])
    max_idx = 0

    for i in range(1, n):
        s = side(i)
        dist = abs(closes[i] - reg[i])

        # gleicher Bereich
        if s == current_side or s == 0:
            if dist > max_dist:
                max_dist = dist
                max_idx = i

        # Seitenwechsel
        else:
            extrema.append((
                max_idx,
                closes[max_idx],
                "high" if current_side > 0 else "low"
            ))

            current_side = s
            max_dist = dist
            max_idx = i

    # letzten Abschnitt speichern
    extrema.append((
        max_idx,
        closes[max_idx],
        "high" if current_side > 0 else "low"
    ))

    return extrema

# =========================
# Plot
# =========================
fig, ax = plt.subplots(figsize=(14, 6))

def redraw():
    ax.clear()

    window = df.iloc[index - WINDOW:index]
    closes = window["close"].values

    x = np.arange(len(closes))
    m, b, reg = regression_line(closes)

    extrema = find_extrema_against_regression(closes, reg)

    # Close Preise
    ax.plot(x, closes, color="black", linewidth=1)

    # Regression
    ax.plot(x, reg, linestyle="--", color="gray", linewidth=1)

    # Highs / Lows
    for i, price, kind in extrema:
        if kind == "high":
            ax.scatter(i, price, color="blue", s=60, zorder=5)
        else:
            ax.scatter(i, price, color="red", s=60, zorder=5)

    ax.set_title(
        f"Index {index} | slope={m:.4f}",
        fontsize=12
    )

    ax.grid(True)
    plt.draw()

# =========================
# Key Events
# =========================
def on_key(event):
    global index
    if event.key == "right":
        index += 1
        redraw()
    elif event.key == "left":
        index -= 1
        redraw()
    elif event.key == "q":
        plt.close()

fig.canvas.mpl_connect("key_press_event", on_key)

redraw()
plt.show()
