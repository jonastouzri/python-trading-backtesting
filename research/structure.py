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
df.rename(columns={"index": "candle_index"}, inplace=True)

# --------------------------
# Parameter
# --------------------------
START_INDEX = 570
SLIDING_START = 100
WINDOW_SIZE = 50
RIGHT_PADDING = 5

current_step = START_INDEX
sensitivity = 10

RESET = {"idx": -1, "p": -1}

MAX0 = RESET
MIN0 = RESET
MAX1 = RESET
MIN1 = RESET

line0 = {"idx": [], "p": [], "m": 0, "b": 0}
line1 = {"idx": [], "p": [], "m": 0, "b": 0}

fig, ax = plt.subplots()
plt.ion()
price_line, = ax.plot([], [], color="black", linewidth=1)

max0_point, = ax.plot([], [], "ro", markersize=10, alpha=0.4)
min0_point, = ax.plot([], [], "bo", markersize=10, alpha=0.4)
max1_point, = ax.plot([], [], "ro", markersize=7, alpha=0.4)
min1_point, = ax.plot([], [], "bo", markersize=7, alpha=0.4)

plt0_line, = ax.plot([], [], "--", color="gray", linewidth=1, markersize=10, alpha=0.6)
plt1_line, = ax.plot([], [], "-", color="green", linewidth=1, markersize=10, alpha=0.6)


def compute_line():
    global MAX0, MAX1
    m = (MAX0["p"] - MAX1["p"]) / (MAX0["idx"] - MAX1["idx"])
    b = MAX0["p"] - m * MAX0["idx"]

    return {
        "idx": [MAX0["idx"], MAX1["idx"]],
        "p": [MAX0["p"], MAX1["p"]],
        "m": m,
        "b": b
    }




def active(point):
    return point["idx"] != -1


def line_active(line):
    return len(line["idx"]) > 0


def update_points(idx, price):
    global MAX0, MIN0, MAX1, MIN1
    global line0, line1

    if active(MIN1):
        if price < MIN0["p"]:
            if current_step - MIN0["idx"] > sensitivity:
                print("Trend confirmed")

                if not line_active(line0):
                    line0 = compute_line()
                elif not line_active(line1):
                    line1 = compute_line()

                MAX0 = RESET
                MIN0 = RESET
                MAX1 = RESET
                MIN1 = RESET

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


def draw_line(idx, line_obj, line_plt):
    if not line_active(line_obj):
        return

    line_obj["idx"].append(idx)
    line_obj["p"].append(line_obj["m"] * idx + line_obj["b"])
    line_plt.set_data([line_obj["idx"]], [line_obj["p"]])




def redraw():
    global MAX0, MIN0, MAX1, MIN1

    # if current_step < SLIDING_START:
    #     window_df = df.iloc[:current_step]
    # else:
    #     window_df = df.iloc[current_step - WINDOW_SIZE: current_step]

    full_df = df.iloc[:current_step]
    idx = full_df["candle_index"].values
    prices = full_df["close"].values


    price_line.set_data(idx, prices)
    ax.set_xlim(
        idx[-WINDOW_SIZE],
        idx[-1] + RIGHT_PADDING
    )

    # ax.set_ylim(prices.min() * 0.999, prices.max() * 1.001)
    ax.set_ylim(prices[-1] - 3, prices[-1] + 3)

    # Running MAX ab Kerze 50
    price = df["close"].iloc[current_step - 1]
    idx = current_step - 1

    update_points(idx, price)
    draw_point(MAX0, max0_point)
    draw_point(MIN0, min0_point)
    draw_point(MAX1, max1_point)
    draw_point(MIN1, min1_point)

    draw_line(idx, line0, plt0_line)
    draw_line(idx, line1, plt1_line)

    ax.set_title(f"Running {START_INDEX} | Step {current_step}")
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
x = warmup_df["candle_index"].values
y = warmup_df["close"].values

price_line.set_data(x, y)
ax.set_xlim(x[0], x[-1] + RIGHT_PADDING)
ax.set_ylim(y.min() * 0.999, y.max() * 1.001)
# .set_yticks(y.min() * 0.999, y.max() * 1.001)

plt.grid(True)
plt.show(block=True)
