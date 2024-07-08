def copy(old_data, new_data, key, skip_value=None):
    if key in old_data:
        if skip_value is not None and old_data[key] == skip_value:
            return
        
        new_data[key] = old_data[key]

def update_soil(data):
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
            'block': '#' + old_variant['object'] if old_variant['useTag'] else old_variant['object']
        }
        if 'stateDefinition' in old_variant and old_variant['stateDefinition'] != []:
            new_variant['states'] = old_variant['stateDefinition']
        
        new_variants.append(new_variant)
    new_data['variants'] = new_variants

    copy(data, new_data, 'humidity')
    copy(data, new_data, 'acidity')
    copy(data, new_data, 'nutrients')
    copy(data, new_data, 'growth_modifier')

    return new_data