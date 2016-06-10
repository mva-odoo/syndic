import xmlrpclib
import sys
from random import randint

# example python change_login.py login mdp db

username = sys.argv[1]
pwd = sys.argv[2]
dbname = sys.argv[3]
import random

sock_common = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/common')
uid = sock_common.login(dbname, username, pwd)
sock = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/object')
users = sock.execute(dbname, uid, pwd, 'res.users', 'search_read', [('id', '>', 1)], ['name', 'login', 'password'])


passwd = pass_generator()
for building in sock.execute(dbname, uid, pwd, 'res.users', 'search', [('user_id', '!=', False)]):
    user_id = sock.execute(dbname, uid, pwd, 'res.users', 'create', {
        'name': building.name,
        'login': building.name,
        'password': passwd,
        'groups_id': [(6, 0, self.env['res.groups'].search([('name', 'ilike', 'Syndic/Client')]).ids)],
    })

    building

    vals['user_id'] = self.env['res.users'].sudo().create({
        'name': building.name,
        'login': building.name,
        'password': passwd,
        'groups_id': [(6, 0, self.env['res.groups'].search([('name', 'ilike', 'Syndic/Client')]).ids)],
    }).id

building.write({'password': passwd})