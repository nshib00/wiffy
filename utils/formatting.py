def format_to_win_path_string(string: str) -> str:
    forbidden_syms = '/:*?»"<>|!'
    for sym in forbidden_syms:
        if sym in string:
            string = string.replace(sym, "")
    filename_parts = string.split(".")
    if len(filename_parts) > 2:
        string = string.replace(".", "", len(filename_parts) - 2)
    return string
