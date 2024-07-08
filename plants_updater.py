def copy(old_data, new_data, key, skip_value=None):
    if key in old_data:
        if skip_value is not None and old_data[key] == skip_value:
            return
        
        new_data[key] = old_data[key]

def transform_products(old_data):
    new_products = []
    for product in old_data:
        new_product = {
            "item": '#' + product["object"] if product['useTag'] else product["object"],
            "min": product["min"],
            "max": product["max"],
            "chance": product["chance"],
            "required": product["required"]
        }

        copy(product, new_product, 'nbt', '')

        new_products.append(new_product)
    return new_products

def transform_seeds(old_data):
    new_seeds = []
    for old_seed in old_data['seed_items']:
        new_seed = {
            "item": '#' + old_seed["object"] if old_seed['useTag'] else old_seed["object"],
            "override_planting": old_seed["overridePlanting"],
        }

        copy(old_data, new_seed, 'grass_drop_chance')
        copy(old_data, new_seed, 'seed_drop_chance')
        copy(old_data, new_seed, 'seed_drop_bonus')
        
        new_seeds.append(new_seed)

    return new_seeds

def transform_soil(old_data):
    new_requirement = {
        'type': old_data['type'],
        'tolerance_factor': old_data['tolerance_factor'],
        'value': old_data['condition']
    }
    return new_requirement

def update_plant(data):
    new_data = {}

    if 'mods' in data:
        data['mods'] = [mod for mod in data['mods'] if mod not in ['agricraft', 'minecraft']]
        copy(data, new_data, 'mods')

    new_data['seeds'] = transform_seeds(data)

    copy(data, new_data, 'stages')

    new_data['harvest_stage'] = data['harvestStage']
    copy(data, new_data, 'growth_chance')
    copy(data, new_data, 'growth_bonus')
    copy(data, new_data, 'cloneable')
    copy(data, new_data, 'spread_chance')

    new_data['products'] = transform_products(data['products']['products'])
    new_data['clip_products'] = transform_products(data['clip_products']['products'])

    old_requirement = data['requirement']
    new_requirement = {}

    new_requirement['soil_humidity'] = transform_soil(old_requirement['soil_humidity'])
    new_requirement['soil_acidity'] = transform_soil(old_requirement['soil_acidity'])
    new_requirement['soil_nutrients'] = transform_soil(old_requirement['soil_nutrients'])
    copy(old_requirement, new_requirement, 'min_light')
    copy(old_requirement, new_requirement, 'max_light')
    copy(old_requirement, new_requirement, 'light_tolerance_factor')
    copy(old_requirement, new_requirement, 'biomes', {"values": [], "blacklist": True, "ignoreFromStrength": 11})
    copy(old_requirement, new_requirement, 'dimensions', {"values": [], "blacklist": True, "ignoreFromStrength": 11})
    copy(old_requirement, new_requirement, 'seasons', ["spring", "summer", "autumn", "winter"])

    block_conditions = []
    for old_condition in old_requirement['conditions']:
        new_condition = {}

        block = old_condition['object']
        new_condition['block'] = '#' + block if old_condition['useTag'] else block
        copy(old_condition, new_condition, 'nbt', '')
        if old_condition['stateDefinition'] != []:
            new_condition['states'] = old_condition['stateDefinition']
        copy(old_condition, new_condition, 'strength')
        copy(old_condition, new_condition, 'amount', 1)
        if not (old_condition['min_x'] == 0 and old_condition['min_y'] == -2 and old_condition['min_z'] == 0 and old_condition['max_x'] == 0 and old_condition['max_y'] == -2 and old_condition['max_z'] == 0):
            copy(old_condition, new_condition, 'min_x')
            copy(old_condition, new_condition, 'min_y')
            copy(old_condition, new_condition, 'min_z')
            copy(old_condition, new_condition, 'max_x')
            copy(old_condition, new_condition, 'max_y')
            copy(old_condition, new_condition, 'max_z')

        block_conditions.append(new_condition)
    if block_conditions != []:
        new_requirement['block_conditions'] = block_conditions

    if 'fluid' in old_requirement:
        fluid = old_requirement['fluid']['object']
        fluid_condition = {
            'fluid': '#' + fluid if old_requirement['fluid']['useTag'] else fluid
        }
        if 'stateDefinition' in old_requirement['fluid'] and old_requirement['fluid']['stateDefinition'] != []:
            fluid_condition['states'] = old_requirement['fluid']['stateDefinition']
        if fluid_condition['fluid'] != 'minecraft:empty':
            new_requirement['fluid_condition'] = fluid_condition

    new_data['requirement'] = new_requirement

    copy(data, new_data, 'callbacks', [])
    copy(data, new_data, 'particle_effects', [])

    return new_data