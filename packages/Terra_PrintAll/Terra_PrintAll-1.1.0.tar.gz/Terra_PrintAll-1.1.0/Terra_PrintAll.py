""""This is the print_all function """
def print_all(one_list,level):
    for each_item in one_list:
        if isinstance(each_item,list):
             print_all(each_item,level+1)
        else:
            for count in range(level):
                     print("\t",end="")
            print(each_item)

            
