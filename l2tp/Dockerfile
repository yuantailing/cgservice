FROM debian:stretch

RUN sed -i s/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g /etc/apt/sources.list && \
	sed -i s/security.debian.org/mirrors.tuna.tsinghua.edu.cn/g /etc/apt/sources.list

RUN apt-get update && \
	apt-get install --no-install-recommends -y ca-certificates curl dnsutils g++ git iptables libcharon-extra-plugins make strongswan xl2tpd && \
	rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/FreeRADIUS/freeradius-client.git /root/freeradius-client && \
	cd /root/freeradius-client && \
	./configure && \
	make && \
	make install && \
	rm -rf /root/freeradius-client

RUN sed -i "s/localhost/radius/g;s/^radius_deadtime/#&/;\$aseqfile         /var/run/radius.seq" /usr/local/etc/radiusclient/radiusclient.conf && \
	sed -i "s/.*ipv6/#&/;\$aINCLUDE /usr/local/etc/radiusclient/dictionary.microsoft" /usr/local/etc/radiusclient/dictionary && \
	curl https://raw.githubusercontent.com/radcli/radcli/master/etc/dictionary.microsoft -o /usr/local/etc/radiusclient/dictionary.microsoft && \
	echo "radius testing123" >>/usr/local/etc/radiusclient/servers

RUN sed -i "s/^\\s*# accounting =.*/    accounting = yes/;s/^\\s*# secret =.*/    secret = testing123/;s/^\\s*# server =.*/    server = radius/" /etc/strongswan.d/charon/eap-radius.conf

COPY conf/ipsec.conf /etc/ipsec.conf
COPY conf/xl2tpd.conf /etc/xl2tpd/xl2tpd.conf
COPY conf/options.xl2tpd /etc/ppp/options.xl2tpd
COPY runscript.sh /runscript.sh

EXPOSE 500/udp 4500/udp
CMD ["/runscript.sh"]
