FROM debian:buster

RUN sed -i s/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g /etc/apt/sources.list && \
	sed -i s/security.debian.org/mirrors.tuna.tsinghua.edu.cn/g /etc/apt/sources.list

RUN apt-get update && \
	apt-get install --no-install-recommends -y certbot python-certbot-apache && \
	rm -rf /var/lib/apt/lists/*

COPY runscript.py /runscript.py
CMD ["/runscript.py"]
