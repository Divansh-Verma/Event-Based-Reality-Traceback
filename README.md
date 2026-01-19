# Event-Based-Reality-Traceback
An algorithm to neutralize sensor rotation and perform a velocity-compensated handshake with GAIA maps
 

This repository implements a Physical Reality Traceback algorithm for asynchronous event-based sensors (DVS). The project demonstrates how to reconstruct the underlying physical geometry and kinematics from a "motion-blurred" event stream, culminating in a Velocity-Compensated Handshake with a static inertial reference map.

## The Challenge

Unlike frame-based cameras, event-based sensors produce a continuous stream of asynchronous spikes triggered by per-pixel brightness changes. In this scenario, a square object follows a circular trajectory over a 10-second duration. Without compensation, the resulting event cloud appears as a thick, blurry ring, obscuring the object's identity and position.

## Technical Methodology

The core of this project is a "Raw-to-Reality" pipeline that neutralizes high-speed rotation to perform an inertial lock:

### 1. Kinematic Inference

By analyzing the spatial extrema of the 486,800 events in circular_motion.h5, the algorithm identifies the absolute center of rotation and the constant angular velocity:

* Orbital Center: (119.00, 89.50) pixels.
* Angular Velocity ():  rad/s (11.42 RPM).
* Orbital Radius:  pixels.

### 2. Spatio-Temporal De-warping

Using the microsecond-accurate timestamps (), we apply a time-dependent inverse rotation to every event:



This transformation "stops" the motion, collapsing the blurry ring back into a sharp, static square geometry.

### 3. The Inertial Handshake

The final validation is a "Handshake" where the de-warped events are overlaid onto a static **GAIA Physical Reference Map**. Sub-pixel alignment between the compensated event cloud and the reference coordinates proves the successful traceback of the physical reality.

## Key Features

* **Phase-Space Analysis:** Visualization of the "Velocity Circle" to confirm central-force motion.
* **Structural Reconstruction:** 20ms temporal slicing to recover the **40.75-pixel square** geometry.
* **Helix Visualization:** 3D spatio-temporal plotting to inspect the "Motion DNA" of the trajectory.

## Dependencies

* h5py (for HDF5 data ingestion)
* numpy (for matrix transformations)
* matplotlib (for 3D and phase-space plotting)

