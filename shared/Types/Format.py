class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def print_title(message: str = 'Dummy Title') -> None:
   '''
   This function prints a title message to the console.

   :param message: The message to be printed on the console.
   '''
   
   print(f'{color.BOLD} {message} {color.END} \n')

def print_error(message: str = 'Dummy Error', error: object = None, tabs: int = 0) -> None:
   '''
   This function prints an error message to the console as RuntimeError.

   :param message: The message to be printed on the console.
   :param error: The error object which has been thrown.
   :param tabs: Number of tab characters at the beginning of the message.
   '''
   start = '\t' * tabs
   raise RuntimeError(f'{start} {color.RED} {message} {color.END} \n', error)

def print_information(message: str = 'Dummy Information', tabs: int = 0) -> None:
   '''
   This function prints an information message to the console.

   :param message: The message to be printed on the console.
   :param tabs: Number of tab characters at the beginning of the message.
   '''
   start = '\t' * tabs
   print(f'{start} {color.RED} {message} {color.END} \n')

def print_warning(message: str = 'Dummy Warning', tabs: int = 0) -> None:
   '''
   This function prints a warning message to the console.

   :param message: The message to be printed on the console.
   :param tabs: Number of tab characters at the beginning of the message.
   '''
   start = '\t' * tabs
   print(f'{start} {color.YELLOW} {message} {color.END} \n')