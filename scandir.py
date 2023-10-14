from pathlib import Path
from collections import OrderedDict

FILE_CATEGORIES = OrderedDict([
    ('images', ['jpeg', 'png', 'jpg', 'svg']),
    ('documents', ['doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx']),
    ('audio', ['mp3', 'ogg', 'wav', 'amr']),
    ('video', ['avi', 'mp4', 'mov', 'mkv']),
    ('archives', ['zip', 'gz', 'tar']),
    ('other', [])
])


def scan_directory(directory_path: str) -> list:

    file_list = []

    for item in Path(directory_path).iterdir():
        if item.is_file():
            file_list.append(item)
        elif item.name not in FILE_CATEGORIES:
            file_list.extend(scan_directory(item))

    return file_list


def file_lister(directory_path: str) -> dict:

    file_list = scan_directory(directory_path)
    categorized_files = {category: [] for category in FILE_CATEGORIES}
    last_category, extensions = FILE_CATEGORIES.popitem(last=True)

    for item in file_list:
        file_extension = Path(item).suffix[1:].lower()
        category_found = False

        for category, extensions in FILE_CATEGORIES.items():
            if file_extension in extensions:
                categorized_files[category].append(item)
                category_found = True
                break

        if not category_found:
            categorized_files[last_category].append(item)

    return categorized_files


if __name__ == '__main__':
    
    directory_path = 'c:\\Temp'
    
    categorized_files = file_lister(directory_path)

    for category, files in categorized_files.items():
        print(f'{category}: {files}')
