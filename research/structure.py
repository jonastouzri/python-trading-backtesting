import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --------------------------
# CSV laden
# --------------------------
df = pd.read_csv(
    "data/XAUUSD_PERIOD_01.csv",
    sep="\t",
    dtype={"close": float}
)
df = df.dropna(subset=["close"])
df.reset_index(inplace=True)

# --------------------------
# Parameter
# --------------------------
START_INDEX = 302050
SLIDING_START = 100
WINDOW_SIZE = 300
RIGHT_PADDING = 50

WINDOW_Y = 4

current_step = START_INDEX
DISTANCE = 20

POINT_RESET = {"idx": -1, "p": -1}

MAX0 = POINT_RESET
MIN0 = POINT_RESET
MAX1 = POINT_RESET
MIN1 = POINT_RESET

TREND_OBJ_RESET = {
    "idx": [],
    "p": [],
    "m": 0, "b": 0,
    "idx_min1": 0,
    "id": None
}


def set_trend_obj(name):
    return {"idx": [], "p": [], "m": 0, "b": 0, "idx_min1": 0}


trend_A = TREND_OBJ_RESET
trend_B = TREND_OBJ_RESET
trend_C = TREND_OBJ_RESET

fig, (ax, ax_macd) = plt.subplots(2, 1, figsize=(10, 8), sharex=True, gridspec_kw={"height_ratios": [1, 1]})
plt.ion()

price_line, = ax.plot([], [], color="black", linewidth=1)

max0_point, = ax.plot([], [], "ro", markersize=10, alpha=0.4)
min0_point, = ax.plot([], [], "bo", markersize=10, alpha=0.4)
max1_point, = ax.plot([], [], "ro", markersize=7, alpha=0.4)
min1_point, = ax.plot([], [], "bo", markersize=7, alpha=0.4)

plt_trend_A, = ax.plot([], [], "--", color="gray", linewidth=1, markersize=10, alpha=0.6)
plt_trend_B, = ax.plot([], [], "--", color="gray", linewidth=1, markersize=10, alpha=0.6)
plt_trend_C, = ax.plot([], [], "--", color="gray", linewidth=1, markersize=10, alpha=0.6)



# MACD lines
macd_line, = ax_macd.plot([], [], color="blue", linewidth=1, label="MACD")
signal_line, = ax_macd.plot([], [], color="orange", linewidth=1, label="Signal")
hist_line, = ax_macd.plot([], [], color="gray", linewidth=1, alpha=0.5, label="Hist")

ax_macd.axhline(0, color="black", linewidth=0.8)
ax_macd.legend(loc="upper left")
ax_macd.grid(True)


def compute_macd(prices, fast=12, slow=26, signal=9):
    prices = pd.Series(prices)
    ema_fast = prices.ewm(span=fast, adjust=False).mean()
    ema_slow = prices.ewm(span=slow, adjust=False).mean()
    macd = ema_fast - ema_slow
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    hist = macd - signal_line
    return macd.values, signal_line.values, hist.values

def compute_trend_from_structure(id):
    global MAX0, MAX1, MIN0, MIN1
    m = (MAX0["p"] - MAX1["p"]) / (MAX0["idx"] - MAX1["idx"])
    b = MAX0["p"] - m * MAX0["idx"]

    return {
        "idx": [MAX0["idx"], MAX1["idx"]],
        "p": [MAX0["p"], MAX1["p"]],
        "m": m,
        "b": b,
        "idx_min1": MIN1["idx"] + 1,
        "id": id
    }


def trend_invalid(prices, trend, n=5):
    idx_min1 = trend["idx_min1"]
    # if idx_min1 is None:
    #     return False
    # start comparing price and trend values exactly
    # after trend is being confirmed, this is at idx of MIN1
    prices = np.asarray(prices[idx_min1:])
    trend = np.asarray(trend["p"][2:])  # ignore idx2 of MAX0, MAX1
    # print("prices  ", prices)
    # print("trend    ", trend)
    if len(prices) < n:
        return False

    return np.all(prices[-n:] > trend[-n:])


