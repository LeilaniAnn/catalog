**Instructions for SSH access to the instance**
-----------------------------------------------

----------
**Download Private Key**
*Move the private key file into the folder ~/.ssh (where ~ is your environment's home directory). So if you downloaded the file to the Downloads folder, just execute the following command in your terminal.*

> mv ~/Downloads/udacity_key.rsa ~/.ssh/

**Open your terminal and type in** 

> chmod 600 ~/.ssh/udacity_key.rsa

**In your terminal, type in** 

> ssh -i ~/.ssh/udacity_key.rsa root@54.68.216.109

**Create a new user named grader**
> sudo adduser grader

**Give the grader the permission to sudo**

> sudo nano /etc/sudoers.d/grader 
> 
```grader ALL=(ALL) NOPASSWD:ALL```

**Logged in as root on the server, run**

> mkdir /home/grader/.ssh
> chown grader /home/grader/.ssh
> chgrp grader /home/grader/.ssh

**Next create the file ```/home/grader/.ssh/authorized_keys```
>chown grader /home/grader/.ssh/authorized_keys
chgrp grader /home/grader/.ssh/authorized_keys
chmod 644 /home/grader/.ssh/authorized_keys
chmod 700 /home/grader/.ssh

**Login with new user**
>sudo su grader

**Configure SSH (Change the SSH port from 22 to 2200 & restrict root login)**
>nano /etc/ssh/sshd_config
```Port 2200```
```PermitRootLogin no```

**Check cannot login as root**
>ssh -i ~/.ssh/udacity_key.rsa grader@54.68.216.109 -p 2200
```Permission denied (publickey).```

**Update all packages using the following commands:**
>sudo apt-get update
sudo apt-get upgrade

**Configure the Uncomplicated Firewall (UFW) to only allow incoming connections for SSH (port 2200), HTTP (port 80), and NTP (port 123)**
>sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 2200/tcp
sudo ufw allow 80/tcp
sudo ufw allow 123/tcp
sudo ufw enable
sudo ufw status

**Monitor for repeat unsuccessful login attempts and ban attackers. Documented at Digitalocean.com - "Protect SSH with fail2ban"**
>sudo apt-get install fail2ban
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
sudo nano /etc/fail2ban/jail.local
Change the ssh port number line
```port     = 2200```

**Restart fail2ban**
>sudo service fail2ban restart

**Configure the local timezone to UTC. As discussed at askubuntu.com.**
>sudo dpkg-reconfigure tzdata
```Choose "None of the above" and then "UTC"```

**Install and configure Apache to serve a Python mod_wsgi application**
>sudo apt-get install apache2
sudo aptitude install libapache2-mod-wsgi
sudo apt-get install libapache2-mod-wsgi python-dev

**Install and configure PostgreSQL (remote connections are disabled by default)**
>sudo apt-get install postgresql

**Install Git**
>sudo apt-get install git

**Clone project source application from git repository**
>Cd /var/www
>sudo git clone -b project https://github.com/LeilaniAnn/catalog.git 
>```(branch made specifically for this project due to database changes)```

**Install PIP and required Python packages**
>sudo apt-get install python-pip
sudo pip install flask httplib2 sqlalchemy requests oauth2client
sudo apt-get install python-psycopg2

**Create database user**
>```sudo su - postgres```
```Psql```
```CREATE USER catalog WITH PASSWORD 'secure_password';```
```GRANT SELECT, INSERT, DELETE, UPDATE ON ALL TABLES IN SCHEMA public TO catalog;```
```\q```
```exit```

**Configure application**
>```sudo nano catalog.conf```

**Copy and paste the following into catalog.conf:** 
```
	<VirtualHost *:80>
    ServerName http://54.68.216.109/
    ServerAlias ec2-54-68-216-109.us-west-2.compute.amazonaws.com
    ServerAdmin grader@52.38.62.144/
    DocumentRoot /var/www/catalog/catalog

    <Directory /usr/local/www/catalog/catalog>
    Order allow,deny
    Allow from all
    </Directory>

    WSGIScriptAlias / /var/www/catalog/catalog.wsgi

    <Directory /var/www/catalog>
    Order allow,deny
    Allow from all
    </Directory>

	</VirtualHost>
```
>```sudo cp /var/www/catalog/catalog.conf /etc/apache2/sites-available```
```sudo nano catalog.wsgi``` 

**copy and paste the following into catalog.wsgi:**
```
!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/catalog/catalog")

from project import app as application
application.secret_key = 'super_secret_key'
```
**Allow users to upload files (pictures) to static.**
>```sudo chmod 777 /var/www/catalog/catalog/static```

**Start serving app.**
>```Service apache2 reload```
```sudo a2ensite catalog```
```sudo service apache2 restart```

**Create db and populate**
Replace all engine variables with: engine = create_engine('postgresql://catalog:secure_password@localhost/catalog')
------------------------------------------------------------------------
>```sudo -u postgres createdb -O catalog catalog```
```python /var/www/catalog/catalog/db.py```
```python /var/www/catalog/catalog/items.py```

**Restrict access to .git folder**
>```cd /var/www/catalog```
```sudo nano .htaccess```
**RedirectMatch 404 /\.git ( http://stackoverflow.com/questions/6142437/make-git-directory-web-inaccessible)**

**Automatic Ubuntu server package updates**
>```sudo apt-get install unattended-upgrades```
```sudo dpkg-reconfigure --priority=low unattended-upgrades```
*(Answer yes to question)*

If app is not displaying (problems I encountered only once out of the 4 times I deleted environment):
Update the Apache configuration file to serve the web application with WSGI.
>```sudo nano /etc/apache2/sites-enabled/000-default.conf```
Add the following line inside the "VirtualHost *:80" element, and save the file.
```WSGIScriptAlias / /var/www/catalog/catalog.wsgi```

**Other issues I had:**
If error with fb_client_secrets.json : Update Project.py with absolute paths to secrets json files (“var/www/catalog/catalog/fb_secrets…)
**Fix sudo warning message**
The sudo command was displaying a warning message unable to resolve host [ip-10-20-2-57]. In /etc/hosts file the line reads: 127.0.0.1 localhost ip-10-20-2-57
**Any other errors:** 
>```sudo tail /var/log/apache2/error.log``` is my new best friend

AH00494: SIGHUP received.  Attempting to restart : Not a bug - just restarts Apache for the traffic/bandwidth tallys
AH00491: caught SIGTERM, shutting down: http://stackoverflow.com/questions/1661802/apache-server-keeps-crashing-caught-sigterm-shutting-down
