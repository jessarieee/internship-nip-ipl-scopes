with open("data_record.bin", "rb") as f:
    data = f.read(32)

print(data)
print(data.hex())