from random import randint
import random
import datetime
import locale

class UCLTools:
    def pass_generator(self):
        alphabet = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        pw_length = 8
        mypw = ""

        for i in range(pw_length):
            next_index = random.randrange(len(alphabet))
            mypw = mypw + alphabet[next_index]

        return mypw

    def login_generator(self, name):
        login = name.replace(' ', '')
        login = login.replace('-', '')
        rand = str(randint(0, 99))
        return login[:8]+rand

    def french_date(self, tr_date):
        date = datetime.datetime.strptime(tr_date, '%Y-%m-%d')
        try:
            locale.setlocale(locale.LC_ALL, 'fr_FR.utf8')
        except ValueError:
            'print Local not settable'

        return date.strftime("%A %d %B %Y")
