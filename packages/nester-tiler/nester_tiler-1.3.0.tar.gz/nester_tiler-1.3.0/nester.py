"""This is nester.py module,provide a function named
   print_lol which to print a list that include 
   another list also"""
  
def print_lol(the_list, indent=False, level=0, fn=sys.stdout):
    """The function use a parameter named the_list to print,
    one item one line"""
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item, indent, level+1,fn)
        else:
            if indent:
                for step in range(level):
                    print("\t", end='',file=fn)
            print(each_item, file=fn)
