import xmlrpclib
import sys

username = sys.argv[1]
pwd = sys.argv[2]
dbname = sys.argv[3]


sock_common = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/common')
uid = sock_common.login(dbname, username, pwd)
sock = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/object')
with open('compte', 'r') as comptes:
    for ligne in comptes.readlines():
        compte = ligne.split(' ', 1)
        sock.execute(dbname, uid, pwd, 'syndic.pcmn', 'create', {'code': compte[0], 'name': compte[1]})




