FROM debian:stretch

RUN sed -i s/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g /etc/apt/sources.list && \
	sed -i s/security.debian.org/mirrors.tuna.tsinghua.edu.cn/g /etc/apt/sources.list

RUN apt-get update && \
	apt-get install --no-install-recommends -y openvpn iptables dnsutils python python-pip && \
	rm -rf /var/lib/apt/lists/*

RUN pip install requests && \
	rm -rf ~/.cache/pip

COPY conf /etc/openvpn/cscg/conf
COPY runscript.sh /runscript.sh

WORKDIR /etc/openvpn/cscg/conf

RUN mkdir ../log

EXPOSE 1194/udp
CMD ["/runscript.sh"]
