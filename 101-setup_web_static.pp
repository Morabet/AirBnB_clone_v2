# sets up your web servers for the deployment of web_static

exec {'update':
  provider => shell,
  command  => 'sudo apt-get -y update',
  before   => Exec['install Nginx'],
}

exec {'install Nginx':
  provider => shell,
  command  => 'sudo apt-get -y install nginx',
  before   => Exec['add_dir_test'],
}


exec {'add_dir_test':
  provider => shell,
  command  => 'mkdir -p /data/web_static/releases/test/',
  before   => Exec['add_dir_shared'],
}

exec {'add_dir_shared':
  provider => shell,
  command  => 'mkdir -p /data/web_static/shared/',
  before   => Exec['add_file_html'],
}


exec {'add_file_html':
  provider => shell,
  command  => 'echo "Holberton School" >/data/web_static/releases/test/index.html',
  before   => Exec['remove_symbol'],
}

file {'remove_symbol'
  path     => '/data/web_static/current',
  ensure   => absent,
  before   => Exec['create_symbol']
}

exec {'create_symbol':
  provider => shell,
  command  => 'ln -sf /data/web_static/releases/test/ /data/web_static/current',
  before   => Exec['change_owner'],
}

exec {'change_owner':
  provider => shell,
  command  => 'chown -R ubuntu:ubuntu /data',
  before   => Exec['conf_nginx'],
}

exec { 'conf_nginx':
  provider => shell,
  command  => 'sed -i '38i\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n' /etc/nginx/sites-available/default',
  before   => Exec['restart Nginx'],
}

exec { 'restart Nginx':
  provider => shell,
  command  => 'sudo service nginx restart',
}
