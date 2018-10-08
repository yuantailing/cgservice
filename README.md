# cgservice

Run all services in a docker composer.

## 概述

1. vsftpd 是 FTP 服务，用于上传文件到网站目录，开放 FTP 端口
1. apache2 用于托管网站（根据域名区分），开放 HTTP、HTTPS 端口
1. pptp、l2tp、openvpn 是几个 VPN 服务，开放各自的端口
1. netredirect 用于 VPN 重定向，VPN 把目的地址为 net.tsinghua.edu.cn 的流量重定向到这里，避免用户通过 VPN 意外“断开连接”
1. mysql 是内网数据库服务
1. phpmyadmin 是 web 端管理 mysql 数据库用的，用 apache2 转发
1. cgserver 是另一项 web 服务，并提供 openvpn 的认证。cgserver 也用 apache2 转发
1. letsencrypt 用于签署 SSL 证书，以便 apache2 能用 HTTPS
1. 网络做了隔离，前端的 apache2 不能跟后端的 mysql 通信，各个 VPN 之间也不能通过内网通信
1. docker-compose 用于构建和管理这些服务，一键启动和停止整批服务

## Usage

### Quick start
1. Please inall [docker](https://docs.docker.com/install/linux/docker-ce/debian/) and [docker-compose](https://docs.docker.com/compose/install/).

1. Build the base image.

   ```sh
   $ base/build.sh
   ```

1. Copy sample configs and make secret config files not globally visible.

   ```sh
   $ cp -r apache2/conf/sites-available.sample/ apache2/conf/sites-available/ && \
       cp vsftpd/conf/vusers.txt.sample vsftpd/conf/vusers.txt && \
       cp -r netredirect/conf/sites-available.sample netredirect/conf/sites-available && \
       cp pptp/conf/chap-secrets.sample pptp/conf/chap-secrets && \
       cp l2tp/vpn.env.sample l2tp/vpn.env && \
       cp openvpn/conf/settings.py.sample openvpn/conf/settings.py && \
       touch openvpn/conf/server.key && \
       cp mysql/password.env.sample mysql/password.env && \
       cp cgserver/conf/settings.py.sample cgserver/conf/settings.py && \
       cp letsencrypt/sites.env.sample letsencrypt/sites.env

	$ chmod 600 vsftpd/conf/vusers.txt pptp/conf/chap-secrets l2tp/vpn.env \
	   openvpn/conf/settings.py openvpn/conf/server.key mysql/password.env \
	   cgserver/conf/settings.py
   ```

1. Up docker composer

   ```sh
   $ docker-compose up --build
   ```

  You can also up docker-compose in daemon mode

   ```sh
   $ docker-compose up --build -d
   ```

### What's next

You should edit configs to solve following issues:

1. Apache2 `ServerName` is not properly configured, so you will always visit the default website.
1. Ensure ftp user root exists and have the proper owner, or vsftpd will fail.
1. The default vsftpd passwords are weak and public available.
1. The default pptp password and l2tp password are weak and public available.
1. OpenVPN key file is broken and openvpn will fail. Please use the correct key file.
1. OpenVPN `CLIENT_SECRET` is incorrect so it cannot communicate with cgserver.
1. The default mysql root password is unsafe, please login to phpmyadmin and change it.
1. Create a database and db user, and then config cgserver to the correct database.
1. Futher configure cgserver.
1. Letsencrypt domain name is not properly configured, so it's failed to issue SSL certificates.
1. Edit apache2 *\*-le-ssl.conf* to use SSL, and edit HTTP configs to redirect to HTTPS.
1. Add a service to run letsencrypt in cycle to renew certificates.

## Services

### apache2

1. Copy *apache2/conf/sites-available.sample/* to *apache2/conf/sites-available/* and edit then (fill `ServerName`).
1. Build and run.
1. After certificates are issued, we can further edit configs in *apache2/conf/sites-available/*, enable SSL, and rewrite HTTP to HTTPS.

### vsftpd

1. Copy *vsftpd/conf/vusers.txt.sample* to *vsftpd/conf/vusers.txt* and edit it.
1. Edit config files in *vsftpd/conf/vsftpd_user_conf/*.
1. Ensure user roots (*/srv/ftp/cscg* and */srv/ftp/oslab*) exists and have the proper owner (UID is 10021 and GID is 10021).
1. Build and run.

