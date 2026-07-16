import struct
import csv
from pathlib import Path

HEADER_FORMAT = "<4sI"
PACKET_FORMAT = "<IH"

HEADER_SIZE = struct.calcsize(HEADER_FORMAT)
PACKET_SIZE = struct.calcsize(PACKET_FORMAT)

BIN_FILE = Path("data_record.bin")
CSV_FILE = Path("data_record.csv")


def convert():

    if not BIN_FILE.exists():
        print("Binary file not found.")
        return

    with open(BIN_FILE, "rb") as f:

        header = f.read(HEADER_SIZE)

        if len(header) != HEADER_SIZE:
            raise RuntimeError("Invalid binary file.")

        magic, startMicros = struct.unpack(
            HEADER_FORMAT,
            header
        )

        if magic != b"NIP1":
            raise RuntimeError("Incorrect file format.")

        with open(CSV_FILE, "w", newline="") as csvfile:

            writer = csv.writer(csvfile)

            writer.writerow([
                "Sample",
                "Timestamp_us",
                "Intensity"
            ])

            sample = 0

            while True:

                data = f.read(PACKET_SIZE)

                if len(data) != PACKET_SIZE:
                    break

                timestamp, intensity = struct.unpack(
                    PACKET_FORMAT,
                    data
                )

                writer.writerow([
                    sample,
                    timestamp,
                    intensity
                ])

                sample += 1

    print("------------------------------------")
    print("Conversion Complete")
    print("------------------------------------")
    print("Magic Number :", magic.decode())
    print("Start Micros :", startMicros)
    print("Samples      :", sample)
    print("CSV File     :", CSV_FILE)
    print("------------------------------------")


if __name__ == "__main__":
    convert()