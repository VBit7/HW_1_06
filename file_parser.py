import sys
from pathlib import Path

JPEG_IMAGES = []
JPG_IMAGES = []
PNG_IMAGES = []
SVG_IMAGES = []
MP3_AUDIO = []
MY_OTHER = []
ARCHIVES = []

REGISTER_EXTENSION = {
    'JPEG': JPEG_IMAGES,
    'JPG': JPG_IMAGES,
    'PNG': PNG_IMAGES,
    'SVG': SVG_IMAGES,
    'MP3': MP3_AUDIO,
    'ZIP': ARCHIVES
}

FOLDERS = []
EXTENSIONS = set()
UNKNOWN = set()


def get_extension(name: str) -> str:
    return Path(name).suffix[1:].upper()


def scan(folder: Path):
    for item in folder.iterdir():
        # print(item)
        if item.is_dir():
            if item.name not in ('archives', 'video', 'audio', 'documents', 'images'):
                FOLDERS.append(item)
                scan(item)
            continue

        extension = get_extension(item.name)
        # print(f'extension: {extension}')
        full_name = folder / item.name
        # print(f'full_name: {full_name}')
        if not extension:
            MY_OTHER.append(full_name)
        else:
            try:
                ext_reg = REGISTER_EXTENSION[extension]
                ext_reg.append(full_name)
                # print(f'temp: {temp}')
                EXTENSIONS.add(extension)
            except KeyError:
                UNKNOWN.add(extension)
                MY_OTHER.append(full_name)


if __name__ == "__main__":
    # folder_process = sys.argv[1]
    folder_process = r'c:\temp'
    
    scan(Path(folder_process))
        
    print(JPG_IMAGES)
    print(MY_OTHER)

    print(EXTENSIONS)
    print(UNKNOWN)

