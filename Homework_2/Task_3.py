import subprocess
import string
import os
import shutil

def run_command_and_check_output(command: str, text: str, word_mode: bool = False) -> bool:
    """
    Выполняет команду и проверяет, есть ли текст в выводе.
    В режиме word_mode удаляет пунктуацию и ищет точное совпадение слова.
    """
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


ARCHIVE_NAME = "test_archive.tar"
EXTRACT_DIR = "extracted_files"

def create_test_archive():
    """Создаем тестовый архив с файлами."""
    os.makedirs("test_dir", exist_ok=True)
    with open("test_dir/file1.txt", "w") as f:
        f.write("Hello file1")
    with open("test_dir/file2.txt", "w") as f:
        f.write("Hello file2")

    subprocess.run(f"tar -cf {ARCHIVE_NAME} -C test_dir .", shell=True, check=True)
    shutil.rmtree("test_dir")

def test_list_files_in_archive():
    """Тестируем команду 'l' — список файлов в архиве."""
    return run_command_and_check_output(f"tar -tf {ARCHIVE_NAME}", "file1.txt")

def test_extract_files():
    """Тестируем команду 'x' — разархивирование с путями."""
    if os.path.exists(EXTRACT_DIR):
        shutil.rmtree(EXTRACT_DIR)
    os.makedirs(EXTRACT_DIR, exist_ok=True)

    result = subprocess.run(f"tar -xf {ARCHIVE_NAME} -C {EXTRACT_DIR}", shell=True)
    if result.returncode != 0:
        return False

    file1_path = os.path.join(EXTRACT_DIR, "file1.txt")
    file2_path = os.path.join(EXTRACT_DIR, "file2.txt")
    return os.path.isfile(file1_path) and os.path.isfile(file2_path)

if __name__ == "__main__":
    create_test_archive()

    print("Тест списка файлов (l):", test_list_files_in_archive())  # True
    print("Тест распаковки (x):", test_extract_files())           # True

    if os.path.exists(ARCHIVE_NAME):
        os.remove(ARCHIVE_NAME)
    if os.path.exists(EXTRACT_DIR):
        shutil.rmtree(EXTRACT_DIR)