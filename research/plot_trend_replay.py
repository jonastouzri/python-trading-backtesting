# research/plot_trend_replay.py

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np

# ------------------------
# Hilfsfunktionen
# ------------------------

def load_csv(path: str):
    df = pd.read_csv(path, sep="\t")
    df["time"] = pd.to_datetime(df["time"], format="%Y.%m.%d %H:%M:%S")
    return df

def find_swing_points(df_window):
    """
    Einfacher Swing Point Finder:
    - High = Close höher als vorherige & nachfolgende Kerze
    - Low = Close niedriger als vorherige & nachfolgende Kerze
    """
    closes = df_window["close"].values
    swing_highs = []
    swing_lows = []
    
    for i in range(1, len(closes)-1):
        if closes[i] > closes[i-1] and closes[i] > closes[i+1]:
            swing_highs.append((i, closes[i]))
        elif closes[i] < closes[i-1] and closes[i] < closes[i+1]:
            swing_lows.append((i, closes[i]))
    
    return swing_highs, swing_lows

def draw_trendline(ax, points, color="green", linestyle="--"):
    if len(points) >= 3:
        x = [p[0] for p in points]
        y = [p[1] for p in points]
        coeffs = np.polyfit(x, y, 1)
        trend_y = np.polyval(coeffs, x)
        ax.plot(x, trend_y, color=color, linestyle=linestyle, linewidth=2)

# ------------------------
# Replay-Funktion
# ------------------------

def trend_replay(df, window_size=30):
    index = window_size  # Start bei Kerze window_size (Index 1 = letzte abgeschlossene Kerze)
    max_index = len(df) - 1
    
    while True:
        df_window = df.iloc[index-window_size:index]
        
        swing_highs, swing_lows = find_swing_points(df_window)
        
        # Plot erstellen
        fig, ax = plt.subplots(figsize=(12,6))
        ax.plot(df_window.index, df_window["close"], color="black", label="Close")
        
        # Swing-Punkte plotten
        if swing_highs:
            ax.scatter([p[0] for p in swing_highs], [p[1] for p in swing_highs], color="blue", label="ZigZag Highs")
        if swing_lows:
            ax.scatter([p[0] for p in swing_lows], [p[1] for p in swing_lows], color="orange", label="ZigZag Lows")
        
        # Trendlinien zeichnen
        draw_trendline(ax, swing_highs, color="blue", linestyle="--")
        draw_trendline(ax, swing_lows, color="orange", linestyle="--")
        
        ax.set_title(f"Trend Replay | Kerze Index: {index}")
        ax.set_xlabel("Candle Index")
        ax.set_ylabel("Close Price")
        ax.legend()
        plt.show(block=False)
        plt.pause(0.01)
        
        # User Input
        key = input("n=next, b=back, q=quit: ").lower()
        plt.close(fig)
        if key == "n":
            if index < max_index:
                index += 1
            else:
                print("End of data reached")
        elif key == "b":
            if index > window_size:
                index -= 1
            else:
                print("Start of data reached")
        elif key == "q":
            break
        else:
            print("Unknown command. Use n, b, or q.")

# ------------------------
# Main
# ------------------------

def main():
    path = "../data/XAUUSD_PERIOD_15_SHORT.csv"
    df = load_csv(path)
    trend_replay(df, window_size=30)

if __name__ == "__main__":
    main()
