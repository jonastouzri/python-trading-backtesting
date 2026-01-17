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
START_INDEX = 1000500
SLIDING_START = 100
WINDOW_SIZE = 300
RIGHT_PADDING = 50

WINDOW_Y = 4

current_step = START_INDEX
sensitivity = 10

RESET = {"idx": -1, "p": -1}

MAX0 = RESET
MIN0 = RESET
MAX1 = RESET
MIN1 = RESET

TREND_OBJ_RESET = {"idx": [], "p": [], "m": 0, "b": 0, "idx_min1": 0}
trend_A = TREND_OBJ_RESET
trend_B = TREND_OBJ_RESET
trend_C = TREND_OBJ_RESET



fig, ax = plt.subplots(figsize=(10, 8))
plt.ion()
price_line, = ax.plot([], [], color="black", linewidth=1)

max0_point, = ax.plot([], [], "ro", markersize=10, alpha=0.4)
min0_point, = ax.plot([], [], "bo", markersize=10, alpha=0.4)
max1_point, = ax.plot([], [], "ro", markersize=7, alpha=0.4)
min1_point, = ax.plot([], [], "bo", markersize=7, alpha=0.4)

plt_trend_A, = ax.plot([], [], "--", color="gray", linewidth=1, markersize=10, alpha=0.6)
plt_trend_B, = ax.plot([], [], "--", color="gray", linewidth=1, markersize=10, alpha=0.6)
plt_trend_C, = ax.plot([], [], "--", color="gray", linewidth=1, markersize=10, alpha=0.6)


def compute_trend():
    global MAX0, MAX1, MIN0, MIN1
    m = (MAX0["p"] - MAX1["p"]) / (MAX0["idx"] - MAX1["idx"])
    b = MAX0["p"] - m * MAX0["idx"]

    return {
        "idx": [MAX0["idx"], MAX1["idx"]],
        "p": [MAX0["p"], MAX1["p"]],
        "m": m,
        "b": b,
        "idx_min1": MIN1["idx"] + 1
    }


def trend_invalid(prices, trend, n=5):
    idx2 = trend["idx_min1"]
    # start comparing price and trend values exactly after trend is being confirmed, this is at idx of MIN1
    prices = np.asarray(prices[idx2:])
    trend = np.asarray(trend["p"][2:])  # ignore idx2 of MAX0, MAX1

    if len(prices) < n:
        return False

    print("prices  ", prices)
    print("trend    ", trend)
    print(np.all(prices[-n:] > trend[-n:]))

    return np.all(prices[-n:] > trend[-n:])


def update_trend(indices, prices, trend):
    # check if a spike above the trend line appeared, but lower than the max1 price
    # this must be checked after the trend has been confirmed

    if not trend_active(trend):
        return

    idx0 = trend["idx"][0]
    idx1 = trend["idx"][1]
    idx2 = trend["idx_min1"]
    section_trend = trend["m"] * indices[idx1: idx2] + trend["b"]
    section_prices = prices[idx1: idx2]

    delta = section_prices - section_trend
    max_point_idx = np.argmax(delta)
    max_point = delta[max_point_idx]

    prices = np.array(section_prices)
    trend = np.array(section_trend)

    mask = prices > trend

    max_idx = None
    max_price = None
    if np.any(mask):
        max_idx = np.argmax(prices * mask)
        max_price = prices[max_idx]

    # print(idx1 + max_idx)
    # print(max_price)


"""
function to check if 
"""


def check_lines():
    global trend_A, trend_B, trend_C


def active(point):
    return point["idx"] != -1


def trend_active(trend):
    return len(trend["idx"]) > 0


def spot_trend(idx, price):
    global MAX0, MIN0, MAX1, MIN1
    global trend_A, trend_B

    if active(MIN1):
        if price < MIN0["p"]:
            if current_step - MIN0["idx"] > sensitivity:
                print("Trend confirmed")

                if not trend_active(trend_A):
                    trend_A = compute_trend()
                elif not trend_active(trend_B):
                    trend_B = compute_trend()

                print(MAX0)
                print(MIN0)
                print(MAX1)
                print(MIN1)

                MAX0 = MAX1
                MIN0 = RESET
                MAX1 = RESET
                MIN1 = RESET
                print("reset points")

    # MAX1
    if active(MAX1):
        if price > MAX1["p"]:
            MAX1 = {"idx": idx, "p": price}
            MIN1 = RESET
        elif price < MAX1["p"]:
            MIN1 = {"idx": idx, "p": price}

    # MIN0
    if active(MIN0):
        if price > MIN0["p"]:
            if not active(MAX1):
                MAX1 = {"idx": idx, "p": price}
        elif price < MIN0["p"]:
            MIN0 = {"idx": idx, "p": price}
            MAX1 = RESET
            MIN1 = RESET

    # MAX0
    if not active(MAX0):
        MAX0 = {"idx": idx, "p": price}
    elif price >= MAX0["p"]:
        MAX0 = {"idx": idx, "p": price}
        MIN0 = RESET
        MAX1 = RESET
        MIN1 = RESET
    elif price < MAX0["p"]:
        if not active(MIN0):
            MIN0 = {"idx": idx, "p": price}


def draw_point(point, pp):
    if active(point):
        pp.set_data([point["idx"]], [point["p"]])
    else:
        pp.set_data([], [])


def draw_trend(idx, price, trend_obj, trend_plt):
    if not trend_active(trend_obj):
        return

    next_trend_value = trend_obj["m"] * idx + trend_obj["b"]

    trend_obj["idx"].append(idx)
    trend_obj["p"].append(next_trend_value)
    trend_plt.set_data([trend_obj["idx"]], [trend_obj["p"]])


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
    indices = full_df["index"].values
    prices = full_df["close"].values
    times = full_df["time"].values

    price_line.set_data(indices, prices)
    set_axis(indices, prices)

    idx = current_step - 1
    price = df["close"].iloc[current_step - 1]

    spot_trend(idx, price)

    draw_point(MAX0, max0_point)
    draw_point(MIN0, min0_point)
    draw_point(MAX1, max1_point)
    draw_point(MIN1, min1_point)

    draw_trend(idx, price, trend_A, plt_trend_A)
    draw_trend(idx, price, trend_B, plt_trend_B)

    # update_trend(indices, prices, trend_A)

    if trend_active(trend_A):
        if trend_invalid(prices, trend_A):
            delete_trend(plt_trend_A)
            trend_A = TREND_OBJ_RESET
            print("trend invalid")


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
# .set_yticks(y.min() * 0.999, y.max() * 1.001)

plt.grid(True)
plt.show(block=True)
