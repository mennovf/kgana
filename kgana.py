import itertools, random, os, sys
from textual.app import App
from textual.containers import Container
from textual.widgets import Label
from textual.reactive import reactive
from textual.keys import Keys
import art

VOWELS = ['a', 'e', 'i', 'o', 'u']
CONSONANTS = ['k', 'r', 's', 't', 'm', 'n', 'h', 'y', 'w']

EXCEPTIONS = {"ti": "chi", "si": "shi", "hu": "fu", "tu": "tsu"}

HIRAGANA = {"a":"あ","i":"い","u":"う","e":"え","o":"お",
"ka":"か","ki":"き","ku":"く","ke":"け","ko":"こ",
"ga":"が","gi":"ぎ","gu":"ぐ","ge":"げ","go":"ご",
"sa":"さ","shi":"し","shi":"し","su":"す","se":"せ","so":"そ",
"za":"ざ","ji":"じ","zu":"ず","ze":"ぜ","zo":"ぞ",
"ta":"た","chi":"ち","tsu":"つ","te":"て","to":"と",
"da":"だ","zu":"づ","de":"で","do":"ど",
"na":"な","ni":"に","nu":"ぬ","ne":"ね","no":"の",
"ha":"は","hi":"ひ","fu":"ふ","he":"へ","ho":"ほ",
"ba":"ば","bi":"び","bu":"ぶ","be":"べ","bo":"ぼ",
"pa":"ぱ","pi":"ぴ","pu":"ぷ","pe":"ぺ","po":"ぽ",
"ma":"ま","mi":"み","mu":"む","me":"め","mo":"も",
"ya":"や","yu":"ゆ","yo":"よ",
"ra":"ら","ri":"り","ru":"る","re":"れ","ro":"ろ",
"wa":"わ","wo":"を",
"n":"ん",
"kya":"きゃ","kyu":"きゅ","kyo":"きょ",
"gya":"ぎゃ","gyu":"ぎゅ","gyo":"ぎょ",
"sha":"しゃ","shu":"しゅ","sho":"しょ",
"ja":"じゃ","ju":"じゅ","jo":"じょ",
"cha":"ちゃ","chu":"ちゅ","cho":"ちょ",
"nya":"にゃ","nyu":"にゅ","nyo":"にょ",
"hya":"ひゃ","hyu":"ひゅ","hyo":"ひょ",
"bya":"びゃ","byu":"びゅ","byo":"びょ",
"pya":"ぴゃ","pyu":"ぴゅ","pyo":"ぴょ",
"mya":"みゃ","myu":"みゅ","myo":"みょ",
"rya":"りゃ","ryu":"りゅ","ryo":"りょ",
"vu":"ゔ",
"sakuon":"っ"}

KATAKANA = {"a":"ア","i":"イ","u":"ウ","e":"エ","o":"オ",
"ka":"カ","ki":"キ","ku":"ク","ke":"ケ","ko":"コ",
"ga":"ガ","gi":"ギ","gu":"グ","ge":"ゲ","go":"ゴ",
"sa":"サ","shi":"シ","su":"ス","se":"セ","so":"ソ",
"za":"ザ","ji":"ジ","zu":"ズ","ze":"ゼ","zo":"ゾ",
"ta":"タ","chi":"チ","tsu":"ツ","te":"テ","to":"ト",
"da":"ダ","zu":"ヅ","de":"デ","do":"ド",
"na":"ナ","ni":"ニ","nu":"ヌ","ne":"ネ","no":"ノ",
"ha":"ハ","hi":"ヒ","fu":"フ","he":"ヘ","ho":"ホ",
"ba":"バ","bi":"ビ","bu":"ブ","be":"ベ","bo":"ボ",
"pa":"パ","pi":"ピ","pu":"プ","pe":"ペ","po":"ポ",
"ma":"マ","mi":"ミ","mu":"ム","me":"メ","mo":"モ",
"ya":"ヤ","yu":"ユ","yo":"ヨ",
"ra":"ラ","ri":"リ","ru":"ル","re":"レ","ro":"ロ",
"wa":"ワ","wo":"ヲ",
"n":"ン",
"kya":"キャ","kyu":"キュ","kyo":"キョ",
"gya":"ギャ","gyu":"ギュ","gyo":"ギョ",
"sha":"シャ","shu":"シュ","sho":"ショ",
"ja":"ジャ","ju":"ジュ","jo":"ジョ",
"cha":"チャ","chu":"チュ","cho":"チョ",
"nya":"ニャ","nyu":"ニュ","nyo":"ニョ",
"hya":"ヒャ","hyu":"ヒュ","hyo":"ヒョ",
"bya":"ビャ","byu":"ビュ","byo":"ビョ",
"pya":"ピャ","pyu":"ピュ","pyo":"ピョ",
"mya":"ミャ","myu":"ミュ","myo":"ミョ",
"rya":"リャ","ryu":"リュ","ryo":"リョ",
"vu":"ヴ",
"va":"ヴァ","vi":"ヴィ","ve":"ヴェ","vo":"ヴォ",
"wi":"ウィ","we":"ウェ",
"fa":"ファ","fi":"フィ","fe":"フェ", "fo":"フォ",
"che":"チェ",
"di":"ディ","du":"ドゥ",
"ti":"ティ","tu":"トゥ",
"je":"ジェ",
"she":"シェ",
"sakuon":"ッ",
"pause":"ー"}

ALL = list(set(map(lambda s: EXCEPTIONS.get(s, s), itertools.chain(map(lambda x: x[0] + x[1], itertools.product(CONSONANTS, VOWELS)), ['n']))) - set(["we", "wi", "wu", "ye", "yi"]))
random.shuffle(ALL)

def large(s: str):
    return art.text2art(s, font="smslant")

class Screen(App):
    CSS = """
    Screen {
        align: center middle;
    }
    #romaji {
        align: center middle;
    }
    #kanas {
        align: center middle;
    }
    """
    def __init__(self, sequence):
        super().__init__()
        self.sequence = sequence
        self.to_show = None

        self.label_query = Label(large("KGANA"), id="romaji")
        self.label_answer = Label("", id="kanas")

    def compose(self) -> Container:
        yield self.label_query
        yield self.label_answer

    def on_key(self, event: Keys) -> None:
        if self.to_show is not None:
            self.label_answer.update(" "*(3 * (len(self.to_show) - 1)) + HIRAGANA[self.to_show] + " " + KATAKANA[self.to_show])
            self.to_show = None
        else:
            kana = self.sequence.pop()
            self.label_query.update(large(kana))
            self.label_answer.update("")
            self.to_show = kana

if __name__ == "__main__":
    app = Screen(ALL)
    app.run()
