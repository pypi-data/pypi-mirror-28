"""nester__UeRS.py: processa listas aninhadas"""
def print_lol(the_list, level=-1):
  """Imprime os itens de uma lista na tela, inclusive os itens aninhados.
  the_list: lista a ser impressa de forma recursiva."""
  for each_item in the_list:
    if isinstance(each_item, list):
      print_lol(each_item, level+1)
    else:
      for num in range(level):
        print("\t", end ='')
        
      print(each_item)
