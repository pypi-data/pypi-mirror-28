"""Nester module contains the print_lol function, which breaks down and prints all individual items in a list, one at a time""" 

def print_lol(the_list):
    """Print_lol takes a positional argument the_list, checks if each item from that is a
        list itself recursively and prints the item if it is not"""
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item)
        else:
            print(each_item)
