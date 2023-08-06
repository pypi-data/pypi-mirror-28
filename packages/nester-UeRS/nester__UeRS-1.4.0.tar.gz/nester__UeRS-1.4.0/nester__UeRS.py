import sys

"""nester__UeRS.py: processa listas aninhadas"""
def print_lol(the_list, indent=False, level=0, out=sys.stdout):
  """Imprime os itens de uma lista na tela, inclusive os itens aninhados.
  the_list: lista a ser impressa de forma recursiva.
  indent: informa se havera indentamento ou nao.
  level: informa o nível de indentamento, se houver."""
  for each_item in the_list:
    if isinstance(each_item, list):
      print_lol(each_item, indent, level+1, out)
    else:
      if indent:
        for tab_stop in range(level):
          print("\t", end='', file=out)
        
      print(each_item, file=out)
