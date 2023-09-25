from os import name, system, get_terminal_size


def clear_terminal():
  _ = system('cls') if name == 'nt' else system('clear')

def inspect_input(input):
  cancel = (input.upper() == 'X')
  return cancel