# cgservice

Run all services in a docker composer.

## 概述

1. vsftpd 是 FTP 服务，用于上传文件到网站目录，开放 FTP 端口
1. apache2 用于托管网站（根据域名区分），开放 HTTP、HTTPS 端口
1. pptp、l2tp、openvpn 是几个 VPN 服务，开放各自的端口
1. netredirect 用于 VPN 重定向，VPN 把目的地址为 net.tsinghua.edu.cn 的流量重定向到这里，避免用户通过 VPN 意外“断开连接”
1. mysql 是内网数据库服务
1. phpmyadmin 是可视化管理 mysql 数据库的 web 服务，用 apache2 转发
1. php 是主页上唯一动态的部分，主页上的其它部分都是静态的
1. cgserver 是另一项 web 服务，并提供 openvpn 的认证，用 apache2 转发
1. csvn 是 SVN 服务，用 apache2 转发
1. download 是 fork 自 [Download9](https://download.net9.org) 的离线下载服务，用 apache2 转发
1. letsencrypt 用于签署 SSL 证书，使得 apache2 用 HTTPS，vsftpd 用 FTPS
1. backup 用于备份 ftp、svn 等数据卷的历史版本
1. 网络做了隔离，前端的 apache2 不能跟后端的 mysql 通信，各个 VPN 之间也不能通过内网通信
1. docker-compose 用于构建和管理这些服务，一键启动和停止整批服务

## Usage

### Quick start
1. Please inall [docker](https://docs.docker.com/install/linux/docker-ce/debian/) and [docker-compose](https://docs.docker.com/compose/install/).

1. Copy sample configs and make secret config files not globally visible.

   ```sh
   $ cp .env.sample .env && \
       cp -r apache2/conf/sites-available.sample/ apache2/conf/sites-available/ && \
       cp vsftpd/conf/vusers.txt.sample vsftpd/conf/vusers.txt && \
       cp -r netredirect/conf/sites-available.sample netredirect/conf/sites-available && \
       cp openvpn/conf/settings.py.sample openvpn/conf/settings.py && \
       cp openvpn/conf/server.key.sample openvpn/conf/server.key && \
       cp -r php/secret.sample php/secret && \
       cp cgserver/conf/settings.py.sample cgserver/conf/settings.py && \
       cp -r backup/exclude.sample backup/exclude && \
       cp -r backup/ignore.sample backup/ignore

   $ chmod 600 .env vsftpd/conf/vusers.txt openvpn/conf/settings.py \
       openvpn/conf/server.key cgserver/conf/settings.py

   $ chmod 700 php/secret
   ```

1. Build images

   ```sh
   $ docker-compose build
   ```

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
1. The default vsftpd passwords are unsafe.
1. The default pptp password and l2tp password are unsafe.
1. L2tp needs to oad the IPsec af_key kernel module on the Docker host: `sudo modprobe af_key`.
1. OpenVPN key file is broken and openvpn will fail. Please use the correct key file.
1. OpenVPN `CLIENT_SECRET` is unsafe.
1. The default mysql root password is unsafe, please login to phpmyadmin and change it.
1. Create a database and db user, and then config cgserver to the correct database.
1. Configure GitHub OAuth for cgserver.
1. The default svn admin password is unsafe, please login to svn and change it.
1. Configure GitHub OAuth and initialize database for download.
1. Letsencrypt domain name is not properly configured, so it's failed to issue SSL certificates.
1. Edit apache2 (and netredirect) *\*-le-ssl.conf* to use SSL, and edit HTTP configs to redirect to HTTPS.
1. Edit *.env* to force vsftpd to use SSL connections.
1. If your server is out of Tsinghua University, please change `ms-dns` to another DNS server in *pptp/conf/pptpd-options*.
1. Add a service to run letsencrypt in cycle to renew certificates.
1. Add a service to run backup in cycle.

## Services

### apache2

1. Fill `ServerName` in *apache2/conf/sites-available/*.
1. Build and run.
1. After certificates are issued, we can further edit configs in *apache2/conf/sites-available/* to enable SSL and rewrite HTTP to HTTPS.

### vsftpd

1. Change passwords in *vsftpd/conf/vusers.txt*.
1. (optional) Edit config files in *vsftpd/conf/vsftpd_user_conf/*.
1. Build and run.
1. Ensure user roots (*/srv/ftp/cscg* and */srv/ftp/oslab*) exists and have the proper owner. For the first run, you can run `docker-compose exec vsftpd bash -c 'mkdir -p /srv/ftp/{cscg,oslab} && chown ftp:ftp /srv/ftp/{cscg,oslab}'`
1. After certificates are issued, we can edit config in *.env*, set `VSFTPD_SSL_ENABLE=1`.

### netredirect

1. Build and run.
1. After certificates are issued, we can edit configs in *netredirect/conf/sites-available/* to enable SSL.

### pptp

1. Change password in *.env*.
1. Build and run.

### l2tp

1. Load the IPsec af_key kernel module on the Docker host: `sudo modprobe af_key`.
1. Change password in *.env*.
1. Build and run.

### openvpn

1. Create *openvpn/conf/server.key* (see *openvpn/conf/server.key.sample* for the format).
1. Fill `CLIENT_SECRET` in *openvpn/conf/settings.py*.
1. Build and run.

### mysql

1. Run.
1. Login to phpmyadmin and change root password.

### phpmyadmin

1. Run.
1. You can login to phpmyadmin in the default website (usually you can visit it by IP, and URI is /phpmyadmin/).

### php

1. Build and run.
1. You may keep something secret in *php/secret* (for example, config files, get database connection).

### cgserver

1. Create a database and a user in database.
1. Fill `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `DATABASES`, `GITHUB_CLIENT_SECRET`, `GITHUB_PERSONAL_ACCESS_TOKEN` and `VPN_CLIENT_SECRET` in *cgserver/conf/settings.py*.
1. Build and run.
1. Run `docker-compose exec cgserver python3 manage.py migrate` to initialize database.
1. Run `docker-compose exec cgserver python3 manage.py createsuperuser` to a super user, who can login to Django administration.
1. Login to Django administration (URI is /admin/) and add some server configs.

### csvn

1. Build and run.
1. login to csvn and change admin password.
1. Login to "Server Settings" and set *hostname*, enable *Apache use SSL* and set *port* to 443.

### download

1. Fill `DOWNLOAD_GITHUB_CLIENT_ID` and `DOWNLOAD_GITHUB_CLIENT_SECRET` in *.env*.
1. Build and run.
1. Run `docker-compose exec cgserver python3 manage.py migrate` to initialize database.

### letsencrypt

1. Edit `LETSENCRYPT_*` in *.env*.
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

使用 backup_storage 卷与 backup_cache 卷双备份，即使备份中断也至少有一个卷是完好的。如果 *backup_storage/backup.lock* 存在，则说明某次备份被中断，此时自动备份会拒绝执行，应手动检查哪一个卷完好，修复后再删除 *backup.lock*。

请修改 *backup/exclude/* 和 *backup/ignore/* 忽略没必要保存历史版本的大文件、文件众多的目录。

## Troubleshooting

If kernel version of host machine is greater than *linux-image-4.7.0-1-amd64*, you may have to run following script to allow GRE traffic forwarding for PPTP and L2TP.

   ```sh
   modprobe ip_conntrack_pptp
   sysctl -w net.netfilter.nf_conntrack_helper=1
  ```

Refer to post [#1](https://lists.debian.org/debian-kernel/2016/10/msg00029.html) and [#2](https://forums.docker.com/t/solved-incoming-network-traffic-not-forwarding-to-container/43191).

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
- [ ] Dynamic manage vsftpd user on web.
- [x] A service like [Download9](https://git.net9.org/sast/Download9).
- [ ] Fix PPTP for Ubuntu and fix L2TP for Mac.
