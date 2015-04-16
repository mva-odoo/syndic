install wkhtmltopdf
$ sudo wget http://jaist.dl.sourceforge.net/project/wkhtmltopdf/0.12.1/wkhtmltox-0.12.1_linux-trusty-amd64.deb
$ sudo dpkg -i wkhtmltox-0.12.1_linux-trusty-amd64.deb
$ sudo cp /usr/local/bin/wkhtmltopdf /usr/bin

si jamais pas de css

system parameters	
Clé
report.url
Valeur
http://127.0.0.1:8069
Groupes


nginx

server {
    server_name ks301308.kimsufi.com;
    listen 443;
    #ssl certificates
    ssl on;
    ssl_certificate /etc/ssl/openerpssl/openerp.crt;
    ssl_certificate_key /etc/ssl/openerpssl/openerp.key;

    location / {
        proxy_pass http://localhost:8069;
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
server {
     listen 80;
     server_name ks301308.kimsufi.com;
     add_header Strict-Transport-Security max-age=2592000;
     location / {
            proxy_set_header    Host $host;
            proxy_set_header    X-Real-IP   $remote_addr;
            proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_pass  http://localhost:8069;
        }
}



mount bind

vim /etc/fstab
add this line
/home/var /var none bind 0 0
mount /var

ps:(bg run background)

crontab
crontab -l (list)
crontab -e (edit)
47 23 * * * python /home/bkp.py everyday a 23h47
service cron restart