FROM cscg/base

RUN apt-get update && \
	apt-get install --no-install-recommends -y openvpn iptables dnsutils && \
	rm -rf /var/lib/apt/lists/*

RUN pip install requests && \
	rm -r ~/.cache/pip

COPY conf /etc/openvpn/cscg/conf
COPY entrypoint.sh /entrypoint.sh
RUN mkdir /etc/openvpn/cscg/log

EXPOSE 1194/udp
ENTRYPOINT ["/entrypoint.sh"]
WORKDIR /etc/openvpn/cscg/conf
CMD ["openvpn", "server.conf"]
