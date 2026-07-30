import sys
import os

if len(sys.argv) != 3:
    print("Usage: python png_to_cpp.py <input.png> <output.cpp>")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

if not os.path.exists(input_file):
    print(f"Error: {input_file} not found. Skipping image injection.")
    sys.exit(0)

try:
    with open(input_file, "rb") as f:
        data = f.read()

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write('#include "pch.h"\n')
        f.write('#include "./img.h"\n\n')
        f.write('const unsigned char g_img[] = {\n')
        
        for i in range(0, len(data), 20):
            chunk = data[i:i+20]
            hex_str = ", ".join(f"0x{b:02x}" for b in chunk)
            f.write("    " + hex_str + ",\n")
            
        f.write('};\n\n')
        f.write('const long long g_imgLen = sizeof(g_img);\n')

    print(f"Successfully converted {input_file} to {output_file}")
except Exception as e:
    print(f"Failed to convert image: {e}")
    sys.exit(1)
