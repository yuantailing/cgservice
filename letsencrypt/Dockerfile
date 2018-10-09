FROM debian:stretch

RUN sed -i s/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g /etc/apt/sources.list && \
	sed -i s/security.debian.org/mirrors.tuna.tsinghua.edu.cn/g /etc/apt/sources.list

RUN echo "deb http://deb.debian.org/debian stretch-backports main" >/etc/apt/sources.list.d/backports.list && \
	apt-get update && \
	apt-get install --no-install-recommends -y python && \
	apt-get install --no-install-recommends -y certbot -t stretch-backports && \
	rm -rf /var/lib/apt/lists/*

COPY runscript.py /runscript.py
CMD ["/runscript.py"]
