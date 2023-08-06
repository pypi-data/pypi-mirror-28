"""Nester module contains the print_lol function, which breaks down and prints all individual items in a list, one at a time""" 

def print_lol(the_list, indent=0, tabs=0):
    """Print_lol takes a positional argument the_list, checks if each item from that is a
        list itself recursively and prints the item if it is not.
        It also uses the secondary argument Tabs to reference the amount of indent printed for each sub-list (use 0 for no indent)
        Lastly, the indent function can be turned off by having indent = 0"""
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent, tabs+1)            
        else:
            if indent:
                for i in range(tabs):
                    print('\t', end='')
            print(each_item)
            
