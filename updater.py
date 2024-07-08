import os
import json
import shutil
from pathlib import Path

from utils import ensure_path

from mutations_updater import update_mutation
from plants_updater import update_plant
from soils_updater import update_soil
from fertilizers_updater import update_fertilizer
from assets_updater import update_assets, update_lang

# Constants
DATAPACK_DESCRIPTION = "Custom AgriCraft plants"
DATAPACK_FORMAT = 15
RESOURCEPACK_DESCRIPTION = DATAPACK_DESCRIPTION
RESOURCEPACK_FORMAT = 15
NEW_BASE_DIR = Path('new')
OLD_BASE_DIR = Path('old')
DATAPACK_DIR = NEW_BASE_DIR / 'datapack'
RESOURCEPACK_DIR = NEW_BASE_DIR / 'resourcepack'
LANG = 'en_us.json'

def add_mcmeta(path, pack_description, pack_format):
    pack = {
        "pack": {
        "description": pack_description,
        "pack_format": pack_format
        }
    }

    ensure_path(path.parent)

    with open(path, 'w', encoding='utf-8') as mcmeta_file:
        json.dump(pack, mcmeta_file, ensure_ascii=False, indent=2)

def update_data(dirname, data, new_filename, namespace):
    match dirname:
        case 'mutations':
            data = update_mutation(data)
            new_filename = new_filename.replace('_mutation', '')
        case 'plants':
            new_filename = new_filename.replace('_plant', '')
            update_assets(RESOURCEPACK_DIR / 'assets' / namespace, data, new_filename)
            data = update_plant(data)
        case 'soils':
            new_filename = new_filename.replace('_soil', '')
            data = update_soil(data)
        case 'fertilizers':
            new_filename = new_filename.replace('_fertilizer', '')
            data = update_fertilizer(data)
        case 'weeds':
            return None, None
        case _:
            return None, None
    
    return data, new_filename

def process_json_files():
    ensure_path(NEW_BASE_DIR)
    
    for dirpath, dirnames, _ in os.walk(OLD_BASE_DIR):
        dirpath = Path(dirpath)

        for dirname in dirnames:
            if dirpath == OLD_BASE_DIR:
                continue

            sub_old_path = dirpath / dirname
            sub_new_path = DATAPACK_DIR / 'data' / dirpath.name.replace('mod_', '') / 'agricraft' / dirname

            ensure_path(sub_new_path)
            
            for filename in os.listdir(sub_old_path):
                if filename.endswith('.json'):
                    old_file_path = sub_old_path / filename

                    with open(old_file_path, 'r', encoding='utf-8') as old_json:
                        data = json.load(old_json)

                    data, new_filename = update_data(dirname, data, filename, dirpath.name.replace('mod_', ''))
                    
                    if data is not None:
                        new_file_path = sub_new_path / new_filename

                        with open(new_file_path, 'w', encoding='utf-8') as new_json:
                            json.dump(data, new_json, ensure_ascii=False, indent=2)
                    else:
                        print(f'Skipping file {dirpath}\{dirname}\{filename}: directory name {dirname} is wrong or unsupported.')

    if Path.is_file(OLD_BASE_DIR / LANG):
        with open(OLD_BASE_DIR / LANG, 'r', encoding='utf-8') as old_lang:
            update_lang(RESOURCEPACK_DIR / 'assets' / 'agricraft' / 'lang' / LANG, json.load(old_lang))

if __name__ == '__main__':
    process_json_files()
    add_mcmeta(DATAPACK_DIR / 'pack.mcmeta', DATAPACK_DESCRIPTION, DATAPACK_FORMAT)
    shutil.make_archive(str(DATAPACK_DIR), 'zip', str(DATAPACK_DIR))

    add_mcmeta(RESOURCEPACK_DIR / 'pack.mcmeta', RESOURCEPACK_DESCRIPTION, RESOURCEPACK_FORMAT)
    shutil.make_archive(str(RESOURCEPACK_DIR), 'zip', str(RESOURCEPACK_DIR))