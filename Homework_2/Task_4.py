import subprocess
import binascii
import os

def python_crc32(filepath):
    with open(filepath, 'rb') as f:
        data = f.read()
    crc = binascii.crc32(data) & 0xffffffff
    return f"{crc:08x}"

def get_crc32_linux(filepath):
    result = subprocess.run(f"crc32 {filepath}", shell=True, capture_output=True, text=True)
    return result.stdout.strip()

def test_crc32_linux_vs_python():
    test_file = "test_file.txt"
    with open(test_file, "w") as f:
        f.write("Test content for crc32 hash")

    crc_python = python_crc32(test_file)
    crc_linux = get_crc32_linux(test_file)

    print(f"Python CRC32: {crc_python}")
    print(f"Linux  CRC32: {crc_linux}")

    os.remove(test_file)
    return crc_python == crc_linux

if __name__ == "__main__":
    if test_crc32_linux_vs_python():
        print("Тест совпадения CRC32 Python и Linux пройден")
    else:
        print("❗ CRC32 не совпадают")