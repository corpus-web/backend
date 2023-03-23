def check_file_suffix(file_obj, type_list):
    try:
        file_suffix = file_obj.name.split(".")[-1]
    except Exception:
        return False
    else:
        if file_suffix not in type_list:
            return False
        return True
