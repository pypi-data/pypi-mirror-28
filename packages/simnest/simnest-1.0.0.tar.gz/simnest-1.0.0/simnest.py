"""This is 'nester.py' model, it contains a bif called 'print_list', in order to print out embedded lists"""

def print_list(the_list):
  for each_item in the_list:
    if isinstance(each_item,list):
      print_list(each_item)
    else:
      print(each_item)


print('constructed')
