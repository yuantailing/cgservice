FROM debian:buster

RUN sed -i s/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g /etc/apt/sources.list && \
	sed -i s/security.debian.org/mirrors.tuna.tsinghua.edu.cn/g /etc/apt/sources.list

RUN apt-get update && \
	apt-get install --no-install-recommends -y git locales python3 python3-openssl python3-pip python3-setuptools && \
	rm -rf /var/lib/apt/lists/*

RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
	dpkg-reconfigure --frontend=noninteractive locales && \
	update-locale LANG=en_US.UTF-8

ENV LANG=en_US.UTF-8 PYTHONIOENCODING=utf-8

RUN pip3 install requests git+https://github.com/yuantailing/pyftpdlib.git@patch-1 && \
	rm -rf ~/.cache/pip

COPY ftp /opt/ftp

RUN useradd -u10021 -m ftp

CMD ["python3", "/opt/ftp/main.py"]
