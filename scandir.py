# import os
# import shutil

from pathlib import Path

FILE_CATEGORIES = {'images': ['jpeg', 'png', 'jpg', 'svg'],
                   'documents': ['doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx'],
                   'audio': ['mp3', 'ogg', 'wav', 'amr'],
                   'video': ['avi', 'mp4', 'mov', 'mkv'],
                   'archives': ['zip', 'gz', 'tar'],
                    'other': []
                  }

# Шлях до директорії, яку потрібно просканувати
directory_path = 'c:\\Temp'

# Створення словника для файлів
categorized_files = {category: [] for category in FILE_CATEGORIES}


def scan_directory(directory_path: str) -> list:

    file_list = []

    for item in Path(directory_path).iterdir():
        if item.is_file():
            file_list.append(item)
        elif item.name not in FILE_CATEGORIES:
            file_list.extend(scan_directory(item))

    return file_list


def file_lister(directory_path: str) -> dict:
    # for item in Path(directory_path).iterdir():
    #     if item.is_dir():
    #         if item.name not in FILE_CATEGORIES:
    #             file_lister(item)
    #         continue
    file_list = scan_directory(directory_path)

    for item in file_list:
        # item = Path(item)
        # print(item.suffix)
        # print(Path(item).name.suffix)
        
        file_extension = Path(item).suffix[1:].lower()
        # print(file_extension)
        category_found = False

        for category, extensions in FILE_CATEGORIES.items():
            if file_extension in extensions:
                categorized_files[category].append(item)
                category_found = True
                break

        if not category_found:
            categorized_files['other'].append(item)

    return None


# Просканувати директорію
# for root, dirs, files in os.walk(directory_path):
#     for file in files:
#         file_extension = file.split('.')[-1].lower()
#         for category, extensions in FILE_CATEGORIES.items():
#             if file_extension in extensions:
#                 source_path = os.path.join(root, file)
#                 destination_path = os.path.join(category, file)
#                 categorized_files[category].append(file)
                # Копіювати файл у відповідну категорію
                # shutil.copy(source_path, destination_path)

# Вивести відсортовані файли в кожній категорії
# for category, files in categorized_files.items():
    # files.sort()  # Сортування файлів за іменем
    # print(f'{category}: {files}')




file_lister(directory_path)

for category, files in categorized_files.items():
    print(f'{category}: {files}')

# print(scan_directory(Path(directory_path)))