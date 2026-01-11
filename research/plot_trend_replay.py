import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# =========================
# Config
# =========================
CSV_PATH = "data/XAUUSD_PERIOD_05.csv"
WINDOW = 30  # N Kerzen Rückblick

# =========================
# Load data
# =========================
df = pd.read_csv(CSV_PATH, sep="\t")
df.reset_index(drop=True, inplace=True)
print(df.columns)
# Kerze 1 = letzte geschlossene Kerze
current_idx = WINDOW + 1

# =========================
# Trendline (simple linear regression on close)
# =========================
def compute_trendline(closes):
    x = np.arange(len(closes))
    y = np.array(closes)

    if len(x) < 2:
        return None

    slope, intercept = np.polyfit(x, y, 1)
    trend = slope * x + intercept
    return trend, slope


# =========================
# Plot
# =========================
fig, ax = plt.subplots(figsize=(12, 6))

def redraw():
    ax.clear()

    start = current_idx - WINDOW
    end = current_idx

    window = df.iloc[start:end]

    closes = window["close"].values
    x = np.arange(len(window))

    # --- Price ---
    ax.plot(x, closes, label="Close", color="black")

    # --- Trendline ---
    result = compute_trendline(closes)
    if result:
        trend, slope = result
        ax.plot(x, trend, linestyle="--", label=f"Trend (slope={slope:.4f})")

    ax.set_title(
        f"Trend Replay | Candle index = {current_idx} | "
        f"Time = {df.iloc[current_idx]['time']}"
    )
    ax.legend()
    ax.grid(True)

    fig.canvas.draw_idle()


# =========================
# Keyboard handler
# =========================
def on_key(event):
    global current_idx

    if event.key in ["n", "right"]:
        if current_idx < len(df) - 1:
            current_idx += 1
            redraw()

    elif event.key in ["b", "left"]:
        if current_idx > WINDOW + 1:
            current_idx -= 1
            redraw()

    elif event.key == "q":
        plt.close(fig)


# =========================
# Init
# =========================
fig.canvas.mpl_connect("key_press_event", on_key)
redraw()
plt.show()
