import itertools, random, os
from textual.app import App
from textual.containers import Container
from textual.widgets import Label

VOWELS = ['a', 'e', 'i', 'o', 'u']
CONSONANTS = ['k', 'r', 's', 't', 'm', 'n', 'h', 'y', 'w']

ALL = list(itertools.chain(map(lambda x: x[0] + x[1], itertools.product(CONSONANTS, VOWELS)), ['n']))
random.shuffle(ALL)

class Screen(App):
    CSS = """
    Screen {
    align: center middle;
    }
    """

    def compose(self) -> Container:
        yield Label("Test")

app = Screen()
app.run()

for i in ALL:
    console.print(Panel(i, style="bold magenta"))

    Prompt.ask("Next?")
