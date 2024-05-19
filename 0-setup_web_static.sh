#!/usr/bin/env bash
#  Bash
apt-get update
apt-get -y install nginx


if [ ! -d "/data/" ]; then
  mkdir /data/
fi
if [ ! -d "/data/web_static/" ]; then
  mkdir /data/web_static/
fi
if [ ! -d "/data/web_static/releases/" ]; then
  mkdir /data/web_static/releases/
fi
if [ ! -d "/data/web_static/shared/ " ]; then
  mkdir /data/web_static/shared/ 
fi
if [ ! -d "/data/web_static/releases/test/" ]; then
  mkdir /data/web_static/releases/test/
fi

echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" > /data/web_static/releases/test/index.html

ln -sf /data/web_static/releases/test/ /data/web_static/current

chown -hR ubuntu:ubuntu /data/
sed -i '51 i \\n\tlocation /hbnb_static {\n\talias /data/web_static/current;\n\t}' /etc/nginx/sites-available/default
service nginx restart
