import subprocess
import string
import binascii

def run_command_and_check_output(command: str, text: str, word_mode: bool = False) -> bool:
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            return False

        output = result.stdout

        if not word_mode:
            return text in output
        else:
            translator = str.maketrans('', '', string.punctuation)
            cleaned_output = output.translate(translator)
            words = cleaned_output.split()
            return text in words

    except Exception as e:
        print(f"Ошибка: {e}")
        return False


def python_crc32(filepath):
    
    with open(filepath, 'rb') as f:
        data = f.read()
    crc = binascii.crc32(data) & 0xffffffff
    return f"{crc:08x}"


def get_crc32_linux(filepath):
    
    result = subprocess.run(f"crc32 {filepath}", shell=True, capture_output=True, text=True)
    return result.stdout.strip()