import xmlrpclib
import sys
from random import randint

# example python change_login.py login mdp db

username = sys.argv[1]
pwd = sys.argv[2]
dbname = sys.argv[3]
import random

def pass_generator():
    alphabet = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    pw_length = 8
    mypw = ""

    for i in range(pw_length):
        next_index = random.randrange(len(alphabet))
        mypw = mypw + alphabet[next_index]

    return mypw

sock_common = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/common')
uid = sock_common.login(dbname, username, pwd)
sock = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/object')
users = sock.execute(dbname, uid, pwd, 'res.users', 'search_read', [('id', '>', 1)], ['name', 'login', 'password'])

for user in users:
    login = user['login'].replace(' ', '')
    login = user['login'].replace('-', '')
    rand = str(randint(0, 99))
    try:
        sock.execute(dbname, uid, pwd, 'res.users', 'write', [user['id']], {'login': login[:8]+rand, 'password': pass_generator()})
    except:
        print '%s cannot replace name'%user['login']