import pytest
import time
import os
import subprocess

CONFIG_FILE = "config.txt"
STAT_FILE = "stat.txt"

def read_config():
    if not os.path.exists(CONFIG_FILE):
        return "-", "-", "zip"
    with open(CONFIG_FILE) as f:
        lines = f.read().strip().splitlines()
        if len(lines) >= 2:
            num_files, file_size = lines[0].strip(), lines[1].strip()
        else:
            num_files, file_size = "-", "-"
        archive_type = lines[2].strip() if len(lines) >= 3 else "zip"
        return num_files, file_size, archive_type

@pytest.fixture(autouse=True)
def write_stat_after_test():
    yield  

    num_files, file_size, _ = read_config()
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    try:
        with open("/proc/loadavg") as f:
            loadavg = f.read().strip()
    except FileNotFoundError:
        loadavg = "No /proc/loadavg (not Linux?)"

    line = f"{current_time}, {num_files}, {file_size}, {loadavg}\n"
    with open(STAT_FILE, "a") as f:
        f.write(line)


def test_7z_archive_type():
    _, _, archive_type = read_config()

    path_to_7z = r"C:\Program Files (x86)\OpenBox\LibreOffice-x64\7z.exe"

    archive_name = f"dummy.{archive_type}"

    if not os.path.exists(archive_name):
        subprocess.run(
            [path_to_7z, 'a', f'-t{archive_type}', archive_name, 'tests_with_stat.py'],
            capture_output=True,
            text=True
        )

    result = subprocess.run(
        [path_to_7z, 't', f'-t{archive_type}', archive_name],
        capture_output=True,
        text=True
    )

    print(result.stdout)
    print(result.stderr)

    assert "Everything is Ok" in result.stdout or result.returncode == 0