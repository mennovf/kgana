import itertools, random, os
from rich.console import Console
from rich.text import Text
from rich.prompt import Prompt
from rich.panel import Panel

VOWELS = ['a', 'e', 'i', 'o', 'u']
CONSONANTS = ['k', 'r', 's', 't', 'm', 'n', 'h', 'y', 'w']

ALL = list(itertools.chain(map(lambda x: x[0] + x[1], itertools.product(CONSONANTS, VOWELS)), ['n']))
random.shuffle(ALL)

console = Console()
for i in ALL:
    console.print(Panel(i, style="bold magenta"))

    Prompt.ask("Next?")
