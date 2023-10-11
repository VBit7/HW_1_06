import argparse
import re
from pathlib import Path
from shutil import copyfile

folder_to_sort = Path(r'C:\TEMP\SORT')
output = Path(r'C:\TEMP\SORT\NEW')

FILE_CATEGORIES = {'images': ['jpeg', 'png', 'jpg', 'svg'],
                   'documents': ['doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx'],
                   'audio': ['mp3', 'ogg', 'wav', 'amr'],
                   'video': ['avi', 'mp4', 'mov', 'mkv'],
                   'archives': ['zip', 'gz', 'tar']
                  }

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

TRANS = {}


def translate(name):
    return name.translate(TRANS)


def replace_non_alphanumeric(input_string):
    # Визначимо регулярний вираз, який збереже тільки латинські літери та цифри
    pattern = re.compile(r'[^a-zA-Z0-9 ]+')
    
    # Використовуємо регулярний вираз для заміни неналежних символів на '_'
    result = pattern.sub('_', input_string)
    
    return result


def read_folder(path: Path):
    for element in path.iterdir():
        if element.is_dir():
            read_folder(element)
        else:
            # ext = element.suffix
            # new_path = output / ext
            # new_path.mkdir(exist_ok=True, parents=True)
            # copyfile(element, new_path / element.name)
            print(element)
            print(replace_non_alphanumeric(translate(element.name)))


# parser = argparse.ArgumentParser(description='Sorting directory')
# parser.add_argument('--source', '-s', required=True, help='Source folder')
# parser.add_argument('--output', '-o', default='destination', help='Output folder')

# args = vars(parser.parse_args())
# source = args.get('source')
# output = args.get('output')

# print(source)
# print(output)


for c, t in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = t
    TRANS[ord(c.upper())] = t.upper()

print(translate("Дмитро Короб"))  # Dmitro Korob

read_folder(folder_to_sort)
    
input_string = "Hello, World! 123"
output_string = replace_non_alphanumeric(input_string)
print(output_string)  # Виведе: "Hello_World_123"
