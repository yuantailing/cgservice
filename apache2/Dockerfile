FROM cscg/base

RUN apt-get update && \
	apt-get install --no-install-recommends -y apache2 && \
	rm -rf /var/lib/apt/lists/*

COPY conf/sites-available/*.conf /etc/apache2/sites-available/
COPY conf/options-ssl-apache.conf /opt/letsencrypt/options-ssl-apache.conf

RUN a2enmod proxy proxy_http rewrite ssl && \
	a2ensite 001-cscg 002-oslab

RUN a2ensite 001-cscg-le-ssl 002-oslab-le-ssl

EXPOSE 80
CMD ["apachectl", "-D", "FOREGROUND"]
