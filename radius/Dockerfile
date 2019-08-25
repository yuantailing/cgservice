FROM debian:stretch

RUN sed -i s/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g /etc/apt/sources.list && \
	sed -i s/security.debian.org/mirrors.tuna.tsinghua.edu.cn/g /etc/apt/sources.list

RUN apt-get update && \
	apt-get install --no-install-recommends -y freeradius python3 python3-pip && \
	rm -rf /var/lib/apt/lists/*

RUN pip3 install requests && \
	rm -rf ~/.cache/pip

RUN sed -i 's/^	ipaddr = .*$/	ipaddr = */g' /etc/freeradius/3.0/clients.conf && \
	sed -i '1i$INCLUDE cgauth' /etc/freeradius/3.0/mods-config/files/authorize && \
	sed -i '/^\s*acct_unique/a	update request { Nt-Password := "%{echo:/usr/bin/python3 /opt/cgauth/acct_req.py}" }' /etc/freeradius/3.0/sites-enabled/default

COPY conf/cgauth /etc/freeradius/3.0/mods-config/files/cgauth
COPY conf/fetch_nt_psw.py /opt/cgauth/fetch_nt_psw.py
COPY conf/acct_req.py /opt/cgauth/acct_req.py
COPY conf/settings.py /opt/cgauth/settings.py
RUN chown freerad:freerad /opt/cgauth/settings.py

EXPOSE 1812 1812/udp 1813 1813/udp
CMD freeradius -fxl stdout | grep -v User-Password --line-buffered
