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
START_INDEX = 500
SLIDING_START = 100
WINDOW_SIZE = 50
RIGHT_PADDING = 5

current_step = START_INDEX
sensitivity = 10

inactive = {"idx": -1, "p": -1}

MAX0 = inactive
MIN0 = inactive
MAX1 = inactive
MIN1 = inactive


REG0 = inactive

fig, ax = plt.subplots()
plt.ion()
price_line, = ax.plot([], [], color="black", linewidth=1)

max0_point, = ax.plot([], [], "ro", markersize=10, alpha=0.4)
min0_point, = ax.plot([], [], "bo", markersize=10, alpha=0.4)
max1_point, = ax.plot([], [], "ro", markersize=7, alpha=0.4)
min1_point, = ax.plot([], [], "bo", markersize=7, alpha=0.4)


reg0, = ax.plot([], [], "g+", markersize=10, alpha=0.4)


def active(point):
    return point["idx"] != -1


def update_points(idx, price):
    global MAX0, MIN0, MAX1, MIN1

    if active(MIN1):
        print("MIN0 = ", MIN0)
        print("MIN1 = ", MIN1)
        if price < MIN0["p"]:
            print("hypothetical trend detected")
            if MIN1["idx"] - MIN0["idx"] >= sensitivity:
                print("hypothetical trend too sensitive")
            else:
                print("hypothetical trend is valid")



    # MAX0
    if not active(MAX0):
        MAX0 = {"idx": idx, "p": price}
    elif price >= MAX0["p"]:
        MAX0 = {"idx": idx, "p": price}
        MIN0 = {"idx": -1, "p": -1}
        MAX1 = {"idx": -1, "p": -1}
        MIN1 = {"idx": -1, "p": -1}
        print(">")
    elif price < MAX0["p"]:
        if not active(MIN0):
            MIN0 = {"idx": idx, "p": price}
            print("<")

    # MIN0
    if active(MIN0):
        if price > MIN0["p"]:
            if not active(MAX1):
                MAX1 = {"idx": idx, "p": price}
        elif price < MIN0["p"]:
            MIN0 = {"idx": idx, "p": price}
            MAX1 = {"idx": -1, "p": -1}
            MIN1 = {"idx": -1, "p": -1}

    # MAX1
    if active(MAX1):
        if price > MAX1["p"]:
            MAX1 = {"idx": idx, "p": price}
            MIN1 = {"idx": -1, "p": -1}
        elif price < MAX1["p"]:
            MIN1 = {"idx": idx, "p": price}

    print("+++++")
    print(MAX0)
    print(MIN0)
    print(MAX1)
    print(MIN1)


def draw_point(point, pp):
    if active(point):
        pp.set_data([point["idx"]], [point["p"]])
    else:
        pp.set_data([], [])


def redraw():
    global MAX0, MIN0, MAX1, MIN1

    if current_step < SLIDING_START:
        window_df = df.iloc[:current_step]
    else:
        window_df = df.iloc[current_step - WINDOW_SIZE: current_step]

    x = window_df["candle_index"].values
    prices = window_df["close"].values

    # Preislinie
    price_line.set_data(x, prices)
    # X/Y Limits mit Padding
    ax.set_xlim(x[0], x[-1] + RIGHT_PADDING)
    ax.set_ylim(prices.min() * 0.999, prices.max() * 1.001)
    # Running MAX ab Kerze 50
    price = df["close"].iloc[current_step - 1]
    idx = current_step - 1

    update_points(idx, price)
    draw_point(MAX0, max0_point)
    draw_point(MIN0, min0_point)
    draw_point(MAX1, max1_point)
    draw_point(MIN1, min1_point)

    ax.set_title(f"Running MAX ab Kerze {START_INDEX} | Step {current_step}")
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
ax.set_title("Warmup (erste 50 Kerzen)")

plt.show(block=True)
