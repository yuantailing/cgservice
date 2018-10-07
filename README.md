# cgservice

Run All services in a docker composer.

## usage

### overall

1. Please inall [docker](https://docs.docker.com/install/linux/docker-ce/debian/) and [docker-compose](https://docs.docker.com/compose/install/#install-compose).

2. Build base image.

   ```sh
   $ cd base && ./build.sh
   ```

3. Run all services in docker-compose.

   ```sh
   $ docker-compose up --build -d
   ```

### apache2

1. Copy *apache2/conf/sites-available.sample/* to *apache2/conf/sites-available/* and edit then.
1. Before certificates are issued, we should disable *001-cscg-le-ssl*, *002-oslab-le-ssl*, and so on, provisionally.
1. Build and run.
1. When certificates have been issued, we can enable *001-cscg-le-ssl*, *002-oslab-le-ssl*, and so on, and rewrite HTTP to HTTPS (edit *apache2/conf/sites-available/*).

### vsftpd

1. Copy *vsftpd/conf/vusers.txt.sample* to *vsftpd/conf/vusers.txt* and edit it.
1. Edit config files in *vsftpd/conf/vsftpd_user_conf/*.
1. Build and run.

### pptp

1. Copy *pptp/conf/chap-secrets.sample* to *pptp/conf/chap-secrets* and edit it.
1. Build and run.

### l2tp

1. Load the IPsec af_key kernel module on the Docker host: `sudo modprobe af_key`.
1. Copy *l2tp/vpn.env.sample* to *l2tp/vpn.env* and edit it.
1. Run.

### openvpn

1. Generate *openvpn/conf/dh2048.pem* by running `openssl dhparam -out openvpn/conf/dh2048.pem 2048`.
1. Create *openvpn/conf/server.key* (see *openvpn/conf/server.key.sample* for the format).
1. Copy *openvpn/conf/settings.py.sample* to *openvpn/conf/settings.py* and edit it (fill `CLIENT_SECRET`).
1. Build and run.

### letsencrypt

1. Copy *letsencrypt/sites.env.sample* to *letsencrypt/sites.env* and edit it.
1. Build and run.
1. Reload apache2 certificates are updated by running `docker-compose exec apache2 apachectl -k graceful`.

Letsencrypt is not a part of docker-compose, it should be run in cycles. Apache2 should be running when renewing certificates.

### mysql

1. Copy *mysql/password.env.sample* to *mysql/password.env* and edit it. Note that the password set on the first run affects.
1. Run.

### phpmyadmin

1. Run.
1. You can login to phpmyadmin in the default website (URI is /phpmyadmin/).

### cgserver

1. Create a database and a user in database.
1. Copy *cgserver/conf/settings.py.sample* to *cgserver/conf/settings.py* and edit it (fill `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `DATABASES`, `GITHUB_CLIENT_SECRET`, `GITHUB_PERSONAL_ACCESS_TOKEN` and `VPN_CLIENT_SECRET`).
1. Build and run.
1. Run `docker-compose exec cgserver python3 manage.py migrate` to initialize database.
1. Run `docker-compose exec cgserver python3 manage.py createsuperuser` to a super user, who can login to Django administration.
1. Login to Django administration (URI is /admin/) and add server configs.

## todo

- [x] Support HTTPS for apache2. Mount cert files into apache2 container, and add a service to renew certifications.
- [x] Add cgserver service.
- [ ] Handle tatic files of cgserver.
- [ ] Redirect traffic to *net.tsinghua.edu.cn* to another page by DNAT.
- [ ] Put ftp into a Docker volume, so does mysql.
- [ ] Add a callback URL to GitHub OAuth.
- [ ] OpenVPN protocol TCP.
