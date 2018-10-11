# cgservice

Run all services in a docker composer.

## 概述

1. vsftpd 是 FTP 服务，用于上传文件到网站目录，开放 FTP 端口
1. apache2 用于托管网站（根据域名区分），开放 HTTP、HTTPS 端口
1. pptp、l2tp、openvpn 是几个 VPN 服务，开放各自的端口
1. netredirect 用于 VPN 重定向，VPN 把目的地址为 net.tsinghua.edu.cn 的流量重定向到这里，避免用户通过 VPN 意外“断开连接”
1. mysql 是内网数据库服务
1. phpmyadmin 是可视化管理 mysql 数据库的 web 服务，用 apache2 转发
1. cgserver 是另一项 web 服务，并提供 openvpn 的认证，用 apache2 转发
1. csvn 是 SVN 服务，用 apache2 转发
1. letsencrypt 用于签署 SSL 证书，使得 apache2 用 HTTPS，vsftpd 用 FTPS
1. 网络做了隔离，前端的 apache2 不能跟后端的 mysql 通信，各个 VPN 之间也不能通过内网通信
1. docker-compose 用于构建和管理这些服务，一键启动和停止整批服务

## Usage

### Quick start
1. Please inall [docker](https://docs.docker.com/install/linux/docker-ce/debian/) and [docker-compose](https://docs.docker.com/compose/install/).

1. Copy sample configs and make secret config files not globally visible.

   ```sh
   $ cp .env.sample .env && \
       cp -r apache2/conf/sites-available.sample/ apache2/conf/sites-available/ && \
       cp vsftpd/conf/vsftpd.conf.sample vsftpd/conf/vsftpd.conf && \
       cp vsftpd/conf/vusers.txt.sample vsftpd/conf/vusers.txt && \
       cp -r netredirect/conf/sites-available.sample netredirect/conf/sites-available && \
       cp openvpn/conf/settings.py.sample openvpn/conf/settings.py && \
       cp openvpn/conf/server.key.sample openvpn/conf/server.key && \
       cp cgserver/conf/settings.py.sample cgserver/conf/settings.py && \
       cp letsencrypt/sites.env.sample letsencrypt/sites.env && \
       cp -r backup/ignore.sample backup/ignore

   $ chmod 600 vsftpd/conf/vusers.txt pptp/conf/chap-secrets l2tp/vpn.env \
       openvpn/conf/settings.py openvpn/conf/server.key cgserver/conf/settings.py
   ```

1. Build images

   ```sh
   $ docker-compose build
   ```

1. (l2tp) Load the IPsec af_key kernel module on the Docker host: `sudo modprobe af_key`.

1. Up docker composer

   ```sh
   $ docker-compose up --build
   ```

   You can also up docker-compose in daemon mode

   ```sh
   $ docker-compose up --build -d
   ```

   You can up only one or more specified service

   ```sh
   $ docker-compose up --build pptp l2tp
   ```

### What's next

You should edit configs to solve following issues:

1. Apache2 `ServerName` is not properly configured, so you will always visit the default website.
1. Ensure ftp user roots exist and have the proper owner, or vsftpd will fail.
1. The default vsftpd passwords are weak and public available.
1. The default pptp password and l2tp password are weak and public available.
1. OpenVPN key file is broken and openvpn will fail. Please use the correct key file.
1. OpenVPN `CLIENT_SECRET` is weak.
1. The default mysql root password is unsafe, please login to phpmyadmin and change it.
1. Create a database and db user, and then config cgserver to the correct database.
1. Futher configure cgserver.
1. The default svn admin password is unsafe, please login to svn and change it.
1. Letsencrypt domain name is not properly configured, so it's failed to issue SSL certificates.
1. Edit apache2 *\*-le-ssl.conf* to use SSL, and edit HTTP configs to redirect to HTTPS.
1. Force vsftpd to use SSL connections.
1. Add a service to run letsencrypt in cycle to renew certificates.
1. Add a service to run backup in cycle.

## Services

### apache2

1. Copy *apache2/conf/sites-available.sample/* to *apache2/conf/sites-available/* and edit then (fill `ServerName`).
1. Build and run.
1. After certificates are issued, we can further edit configs in *apache2/conf/sites-available/*, enable SSL, and rewrite HTTP to HTTPS.

### vsftpd

1. Copy *vsftpd/conf/vsftpd.conf.sample* to *vsftpd/conf/vsftpd.conf.txt*.
1. Copy *vsftpd/conf/vusers.txt.sample* to *vsftpd/conf/vusers.txt* and edit it.
1. Edit config files in *vsftpd/conf/vsftpd_user_conf/*.
1. Build and run.
1. Ensure user roots (*/srv/ftp/cscg* and */srv/ftp/oslab*) exists and have the proper owner. For the first run, you can run `docker-compose exec vsftpd bash -c 'mkdir -p /srv/ftp/{cscg,oslab} && chown ftp:ftp /srv/ftp/{cscg,oslab}'`
1. After certificates are issued, we can further edit configs in *vsftpd/conf/vsftpd.conf*, set `ssl_enable=YES`, `force_local_logins_ssl=YES` and so on.

