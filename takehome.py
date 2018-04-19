from api.food2fork_client import Food2ForkClient
from spellcheck.english_dict import EnglishDictionary

class TakeHomeApplication:
    def __init__(self):
        self._food2fork_client = Food2ForkClient()
        self._spell_checker = EnglishDictionary()

    def main(self):
        print('hello, world')

if __name__ == '__main__':
    app = TakeHomeApplication()
    app.main()