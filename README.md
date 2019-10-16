[![Build Status](https://travis-ci.org/ecaepp/ansible_role_nginx.svg?branch=master)](https://travis-ci.org/ecaepp/ansible_role_nginx)

## Nginx

This role is built to deploy Nginx on an Ubuntu 16.04.

## Requirements

Ansible 2.4

-------

## Configuration

All options in this section are configured as defaults for Nginx and are defined in `defaults.yml` so that they can easly be overwritten within the playbook.

### Self Signed Cert Generation

The Role has an option for generating a self signed TLS cert for testing. This setting is set to false defaultly to prevent unwanted self signed cert generation.

```yaml
selfsigned_cert: false # Generate self signed SSL cert.
```

### Configuratoin Files

All options in this section are configured as defaults for Nginx and are defind in `defaults.yml` so that they can easly be overwritten within the playbook.

This role currently creates three conf files.

* nginx.conf
* general.conf
* server.conf (vhost)

#### nginx.conf

This file contains options for cofiguring global options pretaining to the Nginx service.

```yaml
# Service
nginx_user: www-data
worker_processes: auto
nginx_pid_file: /var/run/nginx.pid
worker_rlimit_nofile: 8192

# Events
event_multi_accept: "on"
worker_connections: 4096

# http
charset: utf-8
sendfile: "on"
tcp_nopush: "on"
tcp_nodelay: "on"
types_hash_max_size: 2048
client_max_body_size: 16M
server_tokens: "off"

# MIME
include: mime.types
default_type: application/octet-stream

# Logging
access_log: /var/log/nginx/access.log
error_log: /var/log/nginx/error.log warn

# Limits
limit_req_log_level: warn
limit_req_zone: $binary_remote_addr zone=login:10m rate=10r/m

# SSL
ssl_session_timeout: 1d
ssl_session_cache: shared:SSL:50m
ssl_session_tickets: "off"

# Modern Config
ssl_protocols: TLSv1.2
ssl_ciphers: ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA256
ssl_prefer_server_ciphers: "on"

# OSCP Stapling
stapling: "on"
stapling_verify: "on"
resolver: 8.8.8.8 8.8.4.4 208.67.222.222 208.67.220.220 valid=60s
resolver_timeout: 2s

# Load Configs
conf_files: /etc/nginx/conf.d/*.conf
sites_enabled: /etc/nginx/sites-enabled/*
```

#### general.conf

This conf file is used to set security headers, restrict access to `.` files, and compression options.

```yaml
# Security Headers
header_options: |
  add_header X-Frame-Options "SAMEORIGIN" always;
  add_header X-XSS-Protection "1; mode=block" always;
  add_header X-Content-Type-Options "nosniff" always;
  add_header Referrer-Policy "no-referrer-when-downgrade" always;
  add_header Content-Security-Policy "default-src * data: 'unsafe-eval' 'unsafe-inline'" always;
  add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
# . files
dot_file_location: "deny all"

# Assets media
media_expires: 7d
media_access_log: "off"

# svg, fonts
fonts_headrer_options: 'Access-Control-Allow-Origin "*"'
fonts_expire: 78
fonts_access_log: "off"

# Gzip
gzip_status: "on"
gzip_vary: "on"
gzip_proxied: any
gzip_comp_level: 6
gzip_types: 'text/plain text/css text/xml application/json application/javascript application/xml+rss application/atom+xml image/svg+xml'
```

`**NOTE:** This file is likely to be deprecated in future when I have time to rewrite the conf file tasks.`

#### server.conf

This file is used to configure Nginx to actually server the web application. This role generates these files from a template in the task `tasks/configure.yml`.

Currently the options below are required for Nginx to be able to run the app

* server_name
* listen_port
* root_dir
* index_name

```yaml
vhost: []
  - server_name: test.com
    listen_port: 80
    root_dir: /var/www
    index_name: index.html

    ssl:
      cert_dir: /etc/nginx/ssl
      crt: '/etc/nginx/ssl/server.crt'
      key: '/etc/nginx/ssl/server.key'

    security_headers:
      transport_security: Strict-Transport-Security "max-age=15768000; includeSubdomains",
      xframe_options: X-Frame-Options SAMEORIGIN

    try_files: '$uri $uri/'

    fastcgi_php:
      fastcgi_split_path_info: fastcgi_split_path_info ^(.+\.php)(/.+)$
      fastcgi_pass: 'fastcgi_pass unix:/var/run/php7.0-fpm.sock'
      fastcgi_index: fastcgi_index index.php,
      include_fastcgi: include fastcgi.conf
```

## Example Playbook

Including an example of how to use your role (for instance, with variables
passed in as parameters) is always nice for users too:

    playbook.yml

    - hosts: servers
      roles:
         - { role: ecaepp.nginx }

      vars:

      vhost:
          - server_name: test.com
            listen_port: 80
            root_dir: /var/www/someapp/app/webroot/
            index_name: index.html

            ssl:
              cert_dir: /etc/nginx/ssl
              crt: '/etc/nginx/ssl/someapp.com.crt'
              key: '/etc/nginx/ssl/someapp.com.key'

            security_headers:
              transport_security: Strict-Transport-Security "max-age=15768000;  includeSubdomains",
              xframe_options: X-Frame-Options SAMEORIGIN

            try_files: '$uri $uri/ /index.html'

## License

MIT
