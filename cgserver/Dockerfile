FROM debian:buster

RUN sed -i s/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g /etc/apt/sources.list && \
	sed -i s/security.debian.org/mirrors.tuna.tsinghua.edu.cn/g /etc/apt/sources.list

RUN apt-get update && \
	apt-get install --no-install-recommends -y apache2 default-libmysqlclient-dev gcc git libapache2-mod-wsgi-py3 python3 python3-dev python3-pip python3-setuptools && \
	rm -rf /var/lib/apt/lists/*

RUN pip3 install boto3 django django-extensions mysqlclient requests && \
	rm -rf ~/.cache/pip

RUN git clone https://github.com/yuantailing/cgserver.git /opt/cgserver && \
	cd /opt/cgserver && \
	git checkout 9dd23f56ff41290db4c8b7994e4eba3749285050 && \
	pip3 install -r cgserver/requirements.txt && \
	rm -rf ~/.cache/pip

COPY conf/settings.py /opt/cgserver/cgserver/cgserver/settings.py
COPY conf/000-default.conf /etc/apache2/sites-available/000-default.conf

WORKDIR /opt/cgserver/cgserver

RUN chown www-data:www-data cgserver/settings.py && \
	sed "s/admin\//serverlist\/admin\//" -i cgserver/urls.py && \
	python3 manage.py collectstatic && \
	a2enmod wsgi && \
	echo "application/x-openvpn-profile			ovpn" >>/etc/mime.types

EXPOSE 80
CMD ["apachectl", "-D", "FOREGROUND"]
