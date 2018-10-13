FROM debian:stretch

RUN sed -i s/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g /etc/apt/sources.list && \
	sed -i s/security.debian.org/mirrors.tuna.tsinghua.edu.cn/g /etc/apt/sources.list

RUN apt-get update && \
	apt-get install --no-install-recommends -y gcc apache2 git python3 python3-dev python3-pip python3-setuptools default-libmysqlclient-dev && \
	rm -rf /var/lib/apt/lists/*

RUN pip3 install django django-extensions mysqlclient && \
	rm -rf ~/.cache/pip

RUN git clone https://github.com/yuantailing/cgserver.git /opt/cgserver && \
	cd /opt/cgserver && \
	git checkout cc452f8dc246725d0eb80657d2f85890303b75c7 && \
	pip3 install -r cgserver/requirements.txt && \
	rm -rf ~/.cache/pip

COPY conf/settings.py /opt/cgserver/cgserver/cgserver/settings.py
COPY conf/000-default.conf /etc/apache2/sites-available/000-default.conf
COPY /runscript.sh /runscript.sh

WORKDIR /opt/cgserver/cgserver

RUN a2enmod proxy proxy_http
RUN python3 manage.py collectstatic
RUN useradd user

EXPOSE 80
CMD /runscript.sh
