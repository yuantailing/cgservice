FROM cscg/base

RUN apt-get update && \
	apt-get install --no-install-recommends -y apache2 && \
    rm -rf /var/lib/apt/lists/*

COPY conf/sites-available/*.conf /etc/apache2/sites-available/

RUN a2ensite 001-cscg 002-oslab

EXPOSE 80
CMD ["apachectl", "-D", "FOREGROUND"]
