FROM debian:buster

RUN sed -i s/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g /etc/apt/sources.list && \
	sed -i s/security.debian.org/mirrors.tuna.tsinghua.edu.cn/g /etc/apt/sources.list

RUN apt-get update && \
	apt-get install --no-install-recommends -y apache2 php libapache2-mod-php php-mysql && \
	rm -rf /var/lib/apt/lists/*

COPY 000-default.conf /etc/apache2/sites-available/000-default.conf
COPY secret /etc/cgservice/php/secret

RUN a2enmod php7.3

EXPOSE 80
CMD ["apachectl", "-D", "FOREGROUND"]
