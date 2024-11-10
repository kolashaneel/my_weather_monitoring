def extract_fields_from_json(d, parent_key='', result_dict=None):
    # Initialize the result dictionary if it's not passed
    if result_dict is None:
        result_dict = {}

    if isinstance(d, dict):  # If the value is a dictionary
        for key, value in d.items():
            new_key = f"{parent_key}.{key}" if parent_key else key  # Append the parent key for nesting
            # If the value is another dictionary or list, recursively call the function
            if isinstance(value, (dict, list)):
                extract_fields_from_json(value, new_key, result_dict)
            else:
                result_dict[new_key] = value  # Store the key-value pair in the result dictionary
    
    elif isinstance(d, list):  # If the value is a list, iterate through the list
        for index, item in enumerate(d):
            new_key = f"{parent_key}[{index}]"  # Use index for lists
            extract_fields_from_json(item, new_key, result_dict)

    return result_dict