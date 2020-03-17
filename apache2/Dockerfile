FROM debian:buster

RUN sed -i s/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g /etc/apt/sources.list && \
	sed -i s/security.debian.org/mirrors.tuna.tsinghua.edu.cn/g /etc/apt/sources.list

RUN apt-get update && \
	apt-get install --no-install-recommends -y apache2 cron libapache2-mod-security2 logrotate modsecurity-crs && \
	rm -rf /var/lib/apt/lists/*

COPY conf/conf-available/*.conf /etc/apache2/conf-available/
COPY conf/options-ssl-apache.conf /opt/letsencrypt/options-ssl-apache.conf
COPY conf/logrotate_apache2.conf /etc/logrotate.d/apache2

RUN a2enmod expires headers http2 mime proxy proxy_http proxy_wstunnel remoteip rewrite security2 ssl
RUN a2enconf cg-default logformat
RUN sed "s/ServerSignature On/ServerSignature Off/" -i /etc/apache2/conf-available/security.conf && \
	sed "s/Alias \/icons\//#&/" -i /etc/apache2/mods-available/alias.conf

COPY conf/sites-available/*.conf /etc/apache2/sites-available/
RUN cd /etc/apache2/sites-available/ && a2ensite $(find -type f -and -not -name "*default*")

EXPOSE 80 443
CMD sh -c "service cron start && apachectl -D FOREGROUND"
