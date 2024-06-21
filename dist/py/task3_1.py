import os
import shutil
import sys
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

# Глобальний лічильник файлів для демонстрації багатопотоковості
file_counter = 0
counter_lock = Lock()

def process_directory(source_directory, target_directory):           # функція для сотрування файлів
    global file_counter
    with ThreadPoolExecutor() as executor:
        for root, dirs, files in os.walk(source_directory):
            for file in files:
                source_file = os.path.join(root, file)
                file_extension = file.split('.')[-1] if '.' in file else 'no_extension'
                target_subdir = os.path.join(target_directory, file_extension)
                os.makedirs(target_subdir, exist_ok=True)
                target_file = os.path.join(target_subdir, file)
                executor.submit(copy_file, source_file, target_file)
                
def copy_file(source_file, target_file):                             # функція для підрахунку кількості файлів
    global file_counter
    shutil.copy2(source_file, target_file)
    with counter_lock:
        file_counter += 1
        print(f"Copied {file_counter} files", end="\r")               

def main():

    if len(sys.argv) < 2:
        print("Usage: python task3_1.py <source_dir> [<target_dir>]") # перевіряємо кількість наданих аргументів для старту роботи програми
        sys.exit(1)

    source_directory = sys.argv[1]
    target_directory = sys.argv[2] if len(sys.argv) > 2 else "dist"   # якщо другим аргументом не вказати директорію для результату, то створиться директорія 'dist' де будуть розміщені відсортовані файли

    if not os.path.exists(source_directory):
        print(f"Source directory '{source_directory}' does not exist.")  # перевірка на наявність директорії з файлами для обробки
        sys.exit(1)

    process_directory(source_directory, target_directory)
    print(f"\nFinished copying files from '{source_directory}' to '{target_directory}'")

if __name__ == "__main__":
    main()
