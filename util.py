def move_list_contents(from_list, to_list):
    to_list.extend(from_list)
    from_list[:] = []