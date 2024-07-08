import os
import json
import shutil
from pathlib import Path

from mutations_updater import update_mutation
from plants_updater import update_plant
from soils_updater import update_soil
from fertilizers_updater import update_fertilizer
from assets_updater import update_assets

# Constants
PACK_DESCRIPTION = "Custom AgriCraft plants"
PACK_FORMAT = 15
NEW_BASE_DIR = Path('new')
OLD_BASE_DIR = Path('old')
DATAPACK_DIR = NEW_BASE_DIR / 'datapack'
ASSETS_DIR = NEW_BASE_DIR / 'assets'

def ensure_path(path):
    path.mkdir(parents=True, exist_ok=True)

def add_datapack_mcmeta():
    pack = {
        "pack": {
        "description": PACK_DESCRIPTION,
        "pack_format": PACK_FORMAT
        }
    }

    pack_path = Path('new/datapack/pack.mcmeta')
    ensure_path(pack_path.parent)

    with open(pack_path, 'w', encoding='utf-8') as pack_mcmeta:
        json.dump(pack, pack_mcmeta, ensure_ascii=False, indent=2)

def update_data(dirname, data, new_filename, sub_new_path):
    match dirname:
        case 'mutations':
            data = update_mutation(data)
            new_filename = new_filename.replace('_mutation', '')
        case 'plants':
            new_filename = new_filename.replace('_plant', '')
            # update_assets(sub_new_path.replace(OLD_BASE_DIR, NEW_BASE_DIR + 'assets/'), data, new_filename)
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

                    data, new_filename = update_data(dirname, data, filename, dirpath)
                    
                    if data is not None:
                        new_file_path = sub_new_path / new_filename

                        with open(new_file_path, 'w', encoding='utf-8') as new_json:
                            json.dump(data, new_json, ensure_ascii=False, indent=2)
                    else:
                        print(f'Skipping file {dirpath}\{dirname}\{filename}')

if __name__ == '__main__':
    process_json_files()
    add_datapack_mcmeta()
    shutil.make_archive(str(DATAPACK_DIR), 'zip', str(DATAPACK_DIR))
