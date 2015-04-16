# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv.orm import Model
from openerp.osv import osv, fields
import os
import time
import subprocess


class DbBackup(Model):
    _name = 'db.backup'
    _columns = {
        'name': fields.char('Database name', size=100, required='True',
                            help='Database you want to schedule backups for'),
        'bkp_dir': fields.char('Backup Directory', required='True',
                               help='Absolute path for storing the backups'),
    }

    def schedule_backup(self, cr, uid, context=None):
        config_ids = self.search(cr, uid, [], context=context)
        for rec in self.browse(cr, uid, config_ids, context=context):
            try:
                if not os.path.isdir(rec.bkp_dir):
                    os.chmod(rec.bkp_dir, 0777)
                    os.makedirs(rec.bkp_dir)
            except:
                raise "Cannot create backup file"

            bkp_file = '%s_%s.sql.gz' % (rec.name, time.strftime(
                '%Y%m%d_%H_%M_%S'))
            file_path = os.path.join(rec.bkp_dir, bkp_file)
            command = 'pg_dump %s > %s -Z 9' % (rec.name, file_path)
            subprocess.call(command, shell=True)

        return True

    def backup(self, cr, uid, ids, context=None):
        self.schedule_backup(cr, uid, context)
