def copy(old_data, new_data, key, skip_value=None):
    if key in old_data:
        if skip_value is not None and old_data[key] == skip_value:
            return
        
        new_data[key] = old_data[key]

def update_fertilizer(data):
    new_data = {}

    if 'mods' in data:
        data['mods'] = [mod for mod in data['mods'] if mod not in ['agricraft', 'minecraft']]
        copy(data, new_data, 'mods')

    new_variants = []
    if 'varients' in data:
        data['variants'] = data['varients']
        del data['varients']

    for old_variant in data['variants']:
        new_variant = {
            'item': '#' + old_variant['object'] if old_variant['useTag'] else old_variant['object']
        }
        if 'stateDefinition' in old_variant and old_variant['stateDefinition'] != []:
            new_variant['states'] = old_variant['stateDefinition']
        
        new_variants.append(new_variant)
    new_data['variants'] = new_variants

    copy(data, new_data, 'trigger_mutation')
    copy(data, new_data, 'trigger_weeds')
    copy(data, new_data, 'potency')
    copy(data['effect'], new_data, 'reduce_growth')
    copy(data['effect'], new_data, 'kill_plant')
    copy(data['effect'], new_data, 'particles')

    neutral_on = []
    for plant in data['effect']['positively_affected']['plant_list']:
        neutral_on.append(plant.removeprefix('mod_').removesuffix('_plant'))
    new_data['neutral_on'] = neutral_on

    negative_on = []
    for plant in data['effect']['negatively_affected']['plant_list']:
        negative_on.append(plant.removeprefix('mod_').removesuffix('_plant'))
    new_data['negative_on'] = negative_on

    return new_data