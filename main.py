import re
from pathlib import Path
import shutil
import sys
from scandir import file_lister
# from normalize import normalize

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
    # print(base_directory)
    for directory, files in file_dict.items():
        destination_dir = base_dir / Path(directory)
        # destination_dir = Path(directory)
        # print(destination_dir.resolve())
        
        if not destination_dir.is_dir():
            destination_dir.mkdir(exist_ok=True, parents=True)

        for file in files:
            destination_path = destination_dir / file.name
            destination_path = normalize(destination_path, destination_dir)
            # print(destination_path)
            # shutil.move(str(source_path), str(destination_path))
            # shutil.move(str(file), str(destination_path))
            print(str(file))
            print(str(destination_path))
            # print('Error')



        
    #     print(destination_dir)


    #     print(files)


    





# def handle_media(file_name: Path, target_folder: Path):
#     target_folder.mkdir(exist_ok=True, parents=True)
#     file_name.replace(target_folder / normalize(file_name.name))


# def handle_archive(file_name: Path, target_folder: Path):
#     target_folder.mkdir(exist_ok=True, parents=True)
#     folder_for_file = target_folder / normalize(file_name.name.replace(file_name.suffix, ''))
#     folder_for_file.mkdir(exist_ok=True, parents=True)
#     try:
#         shutil.unpack_archive(str(file_name.absolute()), str(folder_for_file.absolute()))
#     except shutil.ReadError:
#         folder_for_file.rmdir()
#         return
#     file_name.unlink()


# def main(folder: Path):
#     file_parser.scan(folder)
#     for file in file_parser.JPEG_IMAGES:
#         handle_media(file, folder / 'images' / 'JPEG')
#     for file in file_parser.JPG_IMAGES:
#         handle_media(file, folder / 'images' / 'JPG')
#     for file in file_parser.MY_OTHER:
#         handle_media(file, folder / 'MY_OTHER')
#     for file in file_parser.ARCHIVES:
#         handle_archive(file, folder / 'ARCHIVES')

#     for folder in file_parser.FOLDERS[::-1]:
#         try:
#             folder.rmdir()
#         except OSError:
#             print('Error during remove folder: {folder}')


if __name__ == '__main__':

    # directory_path = Path(sys.argv[1])    
    # directory_path = Path('c:\\Temp')
    directory_path = 'c:\\Temp'
    
    # categorized_files, subdir_list = file_lister(directory_path.resolve())
    categorized_files, subdir_list = file_lister(directory_path)

    move_files(directory_path, categorized_files)


    # folder_process = Path(r'c:\Temp')
    # main(folder_process.resolve())