FROM debian:stretch

RUN sed -i s/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g /etc/apt/sources.list && \
	sed -i s/security.debian.org/mirrors.tuna.tsinghua.edu.cn/g /etc/apt/sources.list

RUN apt-get update && \
	apt-get install --no-install-recommends -y apache2 && \
	rm -rf /var/lib/apt/lists/*

COPY conf/sites-available/*.conf /etc/apache2/sites-available/
COPY conf/options-ssl-apache.conf /opt/letsencrypt/options-ssl-apache.conf

RUN a2enmod http2 proxy proxy_http rewrite ssl && \
	a2ensite 001-cscg 002-oslab 003-cgserver 004-svn 005-download && \
	a2ensite 001-cscg-le-ssl 002-oslab-le-ssl 003-cgserver-le-ssl 004-svn-le-ssl 005-download-le-ssl

EXPOSE 80
EXPOSE 443
CMD ["apachectl", "-D", "FOREGROUND"]
