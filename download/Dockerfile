FROM debian:stretch

RUN sed -i s/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g /etc/apt/sources.list && \
	sed -i s/security.debian.org/mirrors.tuna.tsinghua.edu.cn/g /etc/apt/sources.list

RUN apt-get update && \
	apt-get install --no-install-recommends -y gcc apache2 git python3 python3-pip python3-setuptools aria2 iptables && \
	rm -rf /var/lib/apt/lists/*

RUN pip3 install django\<2 requests pymysql && \
	rm -rf ~/.cache/pip

RUN git clone --single-branch -b cg https://github.com/yuantailing/download9.git /srv/download9 && \
	cd /srv/download9 && \
	git checkout ae390562b7982f0cf38a97270c673350d4ef62f3

COPY runscript.sh /runscript.sh
COPY conf/settings.py /srv/download9/mysite/mysite/settings.py
COPY conf/aria2.conf /srv/aria/aria2.conf
COPY conf/000-default.conf /etc/apache2/sites-available/000-default.conf

WORKDIR /srv/download9/mysite
RUN python3 manage.py collectstatic --noinput
RUN a2enmod proxy proxy_http

EXPOSE 80
CMD ["/runscript.sh"]
