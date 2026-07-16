#!/usr/bin/env python3
"""
Read NIP1 binary data files written by the device.
Format:
 - 4 bytes: ASCII magic 'NIP1'
 - 4 bytes: uint32 little-endian startMicros
 - repeated records of struct '<IhhH' (uint32, int16, int16, uint16)

Usage:
 python read_binary.py data_record.bin --out data.csv --absolute
"""
import struct
import argparse
import csv
import os
import sys

RECORD_FMT = '<IhhH'
RECORD_SIZE = struct.calcsize(RECORD_FMT)
MAGIC = b'NIP1'


def parse(path, out_path=None, absolute=False, limit=None):
    with open(path, 'rb') as f:
        header = f.read(8)
        if len(header) < 8:
            raise SystemExit('File too small or truncated')
        magic = header[:4]
        if magic != MAGIC:
            raise SystemExit(f'Invalid magic: {magic!r}')
        start_micros = struct.unpack('<I', header[4:8])[0]

        if out_path:
            out_f = open(out_path, 'w', newline='')
            writer = csv.writer(out_f)
            writer.writerow(['timestamp_us', 'rawValue', 'waveValue', 'intensity'])
        else:
            writer = None

        count = 0
        while True:
            if limit is not None and count >= limit:
                break
            chunk = f.read(RECORD_SIZE)
            if not chunk:
                break
            if len(chunk) != RECORD_SIZE:
                print('Warning: truncated record encountered; stopping', file=sys.stderr)
                break
            ts, raw, wave, intensity = struct.unpack(RECORD_FMT, chunk)
            ts_out = ts + start_micros if absolute else ts
            if writer:
                writer.writerow([ts_out, raw, wave, intensity])
            else:
                print(f'{count}\t{ts_out}\t{raw}\t{wave}\t{intensity}')
            count += 1

        if out_path:
            out_f.close()

    print(f'Read {count} records. start_micros={start_micros}')


if __name__ == '__main__':
    p = argparse.ArgumentParser(description='Read NIP1 binary data file')
    p.add_argument('input', nargs='?', default='data_record.bin', help='Binary input file')
    p.add_argument('--out', '-o', dest='out', help='Optional CSV output path')
    p.add_argument('--absolute', action='store_true', help='Add startMicros to timestamps (absolute)')
    p.add_argument('--limit', type=int, default=None, help='Stop after N records')
    args = p.parse_args()

    if not os.path.exists(args.input):
        raise SystemExit(f'Input file not found: {args.input}')

    parse(args.input, out_path=args.out, absolute=args.absolute, limit=args.limit)
