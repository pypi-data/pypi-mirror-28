"""递归打印列表"""

import sys


def print_lol(the_list, indent=False, level=0, fh=sys.stdout):
        # the_list 列表（或者嵌套列表），递归打印所有项.
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent, level + 1, fh)
        else:
            if indent:
                for tab_stop in range(level):
                    print("\t", end='', file=fh)
            print(each_item, file=fh)
