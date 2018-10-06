FROM cscg/base

RUN apt-get update && \
	apt-get install --no-install-recommends -y pptpd iptables && \
    rm -rf /var/lib/apt/lists/*

COPY conf/pptpd.conf /etc/pptpd.conf
COPY conf/pptpd-options /etc/ppp/pptpd-options
COPY conf/chap-secrets /etc/ppp/chap-secrets
COPY entrypoint.sh /entrypoint.sh

RUN chmod 600 /etc/ppp/chap-secrets

EXPOSE 1723
ENTRYPOINT ["/entrypoint.sh"]
CMD ["pptpd", "--fg"]
