import struct
from pathlib import Path

inpath = Path("Input/aes.bmp.enc")   # input file
print(f"[1] Reading input file from: {inpath}")

outpath = Path("results/aes_fixed_640x480.bmp")
data = inpath.read_bytes()

filesz = len(data)
print(f"[2] Input file size: {filesz} bytes")

# Build BMP header (14 bytes)
print("[3] Building BMP header...")
bmp_header = b'BM' + struct.pack('<I', filesz) + (0).to_bytes(4,'little') + struct.pack('<I', 54)
print(f"    BMP Header length: {len(bmp_header)} bytes")

print("[4] Building BIT MAP INFO HEADER...")
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

print(f"    Image dimensions: {width}x{height}")
print(f"    Bit depth: {bit_count}-bit")
print(f"    Estimated pixel data size: {image_size} bytes")

dib = struct.pack('<IiiHHIIiiII', biSize, width, height, planes, bit_count, compression,
                  image_size, xppm, yppm, clr_used, clr_important)

print(f"    DIB Header length: {len(dib)} bytes")

print("[5] Combining BMP header, DIB header, and pixel data...")

new_bytes = bmp_header + dib + data[54:]

print(f"    Combined total size: {len(new_bytes)} bytes")

outpath.write_bytes(new_bytes)
print(f"[6] Writing repaired BMP file to: {outpath}")

output_size = outpath.stat().st_size
print(f"[7] Successfully wrote {outpath.name} ({output_size} bytes)")
print("✅ BMP file repair completed successfully!")