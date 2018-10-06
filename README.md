# cgservice

Run All services in a docker compose.

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

1. Build and run.

### vsftpd

1. Copy *vsftpd/conf/vusers.txt.sample* to *vsftpd/conf/vusers.txt.sample* and edit it.
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

## todo

1. Support HTTPS for apache2. Mount cert files into apache2 container, and add a service to renew certifications.
1. Add cgserver service.
