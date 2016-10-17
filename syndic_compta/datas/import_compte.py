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
        ligne = ligne.replace('.', '')
        compte = ligne.split(' ', 1)

        ids = sock.execute(dbname, uid, pwd, 'syndic.compta.pcmn', 'search', [('code', '=', compte[0][:-1])])
        parent_id = False
        if ids:
            parent_id = ids[0]

        sock.execute(dbname, uid, pwd, 'syndic.compta.pcmn', 'create', {
            'code': compte[0],
            'name': compte[1],
            'parent_id': parent_id
        })




