def move_list_contents(from_list, to_list):
    to_list.extend(from_list)
    from_list[:] = []


def move_list_item(item, from_list, to_list):
    from_list.remove(item)
    to_list.append(item)
