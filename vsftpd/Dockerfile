FROM cscg/base

RUN apt-get update && \
	apt-get install --no-install-recommends -y ftp vsftpd db-util libpam-pwdfile && \
	rm -rf /var/lib/apt/lists/*

COPY conf/vsftpd.conf /etc/vsftpd.conf
COPY conf/vsftpd.virtual /etc/pam.d/vsftpd.virtual
COPY conf/vusers.txt /etc/vsftpd/vusers.txt
COPY conf/vsftpd_user_conf /etc/vsftpd_user_conf
COPY runscript.sh /runscript.sh

RUN db_load -T -t hash -f /etc/vsftpd/vusers.txt /etc/vsftpd/vsftpd-virtual-user.db && \
	chmod 600 /etc/vsftpd/vsftpd-virtual-user.db

RUN usermod -u10021 ftp && \
	groupmod -g10021 ftp && \
	mkdir -p /var/run/vsftpd/empty

EXPOSE 20
EXPOSE 21
CMD ["/runscript.sh"]