def update_trend(indices, prices, trend_obj):
    global MAX0
    # check if a spike above the trend line appeared, but lower than the max1 price
    # this must be checked after the trend has been confirmed

    if not trend_active(trend_obj):
        return

    idx_min1 = trend_obj["idx_min1"]
    if idx_min1 is None:
        return


    idx0 = trend_obj["idx"][0]
    idx1 = trend_obj["idx"][1]

    section_trend = trend_obj["m"] * indices[idx1+1: idx_min1] + trend_obj["b"]
    section_prices = prices[idx1+1: idx_min1]

    prices = np.array(section_prices)
    trend = np.array(section_trend)
    mask = prices >= trend

    max_idx = None
    max_price = None
    if np.any(mask):
        max_idx = np.argmax(prices * mask)
        max_price = prices[max_idx]

    if max_idx is None:
        return

    ##############################

    print("---------------")
    # MAX0
    p0_idx = trend_obj["idx"][0]
    p0_price = trend_obj["p"][0]
    print("P0")
    print("p0_idx", p0_idx)
    print("p0_price", p0_price)


    p1_idx = idx1 + max_idx + 1
    p1_price = max_price
    print("P1")
    print("p1_idx", p1_idx)
    print("p1_price", p1_price)


    m = (p0_price - p1_price) / (p0_idx - p1_idx)
    b = p0_price - m * p0_idx

    id = trend_obj["id"]

    trend_obj.clear()
    trend_obj.update({
        "idx": [p0_idx, p1_idx],
        "p": [p0_price, p1_price],
        "m": m,
        "b": b,
        "idx_min1": None,
        "id": id
    })

    #MAX0 = {"idx": p1_idx, "p": p1_price}

    MAX0 = {"idx": p1_idx, "p": p1_price}
    MIN0 = POINT_RESET
    MAX1 = POINT_RESET
    MIN1 = POINT_RESET


   # print("Updated", trend_obj["id"])
   #hier gehts weiter



def check_lines():
    global trend_A, trend_B, trend_C


def active(point):
    return point["idx"] != -1


def trend_active(trend):
    return len(trend["idx"]) > 0


def spot_trend_structure(idx, price):
    global MAX0, MIN0, MAX1, MIN1
    global trend_A, trend_B, trend_C

    if active(MIN1):
        if price <= MIN0["p"]:
            if current_step - MIN0["idx"] > DISTANCE:
                print("Trend confirmed")

                # todo very ugly approach
                if not trend_active(trend_A):
                    trend_A = compute_trend_from_structure("trend_A")
                    print("Created trend_A")
                elif not trend_active(trend_B):
                    trend_B = compute_trend_from_structure("trend_B")
                    print("Created trend_B")
                elif not trend_active(trend_C):
                    trend_B = compute_trend_from_structure("trend_C")
                    print("Created trend_C")

                MAX0 = MAX1
                MIN0 = POINT_RESET
                MAX1 = POINT_RESET
                MIN1 = POINT_RESET
                print("reset points")

    # MAX1
    if active(MAX1):
        if price >= MAX1["p"]:
            MAX1 = {"idx": idx, "p": price}
            MIN1 = POINT_RESET
        elif price < MAX1["p"]:
            MIN1 = {"idx": idx, "p": price}

    # MIN0
    if active(MIN0):
        if price > MIN0["p"]:
            if not active(MAX1):
                MAX1 = {"idx": idx, "p": price}
        elif price <= MIN0["p"]:
            MIN0 = {"idx": idx, "p": price}
            MAX1 = POINT_RESET
            MIN1 = POINT_RESET

    # MAX0
    if not active(MAX0):
        MAX0 = {"idx": idx, "p": price}
    elif price >= MAX0["p"]:
        MAX0 = {"idx": idx, "p": price}
        MIN0 = POINT_RESET
        MAX1 = POINT_RESET
        MIN1 = POINT_RESET
    elif price < MAX0["p"]:
        if not active(MIN0):
            MIN0 = {"idx": idx, "p": price}


