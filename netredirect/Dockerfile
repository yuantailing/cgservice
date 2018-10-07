FROM cscg/base

RUN apt-get update && \
	apt-get install --no-install-recommends -y apache2 && \
	rm -rf /var/lib/apt/lists/*

COPY conf/sites-available/*.conf /etc/apache2/sites-available/
COPY conf/options-ssl-apache.conf /opt/letsencrypt/options-ssl-apache.conf

RUN a2enmod ssl && \
	a2ensite 000-default 000-default-le-ssl

EXPOSE 80
EXPOSE 443
CMD ["apachectl", "-D", "FOREGROUND"]
