from __future__ import print_function
def pretty_list(l,ident=False,level=0):
    for each_list in range(len(l)):
        if isinstance(l[each_list],list):
            pretty_list(l[each_list],ident,level+each_list)
        else:
            if ident:
                for i in range(level):
                    print('\t',end='')
            print(l[each_list])