### netredirect

1. Copy *netredirect/conf/sites-available.sample/* to *netredirect/conf/sites-available/*.
1. Build and run.
1. After certificates are issued, we can further edit configs in *netredirect/conf/sites-available/*, enable SSL, and rewrite HTTP to HTTPS.

### pptp

1. Edit `PPTP_*` in *.env*.
1. Build and run.

### l2tp

1. Load the IPsec af_key kernel module on the Docker host: `sudo modprobe af_key`.
1. Edit `L2TP_*` in *.env*.
1. Build and run.

### openvpn

1. Generate *openvpn/conf/dh2048.pem* by running `openssl dhparam -out openvpn/conf/dh2048.pem 2048`.
1. Create *openvpn/conf/server.key* (see *openvpn/conf/server.key.sample* for the format).
1. Copy *openvpn/conf/settings.py.sample* to *openvpn/conf/settings.py* and edit it (fill `CLIENT_SECRET`).
1. Build and run.

### mysql

1. Run.
1. Login to phpmyadmin and change root password.

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

### csvn

1. Build and run.
1. login to csvn and change admin password.
1. In "Server Settings", set hostname and force apache encryption.

### letsencrypt

1. Copy *letsencrypt/sites.env.sample* to *letsencrypt/sites.env* and edit it.
1. Build and run.
1. Update apache2 config files and reload apache2 by running `docker-compose exec apache2 apachectl -k graceful` and `docker-compose exec netredirect apachectl -k graceful`.

Each certificate expires in about 3 months, so letsencrypt should be run in cycles to renew certificates. Apache2 should be running when renewing certificates.

### backup

Run `docker bulid backup` and `docker run --rm backup <action>`. `action` can be:

 - `nothing`: 不执行任何任务（用于 `docker-compose up`）
 - `rsync-only`: 执行基于时间戳的 rsync 但不 commit，不创建历史版本，运行速度比较快
 - `commit-timestamp`: 执行基于时间戳 rsync 并 commit，创建历史版本，运行速度一般
 - `commit-checksum`: 执行基于文件校验码的 rsync 并 commit，创建历史版本，运行速度很慢
 - `gc`: 只执行 `git gc`

一般定时运行 commit-timestamp，隔很长时间运行 commit-checksum 和 gc。docker-compose 启动时自动运行 rsync-only。

稳定的备份文件在 backup_storage 卷中。代码确保 backup_storage/repo/ 的备份是原子性的，只要存在该目录就一定有完整的备份。如果某次备份报错或中断，则可能导致该目录不存在，此时 backup_cache/ 与 backup_storage/repo.tmp/ 至少有一个是完整的备份，并且代码会拒绝执行备份操作直至修复。

## Todo

- [x] Support HTTPS for apache2. Mount cert files into apache2 container, and add a service to renew certifications.
- [x] Add cgserver service.
- [x] Handle static files in cgserver.
- [x] Redirect traffic to *net.tsinghua.edu.cn* to another page by DNAT.
- [x] Put ftp and mysql data into a Docker volume.
- [x] Add OpenVPN protocol TCP.
- [x] Make it easier to configure apache2.
- [ ] Make it easier to configure openvpn.
- [x] OpenVPN communicate with cgserver through intranet.
- [x] Add an automate script to generate configs (just copy sample configs).
- [x] Make netredirect more friendly.
- [x] Build all docker images from *debian:stretch* and we will have no need to build *cscg/base*.
- [x] Promote FTP to FTPS.
- [x] Backup script.
- [x] Should not put .well-known of *cgserver* and *svn* into ftp.
- [ ] Mysql incremental backup.
- [ ] Move some configs to *.env*.
