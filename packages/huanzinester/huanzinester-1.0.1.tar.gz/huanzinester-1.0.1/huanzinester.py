"""递归打印列表"""


def print_lol(the_list):
        # the_list 列表（或者嵌套列表），递归打印所有项.
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item)
        else:
            print(each_item)
