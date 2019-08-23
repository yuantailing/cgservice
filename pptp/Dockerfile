FROM debian:stretch

RUN sed -i s/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g /etc/apt/sources.list && \
	sed -i s/security.debian.org/mirrors.tuna.tsinghua.edu.cn/g /etc/apt/sources.list

RUN apt-get update && \
	apt-get install --no-install-recommends -y ca-certificates curl dnsutils g++ git iptables make pptpd && \
	rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/FreeRADIUS/freeradius-client.git /root/freeradius-client && \
	cd /root/freeradius-client && \
	./configure && \
	make && \
	make install && \
	rm -rf /root/freeradius-client

RUN sed -i "s/localhost/radius/g;s/^radius_deadtime/#&/;\$aseqfile         /var/run/radius.seq" /usr/local/etc/radiusclient/radiusclient.conf && \
	sed -i "s/.*ipv6/#&/;\$aINCLUDE /usr/local/etc/radiusclient/dictionary.microsoft" /usr/local/etc/radiusclient/dictionary && \
	curl https://raw.githubusercontent.com/talkincode/ToughVPN/master/radius/dictionary/dictionary.microsoft -o /usr/local/etc/radiusclient/dictionary.microsoft && \
	echo "radius testing123" >>/usr/local/etc/radiusclient/servers

RUN echo "localip 192.168.61.1\nremoteip 192.168.61.134-238" >>/etc/pptpd.conf && \
	sed -i "s/^nologfd/#&/" /etc/ppp/pptpd-options && \
	echo "ms-dns 166.111.8.28\nms-dns 166.111.8.29\nlogfile /var/log/pptpd.log\nplugin radius.so\nradius-config-file /usr/local/etc/radiusclient/radiusclient.conf" >>/etc/ppp/pptpd-options

COPY runscript.sh /runscript.sh

EXPOSE 1723
CMD ["/runscript.sh"]
