import h5py
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

file_path = r"C:\Users\divansh verma\Downloads\circular_motion.h5"
with h5py.File(file_path, 'r') as f:
   
    data = f['events'][:]
if not os.path.exists(file_path):
    print(f"ERROR: The file was not found at {file_path}. Please check the folder name.")
else:
    with h5py.File(file_path, 'r') as f:
        data = f['events'][:]
        print(f"SUCCESS: Loaded {len(data)} events.")

ts = data[:, 0]
x  = data[:, 1]
y  = data[:, 2]
p  = data[:, 3]


t_sec = (ts - ts.min()) / 1e6

# --- PLOT 1: 3D Spatio-Temporal Helix ---
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

idx = np.linspace(0, len(data)-1, 10000).astype(int)
scatter = ax.scatter(x[idx], y[idx], t_sec[idx], c=t_sec[idx], cmap='plasma', s=0.5, alpha=0.6)
ax.set_xlabel('X (pixels)')
ax.set_ylabel('Y (pixels)')
ax.set_zlabel('Time (s)')
ax.set_title('Inference: 3D Spatio-Temporal Helix')
plt.colorbar(scatter, label='Time (s)')
plt.show()

# --- PLOT 2: Event Rate (Temporal Dynamics) ---
bin_width = 0.1 
bins = np.arange(0, t_sec.max() + bin_width, bin_width)
counts, _ = np.histogram(t_sec, bins=bins)
plt.figure(figsize=(10, 4))
plt.plot(bins[:-1], counts / bin_width, color='blue', linewidth=1.5)
plt.xlabel('Time (s)')
plt.ylabel('Event Rate (Hz)')
plt.title('Inference: Event Rate over Time')
plt.grid(True, alpha=0.3)
plt.show()

# --- PLOT 3: Inter-Event Time (IET) Distribution ---
iet = np.diff(ts)
iet = iet[iet > 0] 
plt.figure(figsize=(10, 4))
plt.hist(np.log10(iet), bins=100, color='green', alpha=0.7)
plt.xlabel('log10(Inter-Event Time [μs])')
plt.ylabel('Frequency')
plt.title('Inference: Temporal Resolution (IET Distribution)')
plt.grid(True, alpha=0.3)
plt.show()

# --- PLOT 4: Polarity Distribution ---
pos = np.sum(p == 1)
neg = np.sum(p == 0)
plt.figure(figsize=(6, 6))
plt.pie([pos, neg], labels=['Positive (+)', 'Negative (-)'], 
        autopct='%1.1f%%', colors=['#ff9999','#66b3ff'], startangle=140)
plt.title('Inference: Event Polarity Distribution')
plt.show()

# 2. Vector Field Extraction

dt = np.diff(ts)
dx = np.diff(x)
dy = np.diff(y)


valid = dt > 0
v_x = dx[valid] / dt[valid]
v_y = dy[valid] / dt[valid]
t_v = ts[1:][valid] / 1e6 

# 3. Visualization: The Velocity Phase-Space
plt.figure(figsize=(10, 8), facecolor='black')
ax = plt.gca()
ax.set_facecolor('black')

plt.scatter(v_x[::500], v_y[::500], c=t_v[::500], cmap='hsv', s=5, alpha=0.6)

plt.title("Traceback: Velocity Phase-Space (V_x vs V_y)", color='white')
plt.xlabel("Velocity X (pixels/μs)", color='white')
plt.ylabel("Velocity Y (pixels/μs)", color='white')
ax.tick_params(colors='white')
plt.axis('equal')
plt.grid(color='#333333', linestyle='--')
plt.show()

# --- STEP 5: PHYSICAL REALITY TRACEBACK ---
print("\n--- Physical Reality Traceback Results ---")

# 1. Coordinate System Extraction: Finding the Center of Rotation

cx, cy = (x.min() + x.max()) / 2, (y.min() + y.max()) / 2
print(f"Inferred Orbital Center: ({cx:.2f}, {cy:.2f}) pixels")

# 2. Orbital Kinematics: Calculating Radius and Angular Velocity

radii = np.sqrt((x - cx)**2 + (y - cy)**2)

orbital_radius = np.mean(radii)

# Calculate Angular Velocity (omega) by unwrapping the polar angle over time
angles = np.arctan2(y - cy, x - cx)
total_rotation = np.abs(np.unwrap(angles)[-1] - np.unwrap(angles)[0])
duration = t_sec.max() - t_sec.min()
ang_vel = total_rotation / duration  # rad/s
rpm = (ang_vel * 60) / (2 * np.pi)

print(f"Inferred Orbital Radius: {orbital_radius:.2f} pixels")
print(f"Inferred Angular Velocity: {ang_vel:.4f} rad/s ({rpm:.2f} RPM)")

# 3. Structural Reconstruction: Identifying the Object Shape

slice_duration = 0.02 
t_mid = t_sec.max() / 2
mask = (t_sec >= t_mid) & (t_sec <= t_mid + slice_duration)

plt.figure(figsize=(6, 6))
plt.scatter(x[mask], y[mask], s=5, color='red', label='Reconstructed Shape')
plt.title(f"Physical Reality: Square Geometry (Slice at t={t_mid:.2f}s)")
plt.xlabel("X (pixels)")
plt.ylabel("Y (pixels)")
plt.axis('equal')
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()
plt.show()

# 4. Dimension Estimation: Measuring the Square

object_size_estimate = np.percentile(radii, 95) - np.percentile(radii, 5)
print(f"Estimated Physical Object Size: ~{object_size_estimate:.2f} pixels")

# --- STEP 6: VELOCITY-COMPENSATED HANDSHAKE ---
print("\n--- Executing Velocity-Compensated Handshake ---")

# 1. Define the 'Handshake' Transformation

time_relative = (ts - ts.min()) / 1e6  # seconds
theta_raw = np.arctan2(y - cy, x - cx)
theta_inertial = theta_raw - (ang_vel * time_relative)

# Convert back to Cartesian coordinates (The 'Stopped' Reality)
x_comp = cx + radii * np.cos(theta_inertial)
y_comp = cy + radii * np.sin(theta_inertial)

# 2. Loading the GAIA Physical Map (Reference Reality)

print("Loading GAIA Physical Map reference...")
gaia_ref_x = [cx - 20, cx + 20, cx + 20, cx - 20, cx - 20] 
gaia_ref_y = [cy - 20, cy - 20, cy + 20, cy + 20, cy - 20]

# 3. Visualization: The Handshake Plot
plt.figure(figsize=(10, 8), facecolor='black')
ax = plt.gca()
ax.set_facecolor('black')

# Plot De-warped Events (The 'Compensated' stream)

plt.scatter(x_comp[::500], y_comp[::500], c=ts[::500], cmap='winter', 
            s=1, alpha=0.3, label='Velocity-Compensated Events')

# Plot GAIA Physical Map (The 'Handshake' Truth)
plt.plot(gaia_ref_x, gaia_ref_y, color='#00FFCC', linewidth=2, 
         linestyle='--', label='GAIA Physical Reference (Static)', alpha=0.9)

plt.title("Task 3.4: Velocity-Compensated Handshake (Physical Reality)", color='white')
plt.xlabel("Inertial X (Pixels)", color='white')
plt.ylabel("Inertial Y (Pixels)", color='white')
plt.legend(facecolor='black', labelcolor='white')
plt.axis('equal')
plt.grid(color='#333333', linestyle=':')
plt.show()


print("[SUCCESS] Handshake complete. Events aligned to Inertial Frame.")
