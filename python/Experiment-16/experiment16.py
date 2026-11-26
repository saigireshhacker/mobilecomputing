import numpy as np

# Function to calculate Free-Space Path Loss
def fspl_db(d_km, f_mhz):
    """Calculate FSPL in dB"""
    return 20 * np.log10(d_km) + 20 * np.log10(f_mhz) + 32.44

# Transmitter and receiver parameters
Pt_dbm = 43.0
Gt_db = 15.0
Gr_db = 0.0

# Distance values in kilometres
distances = [0.1, 0.5, 1, 2, 5, 10]

# Calculate for 900 MHz and 1800 MHz
for f in (900, 1800):

    print(f"\nFrequency = {f} MHz")
    print(f"{'d (km)':>8}{'FSPL (dB)':>12}{'Pr (dBm)':>11}{'Pr (W)':>14}")

    for d in distances:

        # Calculate path loss
        L = fspl_db(d, f)

        # Calculate received power in dBm
        Pr = Pt_dbm + Gt_db + Gr_db - L

        # Convert received power from dBm to Watts
        Pr_w = 10**(Pr / 10) / 1000

        print(f"{d:8.1f}{L:12.2f}{Pr:11.2f}{Pr_w:14.3e}")
