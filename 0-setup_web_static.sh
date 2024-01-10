#!/usr/bin/env bash
# Bash script that sets up your web servers for the deployment of web_static

apt-get update > /dev/null
apt-get install -y nginx > /dev/null

mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/
touch /data/web_static/releases/test/index.html
echo "Holberton School" > /data/web_static/releases/test/index.html
# Remove the existing symbolic link if it exists
if [ -d "/data/web_static/current" ]
then
	sudo rm -rf /data/web_static/current
fi
# Create the symbolic link
ln -s /data/web_static/releases/test/ /data/web_static/current
# Change ownership to user ubuntu
chown -R ubuntu:ubuntu /data/
# Configure nginx to serve content pointed to by symbolic link to hbnb_static
sed -i '16i\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n' /etc/nginx/sites-available/default

service nginx restart
