"""This is nester.py module,provide a function named
   print_lol which to print a list that include 
   another list also"""
  
def print_lol(the_list):
    """The function use a parameter named the_list to print,
    one item one line"""
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item)
        else:
            print(each_item)
