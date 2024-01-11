# sets up your web servers for the deployment of web_static

$config = "server {
    listen 80 default_server;
    listen [::]:80 default_server;

    add_header X-Served-By ${hostname};

    root   /var/www/html;
    index  index.html index.htm;
    location / {
        try_files ${uri} ${uri}/ =404;
    }

    location /hbnb_static {
        alias /data/web_static/current;
        index index.html index.htm;
    }
}"

exec {'update':
  provider => shell,
  command  => 'sudo apt-get -y update',
}

-> package { 'nginx':
ensure   => 'installed',
provider => 'apt'
}

-> file { '/data':
  ensure  => 'directory'
}

-> file { '/data/web_static':
  ensure => 'directory'
}

-> file { '/data/web_static/releases':
  ensure => 'directory'
}

-> file { '/data/web_static/releases/test':
  ensure => 'directory'
}

-> file { '/data/web_static/shared':
  ensure => 'directory'
}

-> file { '/data/web_static/releases/test/index.html':
  ensure  => 'present',
  content => 'Holberton School'
}

-> file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test'
}

-> exec {'owner':
command => 'chown -R ubuntu:ubuntu /data',
path    => '/usr/bin/:/usr/local/bin/:/bin/'
}

-> file { '/etc/nginx/sites-available/default':
  ensure  => 'present',
  content => $config
}

-> exec { 'restart nginx':
provider => shell,
command  => 'sudo service nginx restart',
}
