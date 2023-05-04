def check_file_suffix(file_obj, type_list):
    if "." not in file_obj.name:
        return False
    file_suffix = file_obj.name.split(".")[-1].lower()
    return file_suffix in type_list
