from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter
from colorama import Fore
import difflib

class PrintInColor:

    @classmethod
    def message(self, color, action, string, **kwargs):
        bspaces = " "*(int((12-len(action))/2))
        espaces = " "*(12-len(bspaces)-len(action))
        print(getattr(Fore, color) + "[" + bspaces + action + espaces + "] " + string + Fore.RESET, **kwargs)

    @classmethod
    def code(self, string):
        print(highlight(string, PythonLexer(), TerminalFormatter()))



    @classmethod
    def diff(self, left, right, fromfile="Current", tofile="Revised"):
        for line in difflib.unified_diff(left.splitlines(),
                                         right.splitlines(),
                                         fromfile=fromfile,
                                         tofile=tofile,
                                         lineterm=''):
            print(color_line(line=line))
        print()

def color_line(line):
    if line.startswith('+'):
        line = Fore.GREEN + line + Fore.RESET
    elif line.startswith('-'):
        line = Fore.RED + line + Fore.RESET
    elif line.startswith('^'):
        line = Fore.BLUE + line + Fore.RESET
    elif line.startswith('@@'):
        line = Fore.YELLOW + line + Fore.RESET
    return " "*2 +line
