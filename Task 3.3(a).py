import numpy as np
import pandas as pd

file_path = r"C:\Users\divansh verma\Downloads\raw_events_stars.npz"
data = np.load(file_path)


print("Arrays in this file:", data.files)


x = data['x']
y = data['y']
t = data['t']
p = data['p']

print(f"Total Events: {len(x)}")
print(f"Time Range: {t[0]} to {t[-1]} microseconds")
print(f"First 5 timestamps (in microseconds): {t[:5]}")


import matplotlib.pyplot as plt

def analyze_event_data(file_path):
    
    data = np.load(file_path)
    x, y, t, p = data['x'], data['y'], data['t'], data['p']
    
    print(f"--- Deep Analysis: {file_path} ---")
    
    
    fig, axs = plt.subplots(2, 2, figsize=(15, 12), facecolor='#121212')
    plt.subplots_adjust(hspace=0.3, wspace=0.3)

    # 1. TRAJECTORY PLOT (Spatial + Time)
    slice_idx = 40000 
    scatter = axs[0, 0].scatter(x[:slice_idx], y[:slice_idx], c=t[:slice_idx], 
                                 cmap='plasma', s=0.5, alpha=0.6)
    axs[0, 0].set_title("Star Trajectories (Color = Time)", color='white')
    axs[0, 0].set_facecolor('black')
    fig.colorbar(scatter, ax=axs[0, 0], label='Microseconds')

    # 2. ACTIVITY HEATMAP (Density)
    axs[0, 1].hist2d(x, y, bins=128, cmap='inferno')
    axs[0, 1].set_title("Pixel Activity Heatmap (Where are the stars?)", color='white')
    axs[0, 1].set_facecolor('black')

    # 3. TIME SERIES (Event Rate)
    axs[1, 0].hist(t / 1e6, bins=100, color='cyan', alpha=0.7)
    axs[1, 0].set_title("Event Rate Over Time (Seconds)", color='white')
    axs[1, 0].set_xlabel("Time (s)")
    axs[1, 0].set_ylabel("Number of Events")

    # 4. POLARITY BALANCE (+1 vs -1)
    unique, counts = np.unique(p, return_counts=True)
    axs[1, 1].bar(['Dimming (-1)', 'Brightening (+1)'], counts, color=['red', 'green'])
    axs[1, 1].set_title("Polarity Distribution", color='white')

    # Formatting text colors 
    for ax in axs.flat:
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.tick_params(colors='white')

    plt.suptitle(f"Event Analysis Dashboard: {file_path.split('/')[-1]}", 
                 color='white', fontsize=16)
    plt.show()


analyze_event_data(r"C:\Users\divansh verma\Downloads\raw_events_stars.npz")

limit = 100000 

df = pd.DataFrame({
    't': data['t'][:limit],
    'x': data['x'][:limit],
    'y': data['y'][:limit],
    'p': data['p'][:limit]
})

# Save to CSV
df.to_csv("event_sample_100k.csv", index=False)
print("Saved 100,000 events to event_sample_100k.csv")



