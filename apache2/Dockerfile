FROM debian:stretch

RUN sed -i s/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g /etc/apt/sources.list && \
	sed -i s/security.debian.org/mirrors.tuna.tsinghua.edu.cn/g /etc/apt/sources.list

RUN apt-get update && \
	apt-get install --no-install-recommends -y apache2 && \
	rm -rf /var/lib/apt/lists/*

COPY conf/sites-available/*.conf /etc/apache2/sites-available/
COPY conf/options-ssl-apache.conf /opt/letsencrypt/options-ssl-apache.conf

RUN a2enmod http2 proxy proxy_http proxy_wstunnel rewrite ssl
RUN cd /etc/apache2/sites-available/ && a2ensite $(find -type f -and -not -name "*default*")

EXPOSE 80
EXPOSE 443
CMD ["apachectl", "-D", "FOREGROUND"]
