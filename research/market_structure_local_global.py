import pandas as pd
import matplotlib.pyplot as plt

# --------------------------
# CSV laden
# --------------------------
df = pd.read_csv(
    "data/XAUUSD_PERIOD_05.csv",
    sep="\t",
    dtype={"close": float}
)
df = df.dropna(subset=["close"])
df.reset_index(inplace=True)
df.rename(columns={"index": "candle_index"}, inplace=True)

# --------------------------
# Parameter
# --------------------------
WINDOW = 3500          # Start-Offset
VISIBLE = 50         # Sliding window Anzahl Kerzen
TREND_LENGTH = 200    # Länge der Trendlinie
MIN_DISTANCE = 5     # Minimaler Abstand MIN1 -> MIN2
current_step = WINDOW

breakout_points = []

fig, ax = plt.subplots()
plt.ion()

# --------------------------
# Variablen für Phasen
# --------------------------
MAX1 = None
MIN1 = None
MAX2 = None
MIN2 = None
phase = 1  # 1=MAX1/MIN1, 2=MAX2/MIN2, 3=Trend bestätigt

def redraw():
    global MAX1, MIN1, MAX2, MIN2, phase

    ax.clear()
    data = df.iloc[:current_step]
    closes = data["close"].values
    x = data["candle_index"].values

    # Sliding Window
    if len(x) > VISIBLE:
        x = x[-VISIBLE:]
        closes = closes[-VISIBLE:]

    ax.plot(x, closes, color="black", label="Close")

    if current_step <= WINDOW:
        ax.set_title(f"Warmup ({current_step}/{WINDOW})")
        plt.draw()
        return

    price = df["close"].iloc[current_step-1]

    # --------------------------
    # Phase 1: MAX1 / MIN1
    # --------------------------
    if phase == 1:
        if MAX1 is None:
            MAX1 = {"idx": current_step-1, "price": price}
        else:
            if price > MAX1["price"]:
                MAX1 = {"idx": current_step-1, "price": price}
            elif price < MAX1["price"]:
                MIN1 = {"idx": current_step-1, "price": price}
            elif MIN1 and price > MIN1["price"] and price > MAX1["price"]:
                MIN1 = None
                MAX1 = {"idx": current_step-1, "price": price}
        if MIN1 is not None:
            phase = 2  # Wechsel zu Phase2

    # --------------------------
    # Phase 2: MAX2 / MIN2 (relativ zu MIN1 / MAX2)
    # --------------------------
    elif phase == 2:
        # MAX2 aufbauen/aktualisieren
        if price > MIN1["price"]:
            if MAX2 is None:
                MAX2 = {"idx": current_step-1, "price": price}
            elif price >= MAX2["price"]:
                MAX2 = {"idx": current_step-1, "price": price}
                MIN2 = None  # MIN2 löschen, sobald MAX2 steigt

        # MIN2 aufbauen/aktualisieren nur nach MAX2
        if MAX2 is not None and (current_step-1) > MAX2["idx"] and price < MAX2["price"]:
            if MIN2 is None:
                MIN2 = {"idx": current_step-1, "price": price}
            elif price < MIN2["price"]:
                MIN2 = {"idx": current_step-1, "price": price}

        # Preis unter MIN1 → MIN1 aktualisieren (falls MAX2 noch nicht existiert)
        if price < MIN1["price"] and MAX2 is None:
            MIN1 = {"idx": current_step-1, "price": price}

        # **Reset auf Phase1**, falls MAX2 > MAX1
        if MAX2 and MAX2["price"] > MAX1["price"]:
            MAX1 = MAX2
            MIN1 = None
            MAX2 = None
            MIN2 = None
            phase = 1

        # Trendbestätigung prüfen
        if MAX1 and MAX2 and MIN1 and MIN2:
            if MAX1["price"] > MAX2["price"] > MIN1["price"] > MIN2["price"]:
                if MIN2["idx"] - MIN1["idx"] >= MIN_DISTANCE:
                    phase = 3  # Trend bestätigt
                else:
                    # Reset: Abstand zu klein
                    MIN1 = MIN2
                    MAX2 = None
                    MIN2 = None
                    # Phase2 läuft weiter, MAX2 wird beim nächsten Preis > MIN1 neu aufgebaut

    # --------------------------
    # Phase 3: Trendlinie bestätigen
    # --------------------------
    if phase == 3:
        x1, y1 = MAX1["idx"], MAX1["price"]
        x2, y2 = MAX2["idx"], MAX2["price"]
        trend_m = (y2 - y1) / (x2 - x1)
        trend_b = y1 - trend_m * x1

        # Trendlinie fortführen TREND_LENGTH
        start_idx = x1
        end_idx = min(current_step, start_idx + TREND_LENGTH)
        trend_x = list(range(start_idx, end_idx))
        trend_y = [trend_m*xi + trend_b for xi in trend_x]

        visible_trend = [(xi, yi) for xi, yi in zip(trend_x, trend_y) if xi >= current_step - VISIBLE]
        if visible_trend:
            tx, ty = zip(*visible_trend)
            ax.plot(tx, ty, linestyle="--", color="gray", linewidth=2, label="Projected Downtrend")

        # Breakout Detection
        for xi, yi in zip(trend_x, trend_y):
            if xi >= current_step - VISIBLE:
                price_now = df["close"].iloc[xi]
                if price_now > yi and xi not in breakout_points:
                    breakout_points.append(xi)

    # --------------------------
    # Marker zeichnen
    # --------------------------
    def draw_point(point, color):
        if point and point["idx"] >= current_step - VISIBLE:
            ax.scatter(point["idx"], point["price"], color=color, s=120, alpha=0.6,
                       marker='o' if phase < 3 else 'x')

    draw_point(MAX1, "blue")
    draw_point(MAX2, "blue")
    draw_point(MIN1, "red")
    draw_point(MIN2, "red")

    # Breakout Marker
    for b_idx in breakout_points:
        if b_idx >= current_step - VISIBLE:
            ax.scatter(b_idx, df["close"].iloc[b_idx], color="green", s=120, marker='x', label="Breakout")

    ax.set_title(f"Market Structure | Phase {phase} | Step {current_step}")
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
