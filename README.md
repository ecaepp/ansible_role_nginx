[![Build Status](https://travis-ci.org/ecaepp/ansible_role_nginx.svg?branch=master)](https://travis-ci.org/ecaepp/ansible_role_nginx)

ecaepp.nginx
=========

This role is being built to deploy an Nginx server on Ubuntu 16.04 that is configured and setup securly.

This role is currently in alpha testing

Requirements
------------

Ansible 2.4

Role Variables
--------------

Base role variables are defined in `default/main.yml` and is divied in to blocks base on the conf file or vhost configureation.

The role creates three config file at the moment `nginx.conf, general.conf, and a vhost conf`.

Configs are defined in `defaults/main.yml so they can be easily overwritten elsewhere in the playbook. 

Example of modifing Nginx configureation:

Lets take a look at the smaple configs found in `defaults/main.yml` that are found in the `nginx.conf` section.
```yaml
# http
charset: utf-8
sendfile: "on"
tcp_nopush: "on"
tcp_nodelay: "on"
types_hash_max_size: 2048
client_max_body_size: 16M
server_tokens: "off"
```

The recommended way to change default value of varibles for `nginx.conf` and `general.conf` is to copy the vars that need to be changed to `vars/main.yml`. It is best to also leave a comment noting the conf file the variable relates to and which stanza the config is stored in. This allows for easy versioning of custom vars in you own repo.

```yaml
# nginx.conf

# http
types_hash_max_size: 1024
server_tokens: "on"
```
```text
Note: Configuring variable like this allows for easy versioning of custom vars in your own repo/vc system.
```

VHosts
------
This role uses the template `templates/server.conf.j2` to create virtualhost conf files for applications.

First create a new `.yml` file in `vars` named after the application ex. `someapp.yml`
Second copy the vars from the vhosts section in `defaults/main.yml` the file you created and then fill in the vars to configure the vhost.
Any config not need can be remove. ex. The `fastcgi_php` configs can be deleted if they are not need as long proper YAML indentaion is maintained.

Example vhosts file for some app:
```yaml
vhost:
  - server_name: someapp.com
    listen_port: 80
    root_dir: /var/www/someapp
    index_name: index.html

    # ssl:
    #   cert_dir: /etc/nginx/ssl
    #   crt: '/etc/nginx/ssl/server.crt'
    #   key: '/etc/nginx/ssl/server.key'

    # security_headers:
    #   transport_security: Strict-Transport-Security "max-age=15768000; includeSubdomains",
    #   xframe_options: X-Frame-Options SAMEORIGIN

    try_files: '$uri $uri/ /index.html'

    # fastcgi_php:
    #   fastcgi_split_path_info: fastcgi_split_path_info ^(.+\.php)(/.+)$
    #   fastcgi_pass: 'fastcgi_pass unix:/var/run/php7.0-fpm.sock'
    #   fastcgi_index: fastcgi_index index.php,
    #   include_fastcgi: include fastcgi.conf
```
The SSL configs can be uncommented and set to the location of any certificates that have been uploaded or generated for the application to enable HTTPS.

The `security_headers` are set globally in `general.conf` and can be modified here.

`Fastcgi_php` can be uncommented for php apps that utilize fastcgi. Please note that this role currently only supports `php7.0-fpm`.

Dependencies
------------

Currently there are no plans for this role to have any dependencies of other roles.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables
passed in as parameters) is always nice for users too:
    
    playbook.yml

    - hosts: servers
      roles:
         - { role: ecaepp.nginx }

    vars/someapp.yml

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
          transport_security: Strict-Transport-Security "max-age=15768000; includeSubdomains",
          xframe_options: X-Frame-Options SAMEORIGIN

        try_files: '$uri $uri/ /index.html'


License
-------

MIT
