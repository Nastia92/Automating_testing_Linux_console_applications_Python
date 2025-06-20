import subprocess

def run_command_and_check_output(command: str, text: str) -> bool:
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0 and text in result.stdout
    except Exception as e:
        print(f"Ошибка: {e}")
        return False


if __name__ == "__main__":
    print(run_command_and_check_output("echo Hello, world!", "Hello"), run_command_and_check_output("ls /nonexistent", "No such file"))