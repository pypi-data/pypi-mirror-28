"""This is nester.py module,provide a function named
   print_lol which to print a list that include 
   another list also"""
  
def print_lol(the_list, level):
    """The function use a parameter named the_list to print,
    one item one line"""
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item, level+1)
        else:
            for step in range(level):
                print("\t", end='')
            print(each_item)
