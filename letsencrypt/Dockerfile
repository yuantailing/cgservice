FROM debian:buster

RUN sed -i s/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g /etc/apt/sources.list && \
	sed -i s/security.debian.org/mirrors.tuna.tsinghua.edu.cn/g /etc/apt/sources.list

RUN apt-get update && \
	apt-get install --no-install-recommends -y python3 python3-pip python3-setuptools && \
	rm -rf /var/lib/apt/lists/*

RUN pip3 install certbot certbot-dns-route53 && \
	rm -rf ~/.cache/pip

COPY runscript.py /runscript.py
CMD ["/runscript.py"]
