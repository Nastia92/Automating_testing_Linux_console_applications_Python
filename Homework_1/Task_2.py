import subprocess
import string

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


if __name__ == "__main__":
    print(run_command_and_check_output("echo Hello, world!", "Hello"))             
    print(run_command_and_check_output("echo Hello, world!", "Hello", word_mode=True))  
    print(run_command_and_check_output("echo Test,Python;Testing!", "Python", word_mode=True))  
    print(run_command_and_check_output("ls /nonexistent", "No such file", word_mode=True))     