import re
import sys
import shutil
from pathlib import Path
import scandir

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

TRANS = {}

for c, t in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = t
    TRANS[ord(c.upper())] = t.upper()


def normalize(file_path, destination_dir):
    base_name, extension = file_path.name.rsplit('.', 1)
    normal_name = re.sub(r'\W', '_', base_name.translate(TRANS))
    normalize_name = f'{normal_name}.{extension}'
    counter = 1

    while (destination_dir / normalize_name).exists():
        new_name = f"{normal_name}_{counter}.{extension}"
        normalize_name = file_path.with_name(new_name)
        counter += 1

    return destination_dir / normalize_name


def move_files(base_dir: str, file_dict: dict):
    base_dir = Path(base_dir).resolve()

    for directory, files in file_dict.items():
        destination_dir = base_dir / Path(directory)

        try:
            if not destination_dir.is_dir():
                destination_dir.mkdir(exist_ok=True, parents=True)

            for file in files:
                destination_path = destination_dir / file.name
                destination_path = normalize(destination_path, destination_dir)
                shutil.move(str(file), str(destination_path))
        except FileNotFoundError as e:
            print(f"Error: {e} - File not found.")
            return 1
        except FileExistsError as e:
            print(f"Error: {e} - A file with the same name already exists in the destination directory.")
            return 2
        except PermissionError as e:
            print(f"Error: {e} - Insufficient permissions to write to the destination directory.")
            return 3

    return -1


def remove_dir(dir_list: list):
    sorted_dir_list = sorted(dir_list, key=lambda x: len(str(x)), reverse=True)
    
    for dir in sorted_dir_list:
        try:
            shutil.rmtree(dir)
        except FileNotFoundError:
            print(f"Error: Directory {dir} not found.")
            return 1
        except OSError as e:
            print(f"Error: {e} - Failed to delete the directory {dir}.")
            return 2

    return -1


def unpack_dir(dir_path):
    try:
        for item in dir_path.iterdir():
            
            if item.is_file():
                base_name, extension = item.name.rsplit('.', 1)

                if extension in scandir.FILE_CATEGORIES['archives']:
                    destination_dir = dir_path / base_name
                    
                    if not destination_dir.is_dir():
                        destination_dir.mkdir(exist_ok=True, parents=True)

                        try:
                            shutil.unpack_archive(str(item.absolute()), str(destination_dir.absolute()))
                            # os.remove(str(item.absolute()))   # to delete the file, if necessary
                        except (shutil.ReadError, PermissionError, FileNotFoundError) as e:
                            print(f"Error: {e} - Failed to unpack the archive {item}.")
                            return 3
                    
    except FileNotFoundError as e:
        print(f"Error: {e} - File not found.")
        return 1
    except PermissionError as e:
        print(f"Error: {e} - Permission denied to create a directory.")
        return 2

    return -1


if __name__ == '__main__':

    # directory_path = Path(sys.argv[1])    
    directory_path = 'c:\\Temp'
    

    # categorized_files, subdir_list = scandir.file_lister(directory_path)

    # if move_files(directory_path, categorized_files) == -1:
    #     remove_dir(subdir_list)

    unpack_dir(Path(directory_path) / 'archives')
