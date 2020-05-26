FROM debian:buster

RUN sed -i s/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g /etc/apt/sources.list && \
	sed -i s/security.debian.org/mirrors.tuna.tsinghua.edu.cn/g /etc/apt/sources.list

RUN apt-get update && \
	apt-get install --no-install-recommends -y apache2 ssl-cert && \
	rm -rf /var/lib/apt/lists/*

COPY conf/sites-available/*.conf /etc/apache2/sites-available/
COPY conf/options-ssl-apache.conf /opt/letsencrypt/options-ssl-apache.conf

RUN rm -rf /var/www/html/*
COPY html/ /var/www/html/

RUN a2enmod rewrite ssl && \
	a2ensite 000-default 000-default-le-ssl

EXPOSE 80
EXPOSE 443
CMD ["apachectl", "-D", "FOREGROUND"]
