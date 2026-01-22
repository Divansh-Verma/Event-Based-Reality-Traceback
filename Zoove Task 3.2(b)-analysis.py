
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def analyze_tracking_reliability(csv_file, fov_h, fov_v):
    """
    Analyzes the 'Physical Reality' of the star field to ensure 
    the sensor can maintain an 'absolute lock'.
    """
    df = pd.read_csv(csv_file)
    area = fov_h * fov_v
    stars_per_deg = len(df) / area
   
    plt.figure(figsize=(8, 6), facecolor='black')
    ax = plt.subplot(111)
    ax.set_facecolor('black')
    
    
    sizes = (15 - df['magnitude']) ** 2 
    
    plt.scatter(df['ra'], df['dec'], s=sizes, c='white', alpha=0.8)
    plt.title(f"Sensor View: {csv_file}\nDensity: {stars_per_deg:.2f} stars/deg²", color='white')
    plt.xlabel("Right Ascension (RA)", color='white')
    plt.ylabel("Declination (DEC)", color='white')
    plt.grid(color='gray', linestyle='--', alpha=0.3)
    plt.show()
    
    return stars_per_deg


wide_density = analyze_tracking_reliability('gaia_catalog_f8mm.csv', 21.98, 17.65)
narrow_density = analyze_tracking_reliability('gaia_catalog_f50mm.csv', 3.56, 2.85)