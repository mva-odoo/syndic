from random import randint
import random


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
