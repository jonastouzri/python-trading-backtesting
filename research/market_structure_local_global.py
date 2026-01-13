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
df = df.dropna(subset=["close"])
df.reset_index(inplace=True)
df.rename(columns={"index": "candle_index"}, inplace=True)

# --------------------------
# Parameter
# --------------------------
WINDOW = 30
current_step = WINDOW

fig, ax = plt.subplots()
plt.ion()

# --------------------------
# Globale Struktur
# --------------------------
global_points = []  # (idx, price, "high"/"low")

def redraw():
    ax.clear()

    data = df.iloc[current_step - WINDOW : current_step]
    closes = data["close"].values
    x = data["candle_index"].values

    # --------------------------
    # Initialisierung
    # --------------------------
    local_high = closes[0]
    local_low = closes[0]
    local_high_idx = 0
    local_low_idx = 0

    # 🔴 erster Punkt ist GLOBAL HIGH
    if not global_points:
        global_points.append((x[0], closes[0], "high"))

    direction = None  # "up" / "down"

    # --------------------------
    # Durchlauf
    # --------------------------
    for i in range(1, len(closes)):
        price = closes[i]

        # Richtung initialisieren
        if direction is None:
            direction = "up" if price >= closes[i - 1] else "down"

        # -------- Aufwärtsbewegung
        if direction == "up":
            if price > local_high:
                local_high = price
                local_high_idx = i
            elif price < local_high:
                direction = "down"
                local_low = price
                local_low_idx = i

        # -------- Abwärtsbewegung
        elif direction == "down":
            if price < local_low:
                local_low = price
                local_low_idx = i
            elif price > local_low:
                direction = "up"
                local_high = price
                local_high_idx = i

        # --------------------------
        # GLOBAL BREAK DOWN
        # --------------------------
        if price < local_low:
            global_points.append((x[local_high_idx], local_high, "high"))
            global_points.append((x[local_low_idx], local_low, "low"))

            local_high = price
            local_low = price
            local_high_idx = i
            local_low_idx = i
            direction = None

        # --------------------------
        # GLOBAL BREAK UP
        # --------------------------
        if price > local_high:
            global_points.append((x[local_low_idx], local_low, "low"))
            global_points.append((x[local_high_idx], local_high, "high"))

            local_high = price
            local_low = price
            local_high_idx = i
            local_low_idx = i
            direction = None

    # --------------------------
    # Plot
    # --------------------------
    ax.plot(x, closes, color="black", label="Close")

    # Lokale Punkte (transparent)
    ax.scatter(x[local_high_idx], local_high, color="red", alpha=0.4)
    ax.scatter(x[local_low_idx], local_low, color="blue", alpha=0.4)

    # Globale Struktur
    if len(global_points) >= 2:
        gx = [p[0] for p in global_points]
        gy = [p[1] for p in global_points]
        ax.plot(gx, gy, color="orange", linewidth=2, label="Global Structure")

        for idx, price, typ in global_points:
            ax.scatter(
                idx,
                price,
                color="red" if typ == "high" else "blue",
                s=80,
                zorder=5
            )

    ax.set_title(f"Market Structure | Step {current_step}")
    ax.legend()
    plt.draw()

# --------------------------
# Interaktion
# --------------------------
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
