FROM debian:stretch

RUN sed -i s/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g /etc/apt/sources.list && \
	sed -i s/security.debian.org/mirrors.tuna.tsinghua.edu.cn/g /etc/apt/sources.list

RUN apt-get update && \
	apt-get install --no-install-recommends -y pptpd iptables dnsutils && \
	rm -rf /var/lib/apt/lists/*

COPY conf/pptpd.conf /etc/pptpd.conf
COPY conf/pptpd-options /etc/ppp/pptpd-options
COPY conf/chap-secrets /etc/ppp/chap-secrets
COPY entrypoint.sh /entrypoint.sh

RUN chmod 600 /etc/ppp/chap-secrets

EXPOSE 1723
ENTRYPOINT ["/entrypoint.sh"]
CMD ["pptpd", "--fg"]
