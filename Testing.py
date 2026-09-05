import requests
from colorama import Fore, Style, init

init(autoreset=True)

print(Fore.GREEN + "Requests version:", requests.__version__)
print(Fore.BLUE + "Colorama is working!")