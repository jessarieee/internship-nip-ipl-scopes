import pandas as pd
import numpy as np

# ======================================================
# Read CSV exported from binary file
# Columns:
# Sample, Timestamp_us, Intensity
# ======================================================

input_file = "data_record.csv"

df = pd.read_csv(input_file)

# Extract columns
timestamps_us = df["Timestamp_us"].to_numpy()
signal = df["Intensity"].to_numpy(dtype=float)

# ======================================================
# Determine sampling frequency from timestamps
# ======================================================

timestamps_sec = timestamps_us * 1e-6

dt = np.mean(np.diff(timestamps_sec))
fs = 1.0 / dt

print(f"Detected Sampling Frequency: {fs:.3f} Hz")

# ======================================================
# Remove DC offset
# ======================================================

signal = signal - np.mean(signal)

# ======================================================
# FFT
# ======================================================

N = len(signal)

fft_values = np.fft.rfft(signal)

frequencies = np.fft.rfftfreq(N, d=dt)

# Normalize amplitude
amplitude = np.abs(fft_values) / N

# Double amplitudes except DC and Nyquist
if N % 2 == 0:
    amplitude[1:-1] *= 2
else:
    amplitude[1:] *= 2

# ======================================================
# Save FFT result
# ======================================================

mask = (frequencies >= 10) & (frequencies <= 2000)

fft_df = pd.DataFrame({
    "Frequency_Hz": frequencies,
    "Amplitude": amplitude
})

output_file = "fft_output_lim.csv"
fft_df.to_csv(output_file, index=False)

print(f"FFT saved to {output_file}")