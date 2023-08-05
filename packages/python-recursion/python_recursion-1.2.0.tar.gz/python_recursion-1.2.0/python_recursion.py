"""这是nester.py模块,提供了一个名为print_lol()的函数,这个函数的作用是打印列
表，其中有可能包含（也可能不包含）嵌套列表。"""
def print_lol(the_list,level=0):
        """这个函数有一个位置参数,名为 'the_list',
        这可以是任何python列表(也可以是包含嵌套列表的列表),
        另一个缩进参数,名为level,用于控制缩进次数（在屏幕上显示一行数据时需要加多少个制表符tab）
        所指定的列表中的每一个数据项会(递归地)输出到屏幕上，每个数据项各占一行。"""
        for each_item in the_list:
            if isinstance(each_item,list):
                print_lol(each_item,level+1)
            else:
                for tab_stop in range(level):
                    print("\t",end='')
                print(each_item)
