import os
import json
from pathlib import Path

from utils import ensure_path

def crop_hash(crop_textures):
    if len(crop_textures) == 1:
        return {
            "parent": "agricraft:crop/crop_hash",
            "textures": {
                "crop": crop_textures[0]
            }
        }
    else:
        return {
            "parent": "agricraft:crop/tall_crop_hash",
            "textures": {
                "crop": crop_textures[1],
                "crop_top": crop_textures[0]
            }
        }

def crop_gourd(crop_textures):
    return {
        "parent": "agricraft:crop/crop_gourd",
        "textures": {
            "crop": crop_textures[0],
            "gourd": crop_textures[1]
        }
    }

def crop_cross(crop_textures):
    if len(crop_textures) == 1:
        return {
            "parent": "agricraft:crop/crop_cross",
            "textures": {
                "crop": crop_textures[0]
            }
        }
    else:
        return {
            "parent": "agricraft:crop/tall_crop_cross",
            "textures": {
                "crop": crop_textures[1],
                "crop_top": crop_textures[0]
            }
        }

def crop_plus(crop_textures):
    if len(crop_textures) == 1:
        return {
            "parent": "agricraft:crop/crop_plus",
            "textures": {
                "crop": crop_textures[0]
            }
        }
    else:
        return {
            "parent": "agricraft:crop/tall_crop_plus",
            "textures": {
                "crop": crop_textures[1],
                "crop_top": crop_textures[0]
            }
        }

def crop_mysticalagriculture(crop_textures):
    if len(crop_textures) == 1:
        return {
            "parent": crop_textures[0]
        }
    else:
        return {
            "parent": crop_textures[0],
            "textures": {
                "flower": crop_textures[1]
            }
        }

def update_assets(namespace, data, id):
    id = id.replace('.json', '')

    seed_path = namespace / 'models' / 'seed'
    ensure_path(seed_path)

    crop_path = namespace / 'models' / 'crop'
    ensure_path(crop_path)

    seed_model = {
        "parent": "minecraft:item/generated",
        "textures": {
            "layer0": f"{data['seed_texture']}"
        }
    }

    with open(os.path.join(seed_path, f'{id}.json'), 'w', encoding='utf-8') as new_file:
        json.dump(seed_model, new_file, ensure_ascii=False, indent=2)

    texture = data['texture']
    render_type = texture['render_type']

    for stage, plant_textures in enumerate(texture['plant_textures']):
        match render_type, stage:
            case 'hash', _:
                crop_model = crop_hash(plant_textures)
            case 'gourd', 7:
                crop_model = crop_gourd(plant_textures)
            case 'gourd', _:
                crop_model = crop_hash(plant_textures)
            case 'plus', _:
                crop_model = crop_plus(plant_textures)
            case 'cross', _:
                crop_model = crop_cross(plant_textures)
            case 'mysticalagriculture', _:
                crop_model = crop_mysticalagriculture(plant_textures)
            case _, _:
                print(f'Skipping model {namespace}\{id}, model: {render_type}, stage: {stage}')
                continue

        with open(os.path.join(crop_path, f'{id}_stage{stage}.json'), 'w', encoding='utf-8') as new_file:
            json.dump(crop_model, new_file, ensure_ascii=False, indent=2)

def update_lang(path, data, namespaces):
    lang = {}

    for key in data:
        for namespace in namespaces:
            if namespace in key and key.startswith('agricraft.plant.'):
                split_key = key.split('.')

                match split_key[-1]:
                    case 'seed':
                        id = split_key[-2].replace(f'{namespace}_', '')
                        lang[f'seed.agricraft.{namespace}.{id}'] = data[key]
                    case 'desc':
                        id = split_key[-2].replace(f'{namespace}_', '')
                        lang[f'description.agricraft.{namespace}.{id}'] = data[key]
                    case 'name':
                        id = split_key[-2].replace(f'{namespace}_', '')
                        lang[f'plant.agricraft.{namespace}.{id}'] = data[key]
                    case _:
                        id = split_key[-1].replace(f'{namespace}_', '')
                        lang[f'seed.agricraft.{namespace}.{id}'] = data[key]

    ensure_path(path.parent)
    
    with open(path, 'w', encoding='utf-8') as lang_file:
        json.dump(lang, lang_file, ensure_ascii=False, indent=2)