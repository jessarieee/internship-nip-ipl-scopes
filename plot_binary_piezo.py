import argparse
import struct
from pathlib import Path

import matplotlib.pyplot as plt


PACKET_SIZE = struct.calcsize("<IhhH")


def read_packets(path: Path):
    data = path.read_bytes()

    if len(data) % PACKET_SIZE != 0:
        raise ValueError(
            f"Binary file size ({len(data)} bytes) is not a multiple of packet size ({PACKET_SIZE} bytes)."
        )

    packets = []
    for offset in range(0, len(data), PACKET_SIZE):
        raw = data[offset : offset + PACKET_SIZE]
        timestamp_sec, raw_value, wave_value, intensity = struct.unpack("<IhhH", raw)
        packets.append((timestamp_sec, raw_value, wave_value, intensity))

    if not packets:
        raise ValueError("No packets found in the binary file.")

    timestamps = [p[0] for p in packets]
    intensities = [p[3] for p in packets]

    start_time = timestamps[0]
    elapsed_seconds = [(t - start_time) for t in timestamps]
    return elapsed_seconds, intensities


def plot_binary_file(input_path: str, output_path: str | None = None, show: bool = True):
    path = Path(input_path)
    elapsed, intensity = read_packets(path)

    plt.figure(figsize=(12, 4))
    plt.plot(elapsed, intensity, linewidth=1, color="tab:blue")
    plt.xlabel("Time (s)")
    plt.ylabel("Intensity")
    plt.title(f"Piezo intensity from {path.name}")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    if output_path:
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(out, dpi=200)
        print(f"Saved plot to {out}")

    if show:
        plt.show()


def main():
    parser = argparse.ArgumentParser(description="Plot binary piezo data from SD card export")
    parser.add_argument("input", nargs="?", default="data_record.bin", help="Path to the binary file")
    parser.add_argument("-o", "--output", help="Optional output image file (for example plot.png)")
    parser.add_argument("--no-show", action="store_true", help="Do not display the plot window")
    args = parser.parse_args()

    plot_binary_file(args.input, args.output, show=not args.no_show)


if __name__ == "__main__":
    main()
