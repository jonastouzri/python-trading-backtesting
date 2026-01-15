import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --------------------------
# CSV laden
# --------------------------
df = pd.read_csv(
    "data/XAUUSD_PERIOD_05.csv",
    sep="\t",
    dtype={"open": float, "high": float, "low": float, "close": float}
)
df = df.dropna(subset=["open", "high", "low", "close"])
df.reset_index(inplace=True)
df.rename(columns={"index": "candle_index"}, inplace=True)

# --------------------------
# Regression
# --------------------------
def regression_line(y):
    x = np.arange(len(y))
    m, b = np.polyfit(x, y, 1)
    return m, b

# --------------------------
# Extrempunkte pro Segment
# --------------------------
def find_extreme_points(y, m, b):
    """
    Für jedes Segment zwischen zwei Kreuzungen der Regressionslinie
    wird GENAU EIN Punkt markiert:
      oberhalb -> High (max. Distanz)
      unterhalb -> Low  (min. Distanz)
    """
    x = np.arange(len(y))
    line = m * x + b
    dist = y - line

    extremes = []

    segment_start = 0
    current_sign = np.sign(dist[0])

    for i in range(1, len(y)):
        if np.sign(dist[i]) != current_sign and np.sign(dist[i]) != 0:
            # Segment abgeschlossen → Extrempunkt bestimmen
            segment = dist[segment_start:i]

            if current_sign > 0:
                rel_idx = np.argmax(segment)
                typ = "high"
            else:
                rel_idx = np.argmin(segment)
                typ = "low"

            idx = segment_start + rel_idx
            extremes.append((idx, y[idx], typ))

            # Neues Segment
            segment_start = i
            current_sign = np.sign(dist[i])

    # Letztes Segment auswerten
    if segment_start < len(y) - 1:
        segment = dist[segment_start:]
        if current_sign > 0:
            rel_idx = np.argmax(segment)
            typ = "high"
        else:
            rel_idx = np.argmin(segment)
            typ = "low"

        idx = segment_start + rel_idx
        extremes.append((idx, y[idx], typ))

    return extremes

# --------------------------
# Interaktiver Plot
# --------------------------
current_step = 5

fig, ax = plt.subplots()
plt.ion()

def redraw():
    ax.clear()

    closes = df["close"].values[:current_step]
    x = df["candle_index"].values[:current_step]

    if len(closes) < 3:
        return

    m, b = regression_line(closes)
    reg_line = m * np.arange(len(closes)) + b

    # Plot
    ax.plot(x, closes, color="black", label="Close")
    ax.plot(x, reg_line, linestyle="--", color="gray", label="Regression")

    extremes = find_extreme_points(closes, m, b)
    for idx, val, typ in extremes:
        ax.scatter(
            x[idx], val,
            color="blue" if typ == "high" else "red",
            s=60, zorder=5
        )

    ax.set_title(f"Step {current_step}/{len(df)}")
    ax.legend()
    plt.draw()

def on_key(event):
    global current_step
    if event.key == "q":
        plt.close()
    else:
        current_step += 1
        if current_step >= len(df):
            print("End of data")
            plt.close()
        else:
            redraw()

fig.canvas.mpl_connect("key_press_event", on_key)
redraw()
plt.show(block=True)
