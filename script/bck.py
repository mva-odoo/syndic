#!/usr/bin/env python
import os
import time
import subprocess

bkp_dir = '/home/var/www/owncloud/data/sgimmo/files/'
name = 'sgimmo'
try:
    if not os.path.isdir(bkp_dir):
        os.makedirs(bkp_dir)
        os.chmod(bkp_dir, 0777)
except:
    raise "Cannot create backup file"

bkp_file = '%s_%s.sql.gz' % (name, time.strftime('%Y%m%d_%H_%M_%S'))
file_path = os.path.join(bkp_dir, bkp_file)
command = 'pg_dump %s > %s -Z 9' % (name, file_path)
subprocess.call(command, shell=True)
