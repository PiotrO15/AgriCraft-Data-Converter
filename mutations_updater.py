def update_mutation(data):
    # Remove unnecessary keys
    keys_to_remove = ["path", "version", "json_documentation", "enabled"]
    for key in keys_to_remove:
        if key in data:
            del data[key]

    # Simplify plant names
    if 'child' in data:
        data['child'] = data['child'].replace('_plant', '')
    if 'parent1' in data:
        data['parent1'] = data['parent1'].replace('_plant', '')
    if 'parent2' in data:
        data['parent2'] = data['parent2'].replace('_plant', '')

    # Remove specific mods and the entire mods list if empty
    if 'mods' in data:
        data['mods'] = [mod for mod in data['mods'] if mod not in ['agricraft', 'minecraft']]
        del data['mods']

    # Remove conditions if it's empty
    if 'conditions' in data and not data['conditions']:
        del data['conditions']

    return data