def draw_point(point, pp):
    if active(point):
        pp.set_data([point["idx"]], [point["p"]])
    else:
        pp.set_data([], [])


def draw_trend(idx, prices, trend_obj, trend_plt):
    if not trend_active(trend_obj):
        return

    next_trend_value = trend_obj["m"] * idx + trend_obj["b"]

    trend_obj["idx"].append(idx)
    trend_obj["p"].append(next_trend_value)
    trend_plt.set_data([trend_obj["idx"]], [trend_obj["p"]])

    # Remove trend after price broke through
    if trend_invalid(prices, trend_obj):
        delete_trend(trend_plt)
        print("Deleted", trend_obj["id"])
        trend_obj.clear()
        trend_obj.update(TREND_OBJ_RESET)


def delete_trend(trend_plt):
    trend_plt.set_data([], [])


def set_axis(idx, prices):
    ax.set_xlim(
        idx[-WINDOW_SIZE],
        idx[-1] + RIGHT_PADDING
    )

    # ax.set_ylim(prices[-1] - WINDOW_Y / 2, prices[-1] + WINDOW_Y / 2)
    ax.set_ylim(prices[
                current_step - WINDOW_SIZE: -1].min() * 0.999,
                prices[current_step - WINDOW_SIZE: -1].max() * 1.001
                )


def redraw():
    global MAX0, MIN0, MAX1, MIN1
    global trend_A, trend_B, trend_C

    full_df = df.iloc[:current_step]
    idxs = full_df["index"].values
    prices = full_df["close"].values
    times = full_df["time"].values

    price_line.set_data(idxs, prices)
    set_axis(idxs, prices)

    idx = current_step - 1
    price = df["close"].iloc[current_step - 1]

    spot_trend_structure(idx, price)

    draw_point(MAX0, max0_point)
    draw_point(MIN0, min0_point)
    draw_point(MAX1, max1_point)
    draw_point(MIN1, min1_point)

    draw_trend(idx, prices, trend_A, plt_trend_A)
    draw_trend(idx, prices, trend_B, plt_trend_B)


    # ---- MACD ----
    macd, signal, hist = compute_macd(prices)
    macd_line.set_data(idxs, macd)
    signal_line.set_data(idxs, signal)
    hist_line.set_data(idxs, hist)

    ax_macd.set_xlim(idxs[-WINDOW_SIZE], idxs[-1] + RIGHT_PADDING)
    ax_macd.set_ylim(
        min(macd[-WINDOW_SIZE:]) * 1.1,
        max(macd[-WINDOW_SIZE:]) * 1.1
    )

    #update_trend(idxs, prices, trend_A)
    #

    ax.set_title(f"Running {START_INDEX} | Step {current_step} | Time {times[-1]}")
    fig.canvas.draw_idle()


# --------------------------
# Key Handling
# --------------------------
def on_key(event):
    global current_step
    if event.key == "q":
        plt.close()
        return

    current_step += 1
    if current_step >= len(df):
        print("End of data")
        plt.close()
        return

    redraw()


fig.canvas.mpl_connect("key_press_event", on_key)

# --------------------------
# Warmup Plot
# --------------------------
warmup_df = df.iloc[START_INDEX - WINDOW_SIZE:START_INDEX]
x = warmup_df["index"].values
y = warmup_df["close"].values

price_line.set_data(x, y)
ax.set_xlim(x[0], x[-1] + RIGHT_PADDING)
ax.set_ylim(y.min() * 0.999, y.max() * 1.001)


macd, signal, hist = compute_macd(y)
macd_line.set_data(x, macd[-len(x):])
signal_line.set_data(x, signal[-len(x):])
hist_line.set_data(x, hist[-len(x):])


plt.grid(True)
plt.show(block=True)
