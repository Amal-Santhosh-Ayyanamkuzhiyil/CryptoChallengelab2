import struct
from pathlib import Path

inpath = Path("Input/aes.bmp.enc")   # input file
outpath = Path("results/aes_fixed_640x480.bmp")
data = inpath.read_bytes()

filesz = len(data)
print("Input file size:", filesz)

# Build BMP header (14 bytes)
bmp_header = b'BM' + struct.pack('<I', filesz) + (0).to_bytes(4,'little') + struct.pack('<I', 54)

# Build BITMAPINFOHEADER (40 bytes) for 640x480, 24-bit
biSize = 40
width = 640
height = 480
planes = 1
bit_count = 24
compression = 0
image_size = width * height * 3
xppm = 2835
yppm = 2835
clr_used = 0
clr_important = 0
dib = struct.pack('<IiiHHIIiiII', biSize, width, height, planes, bit_count, compression,
                  image_size, xppm, yppm, clr_used, clr_important)

# Write repaired BMP (header + dib + remaining pixel data)
new_bytes = bmp_header + dib + data[54:]
outpath.write_bytes(new_bytes)
print("Wrote", outpath, "size:", outpath.stat().st_size)