### netredirect

1. Copy *netredirect/conf/sites-available.sample/* to *netredirect/conf/sites-available/*.
1. Build and run.
1. After certificates are issued, we can further edit configs in *netredirect/conf/sites-available/*, enable SSL, and rewrite HTTP to HTTPS.

### pptp

1. Copy *pptp/conf/chap-secrets.sample* to *pptp/conf/chap-secrets* and edit it.
1. Build and run.

### l2tp

1. Load the IPsec af_key kernel module on the Docker host: `sudo modprobe af_key`.
1. Copy *l2tp/vpn.env.sample* to *l2tp/vpn.env* and edit it.
1. Build and run.

### openvpn

1. Generate *openvpn/conf/dh2048.pem* by running `openssl dhparam -out openvpn/conf/dh2048.pem 2048`.
1. Create *openvpn/conf/server.key* (see *openvpn/conf/server.key.sample* for the format).
1. Copy *openvpn/conf/settings.py.sample* to *openvpn/conf/settings.py* and edit it (fill `CLIENT_SECRET`).
1. Build and run.

### mysql

1. Copy *mysql/password.env.sample* to *mysql/password.env* and edit it. Note that only the password set on the first run affects.
1. Run.

### phpmyadmin

1. Run.
1. You can login to phpmyadmin in the default website (usually you can visit it by IP, and URI is /phpmyadmin/).

### cgserver

1. Create a database and a user in database.
1. Copy *cgserver/conf/settings.py.sample* to *cgserver/conf/settings.py* and edit it (fill `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `DATABASES`, `GITHUB_CLIENT_SECRET`, `GITHUB_PERSONAL_ACCESS_TOKEN` and `VPN_CLIENT_SECRET`).
1. Build and run.
1. Run `docker-compose exec cgserver python3 manage.py migrate` to initialize database.
1. Run `docker-compose exec cgserver python3 manage.py createsuperuser` to a super user, who can login to Django administration.
1. Login to Django administration (URI is /admin/) and add some server configs.

### letsencrypt

1. Copy *letsencrypt/sites.env.sample* to *letsencrypt/sites.env* and edit it.
1. Build and run.
1. Update apache2 config files and reload apache2 by running `docker-compose exec apache2 apachectl -k graceful` and `docker-compose exec netredirect apachectl -k graceful`.

Each certificate expires in about 3 months, so letsencrypt should be run in cycles to renew certificates. Apache2 should be running when renewing certificates.

## Todo

- [x] Support HTTPS for apache2. Mount cert files into apache2 container, and add a service to renew certifications.
- [x] Add cgserver service.
- [x] Handle static files in cgserver.
- [x] Redirect traffic to *net.tsinghua.edu.cn* to another page by DNAT.
- [ ] Put ftp into a Docker volume, ~~do so to mysql data~~.
- [ ] In cgserver, add a callback URL to GitHub OAuth to allow multiple instances use the same OAuth App.
- [x] Add OpenVPN protocol TCP.
- [x] Make it easier to config apache2.
- [ ] Make it easier to config openvpn.
- [ ] VPN server secret is not required if we use intranet to communicate with cgserver.
- [x] Add an automate script to generate configs (just copy sample configs).
- [ ] Make netredirect more friendly.
- [ ] Build all docker images from *debian:stretch* and we will have no need to build *cscg/base*.
- [ ] Promote FTP to FTPS.
- [ ] Backup script for web content.
