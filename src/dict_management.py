
def merge_dicts(dicts_list: list[dict]):
    """takes a list of dicts and combine their keys value. 
    keys must be in the same order. only work in simple dicts
    (when the keys havent a list or another dict as the value)"""
    first_dict = dicts_list[0]
    first_dict_keys = list(first_dict.keys())
    # verify that all dicts have the same keys
    for dicti in dicts_list:
        if list(dicti.keys()) != first_dict_keys:
            raise Exception('the keys of some dict is different to the others')

    # here will be stored the value of all keys in all dicts, avoiding duplicates
    all_keys_values = []

    for key in first_dict_keys:
        # what will be apended to all_keys_values is a set, to avoid duplicates
        current_key_values = set()
        for dicti in dicts_list:
            current_key_values.add(dicti.get(key))
        all_keys_values.append(current_key_values)

    merged_dict: dict = {}

    # here, the values of all keys in all dicts is joined into 
    # one value, and assigning it to merged dict
    for i, key in enumerate( first_dict_keys ):
        merged_dict.update({
            key: ','.join(all_keys_values[i])
        })

    return merged_dict


def get_dicts_from_dicts_list(dicts_list: list[dict], condition_dict: dict, can_be_several: bool = False) -> list[dict]:
    found_dicts = []
    for dict in dicts_list:
        condition_keys = list(condition_dict.keys())



        for key in condition_keys:
            if dict.get(key) != condition_dict.get(key):
                break
        else:
            found_dicts.append(dict)
            if not can_be_several:
                return found_dicts

    return found_dicts
