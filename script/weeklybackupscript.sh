 #!/bin/bash
DIR=/home/openerp/oerpbackups
[ !$DIR ] && mkdir -p $DIR || :
LIST=$(su - postgres -c "psql -lt" |awk '{ print $1}' |grep -vE '^-|:|^List|^Name|template[0|1]')
for d in $LIST
do
 mkdir -p $DIR/$d
 chown postgres:postgres $DIR/$d
 su - postgres -c "/usr/bin/pg_dump --format=c $d | gzip -c > $DIR/$d/$d.`date +\%a`.sql.gz"
done 