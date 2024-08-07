import itertools, random, os, sys
from textual.app import App
from textual.containers import Container
from textual.widgets import Label
from textual.reactive import reactive
from textual.keys import Keys
import art

VOWELS = ['a', 'e', 'i', 'o', 'u']
CONSONANTS = ['k', 'r', 's', 't', 'm', 'n', 'h', 'y', 'w']

ALL = list(itertools.chain(map(lambda x: x[0] + x[1], itertools.product(CONSONANTS, VOWELS)), ['n']))
random.shuffle(ALL)

def large(s: str):
    return art.text2art(s, font="smslant")

class Screen(App):
    CSS = """
    Screen {
        align: center middle;
    }
    """
    def __init__(self, sequence):
        super().__init__()
        self.sequence = sequence

    def compose(self) -> Container:
        yield Label(large("KGANA"), id="romaji")

    def on_key(self, event: Keys) -> None:
        self.query_one(Label).update(large(self.sequence.pop()))

if __name__ == "__main__":
    app = Screen(ALL)
    app.run()
