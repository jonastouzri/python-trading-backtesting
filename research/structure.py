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
START_INDEX = 50
SLIDING_START = 100
WINDOW_SIZE = 50
RIGHT_PADDING = 5

current_step = START_INDEX
dist = 10

MAX0 = None
MIN0 = None
MAX1 = None
MIN1 = None

fig, ax = plt.subplots()
plt.ion()
price_line, = ax.plot([], [], color="black", linewidth=1)


max0_point, = ax.plot([], [], "ro", markersize=10, alpha=0.4)


def update_points(idx, price):
    global MAX0, MIN0, MAX1, MIN1
    if MAX0 is None:
        MAX0 = {"idx": idx, "price": price}
    elif price > MAX0["price"]:
        MAX0 = {"idx": idx, "price": price}

def draw_points(window_df):
    global MAX0, MIN0, MAX1, MIN1
    if MAX0["idx"] >= window_df["candle_index"].iloc[0]:
        max0_point.set_data([MAX0["idx"]], [MAX0["price"]])
    else:
        max0_point.set_data([], [])


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

    # --------------------------
    # Running MAX ab Kerze 50
    price = df["close"].iloc[current_step - 1]
    idx = current_step - 1

    update_points(idx, price)
    draw_points(window_df)

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
warmup_df = df.iloc[:START_INDEX]
x = warmup_df["candle_index"].values
y = warmup_df["close"].values

price_line.set_data(x, y)
ax.set_xlim(x[0], x[-1] + RIGHT_PADDING)
ax.set_ylim(y.min() * 0.999, y.max() * 1.001)
ax.set_title("Warmup (erste 50 Kerzen)")

plt.show(block=True)
