import os
import json

parents = {

}

def update_assets(namespace, data, id):
    namespace = namespace.replace('mod_', '')

    seed_path = os.path.join(namespace, 'models/seed/')
    if not os.path.exists(seed_path):
        os.makedirs(seed_path)

    crop_path = os.path.join(namespace, 'models/crop/')
    if not os.path.exists(crop_path):
        os.makedirs(crop_path)

    seed_model = {
        "parent": "minecraft:item/generated",
        "textures": {
            "layer0": f"{data['seed_texture']}"
        }
    }

    with open(os.path.join(seed_path, id), 'w', encoding='utf-8') as new_file:
        json.dump(seed_model, new_file, ensure_ascii=False, indent=2)

    # texture = data['texture']

    # for stage, texture in enumerate(texture['plant_textures']):
    #     crop_model = {
    #         "parent": "agricraft:crop/crop_hash",
    #         "textures": {
    #             "crop": texture[0]
    #         }
    #     }

    #     with open(os.path.join(crop_path, f'{id}_stage{stage}'), 'w', encoding='utf-8') as new_file:
    #         json.dump(crop_model, new_file, ensure_ascii=False, indent=2)



