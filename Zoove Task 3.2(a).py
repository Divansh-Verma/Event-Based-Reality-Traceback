import pandas as pd
import numpy as np
from astroquery.gaia import Gaia

def get_star_map(focal_length_mm):
    """
    Step 1: Figure out how much of the sky our lens can actually see.
    """
    
    pixel_pitch_mm = 0.00486 
    width_pixels = 640
    height_pixels = 512
    
   
    sensor_width_mm = width_pixels * pixel_pitch_mm
    sensor_height_mm = height_pixels * pixel_pitch_mm
    
   
    # Formula: 2 * arctan(dimension / (2 * focal_length))
    horizontal_angle = 2 * np.degrees(np.arctan(sensor_width_mm / (2 * focal_length_mm)))
    vertical_angle = 2 * np.degrees(np.arctan(sensor_height_mm / (2 * focal_length_mm)))
    
    diagonal_size = np.sqrt(sensor_width_mm**2 + sensor_height_mm**2)
    search_radius = np.degrees(np.arctan(diagonal_size / (2 * focal_length_mm)))
    
    print(f"--- Lens: {focal_length_mm}mm ---")
    print(f"I can see a patch of sky about {horizontal_angle:.1f}° wide.")
    
    """
    Step 2: Ask the GAIA database for stars in that specific patch.
    """
    
    center_ra = 160.0
    center_dec = -13.0
    brightness_limit = 12 
    
    print(f"Searching for stars near RA {center_ra}, DEC {center_dec}...")

    
    query = f"""
    SELECT source_id, ra, dec, phot_bp_mean_mag as magnitude
    FROM gaiadr3.gaia_source
    WHERE CONTAINS(POINT('ICRS', ra, dec), 
                   CIRCLE('ICRS', {center_ra}, {center_dec}, {search_radius})) = 1
    AND phot_bp_mean_mag <= {brightness_limit}
    """
    
    
    job = Gaia.launch_job_async(query)
    found_stars = job.get_results().to_pandas()
    
    # Save the results to a simple spreadsheet
    filename = f"star_map_{focal_length_mm}mm.csv"
    found_stars.to_csv(filename, index=False)
    
    print(f"Success! Found {len(found_stars)} stars. Saved to {filename}.\n")


get_star_map(8)  # Wide view
get_star_map(50) # Zoomed-in view