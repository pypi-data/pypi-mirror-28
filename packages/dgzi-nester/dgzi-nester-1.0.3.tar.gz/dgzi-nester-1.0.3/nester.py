"""
递归函数打印多维数组
"""
def print_names (names, level=0) :
    for each_name in names :
        if isinstance(each_name, list):
            print_names(each_name, level+1)
        else:
            for tab_stop in range(level):
                print("\t", end='')
            print(each_name)
